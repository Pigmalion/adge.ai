#!/usr/bin/env python3
"""
Facebook Ads Library scraper for Nike ads.
Scrapes up to 50 ads and stores them in PostgreSQL database.
"""

import os
import sys
import time
import re
import requests
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database


class FacebookAdsScraper:
    """Scraper for Facebook Ads Library."""
    
    def __init__(self, max_ads: int = 50, assets_dir: str = "assets"):
        self.max_ads = max_ads
        self.ads_url = (
            "https://www.facebook.com/ads/library/"
            "?active_status=all&ad_type=all&country=US&is_targeted_country=false"
            "&media_type=all&search_type=page&view_all_page_id=15087023444"
        )
        self.db = Database()
        self.driver = None
        self.scraped_ads = []
        self.assets_dir = assets_dir
        self._ensure_assets_dirs()
    
    def _ensure_assets_dirs(self):
        """Create assets directories if they don't exist."""
        images_dir = os.path.join(self.assets_dir, "images")
        videos_dir = os.path.join(self.assets_dir, "videos")
        
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)
    
    def download_asset(self, asset_url: str, asset_type: str, ad_id: str) -> Optional[str]:
        """Download asset (image or video) and save locally.
        
        Returns:
            Local file path if successful, None otherwise
        """
        if not asset_url:
            return None
        
        try:
            # Determine file extension from URL or content type
            parsed_url = urlparse(asset_url)
            path = parsed_url.path
            
            # Get file extension
            if asset_type == 'image':
                if '.jpg' in path.lower() or 'jpeg' in path.lower():
                    ext = '.jpg'
                elif '.png' in path.lower():
                    ext = '.png'
                elif '.gif' in path.lower():
                    ext = '.gif'
                elif '.webp' in path.lower():
                    ext = '.webp'
                else:
                    ext = '.jpg'  # Default for images
                subdir = "images"
            else:  # video
                if '.mp4' in path.lower():
                    ext = '.mp4'
                elif '.webm' in path.lower():
                    ext = '.webm'
                elif '.mov' in path.lower():
                    ext = '.mov'
                else:
                    ext = '.mp4'  # Default for videos
                subdir = "videos"
            
            # Create filename: ad_id + extension
            filename = f"{ad_id}{ext}"
            filepath = os.path.join(self.assets_dir, subdir, filename)
            
            # Skip if file already exists
            if os.path.exists(filepath):
                return filepath
            
            # Download the asset
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(asset_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filepath
            
        except Exception as e:
            print(f"    ⚠️  Could not download asset for ad {ad_id}: {e}")
            return None
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        # Run in headless mode for production, but visible for debugging
        if os.getenv('HEADLESS', 'true').lower() == 'true':
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Use webdriver-manager to automatically handle ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            print("✓ Chrome WebDriver initialized")
            return True
        except Exception as e:
            print(f"✗ Error setting up WebDriver: {e}")
            print("  Make sure Chrome is installed")
            return False
    
    def scroll_and_extract_ads(self, target_count: int):
        """Scroll the page and extract ads until we have enough valid ads."""
        print(f"  Scrolling and extracting ads (target: {target_count})...")
        scroll_attempts = 0
        max_scroll_attempts = 50
        last_valid_count = 0
        
        while len(self.scraped_ads) < target_count and scroll_attempts < max_scroll_attempts:
            # Find ad containers
            try:
                ad_containers = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "div[class*='xh8yej3']"
                )
            except:
                ad_containers = []
            
            # Try to extract ads from visible containers
            for i, container in enumerate(ad_containers):
                if len(self.scraped_ads) >= target_count:
                    break
                
                # Skip if we've already processed this ad
                try:
                    ad_id = self.extract_ad_id(container)
                    if ad_id and any(ad.get('ad_id') == ad_id for ad in self.scraped_ads):
                        continue
                except:
                    pass
                
                # Try to extract this ad
                ad_data = self.extract_ad_data(container, len(self.scraped_ads))
                if ad_data and ad_data.get('ad_id'):
                    # Check if we already have this ad
                    if not any(ad.get('ad_id') == ad_data.get('ad_id') for ad in self.scraped_ads):
                        self.scraped_ads.append(ad_data)
                        
                        # Console log first 10 ads
                        if len(self.scraped_ads) <= 10:
                            print(f"\n    📋 Ad #{len(self.scraped_ads)} Data:")
                            print(f"       Ad ID: {ad_data.get('ad_id')}")
                            print(f"       Status: {ad_data.get('status')}")
                            print(f"       Platforms: {ad_data.get('platforms')}")
                            print(f"       Start Date: {ad_data.get('start_date')}")
                            print(f"       End Date: {ad_data.get('end_date')}")
                            print(f"       Multiple Versions: {ad_data.get('multiple_versions')}")
                            print(f"       Asset URL: {ad_data.get('asset_url', 'N/A')[:80]}...")
                            if ad_data.get('asset_path'):
                                print(f"       Asset saved: {ad_data.get('asset_path')}")
                            print()
                        
                        # Save to database
                        self.db.insert_ad(ad_data)
                        print(f"    ✓ Saved ad {len(self.scraped_ads)}/{target_count}: {ad_data.get('ad_id')}")
            
            # Check if we got new valid ads
            if len(self.scraped_ads) == last_valid_count:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_valid_count = len(self.scraped_ads)
            
            # If we have enough, stop
            if len(self.scraped_ads) >= target_count:
                break
            
            # Scroll down to load more
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load
        
        print(f"  Finished. Extracted {len(self.scraped_ads)} valid ads")
    
    def extract_ad_id(self, element) -> Optional[str]:
        """Extract Library ID from ad element."""
        try:
            # Look for "Library ID: XXXXX" text
            text_elements = element.find_elements(By.XPATH, ".//span[contains(text(), 'Library ID:')]")
            for elem in text_elements:
                text = elem.text
                match = re.search(r'Library ID:\s*(\d+)', text)
                if match:
                    return match.group(1)
        except:
            pass
        return None
    
    def extract_status(self, element) -> str:
        """Extract ad status (Active/Inactive)."""
        try:
            # Look for status text - it's in a span with class containing 'x117nqv4' or 'xeuugli'
            # The text "Active" or "Inactive" appears directly in a span
            status_elements = element.find_elements(By.XPATH, ".//span[text()='Active' or text()='Inactive']")
            if not status_elements:
                # Try with contains
                status_elements = element.find_elements(By.XPATH, ".//span[contains(text(), 'Active') or contains(text(), 'Inactive')]")
            
            for elem in status_elements:
                text = elem.text.strip()
                if text == 'Active' or 'Active' in text:
                    return 'active'
                elif text == 'Inactive' or 'Inactive' in text:
                    return 'inactive'
        except Exception as e:
            pass
        return 'unknown'
    
    def extract_platforms(self, element) -> List[str]:
        """Extract platforms (Facebook, Instagram, etc.)."""
        platforms = []
        try:
            # Find the Platforms section - it's a span with "Platforms" text followed by a div
            platform_label = element.find_elements(By.XPATH, ".//span[contains(text(), 'Platforms')]")
            
            if platform_label:
                # Get the parent or following sibling that contains the icons
                # The icons are in divs with class 'x1rg5ohu' within the Platforms section
                platform_section = platform_label[0].find_elements(By.XPATH, "./following-sibling::div[1]")
                
                if platform_section:
                    platform_div = platform_section[0]
                    # Look for all icon containers in the platform section
                    icon_containers = platform_div.find_elements(By.CSS_SELECTOR, "div[class*='x1rg5ohu']")
                    
                    # Check each container for platform icons
                    for icon_container in icon_containers:
                        # Look for the icon div with style attribute
                        icon_divs = icon_container.find_elements(By.CSS_SELECTOR, "div[style*='mask-position']")
                        
                        for icon_div in icon_divs:
                            style = icon_div.get_attribute('style') or ''
                            
                            # Facebook icon: mask-position: -13px -2812px
                            if '-13px -2812px' in style or '-13px-2812px' in style.replace(' ', ''):
                                if 'Facebook' not in platforms:
                                    platforms.append('Facebook')
                            
                            # Instagram icon: mask-position: 0px -2825px
                            if '0px -2825px' in style or '0px-2825px' in style.replace(' ', ''):
                                if 'Instagram' not in platforms:
                                    platforms.append('Instagram')
            
            # If no platforms found, default to Facebook
            if not platforms:
                platforms = ['Facebook']
        except Exception as e:
            platforms = ['Facebook']  # Default
        
        return platforms
    
    def extract_dates(self, element) -> tuple:
        """Extract start and end dates from ad element."""
        start_date = None
        end_date = None
        
        try:
            # Look for the specific element structure: div.x3nfvp2.x1e56ztr > span with date text
            # The HTML structure is: <div class="x3nfvp2 x1e56ztr"><span class="x8t9es0 xw23nyj xo1l8bm x63nzvj x108nfp6 xq9mrsl x1h4wwuj xeuugli">Started running on 8 Jan 2026</span></div>
            # Try multiple XPath patterns to find date text
            date_patterns = [
                # Most specific: div with both classes, then span
                ".//div[contains(@class, 'x3nfvp2') and contains(@class, 'x1e56ztr')]//span[contains(text(), 'Started running on')]",
                # Try finding span with the specific classes
                ".//span[contains(@class, 'x8t9es0') and contains(@class, 'xw23nyj') and contains(@class, 'xo1l8bm') and contains(text(), 'Started running on')]",
                # Try finding the div first, then any span inside
                ".//div[contains(@class, 'x3nfvp2')]//span[contains(text(), 'Started running on')]",
                # Generic: any span with "Started running on"
                ".//span[contains(text(), 'Started running on')]",
                # Generic: any element with "Started running on"
                ".//*[contains(text(), 'Started running on')]",
            ]
            
            date_text = None
            for pattern in date_patterns:
                try:
                    date_elements = element.find_elements(By.XPATH, pattern)
                    for elem in date_elements:
                        text = elem.text.strip()
                        if 'Started running on' in text:
                            date_text = text
                            break
                    if date_text:
                        break
                except Exception as e:
                    if len(self.scraped_ads) < 3:
                        print(f"      DEBUG: Pattern error: {e}")
                    continue
            
            if date_text:
                # Parse different date formats:
                # "Started running on 8 Jan 2026" (day first, no comma) - PRIMARY FORMAT based on user's HTML
                # "Started running on Jan 8, 2026" (month first, with comma) - alternative format
                patterns = [
                    # Format: "Started running on 8 Jan 2026" (day first, no comma) - PRIMARY
                    r'Started running on\s+(\d+)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
                    # Format: "Started running on Jan 8, 2026" (month first, with comma)
                    r'Started running on\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d+),\s+(\d{4})',
                    # Format: "Started on 8 Jan 2026"
                    r'Started\s+(\d+)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
                    # Format: "Started on Jan 8, 2026"
                    r'Started\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d+),\s+(\d{4})',
                    # Generic: "8 Jan 2026" (day first, no comma) - try this before comma version
                    r'(\d+)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
                    # Generic: "Jan 8, 2026" (month first, with comma)
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d+),\s+(\d{4})',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, date_text, re.IGNORECASE)
                    if match:
                        groups = match.groups()
                        try:
                            # Check if first group is month name or day number
                            if groups[0] in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                                # Format: "Jan 8, 2026" - month, day, year
                                month, day, year = groups[0], groups[1], groups[2]
                            else:
                                # Format: "8 Jan 2026" - day, month, year
                                day, month, year = groups[0], groups[1], groups[2]
                            
                            # Parse month (handle both abbreviated and full names)
                            try:
                                month_num = datetime.strptime(month[:3], '%b').month
                            except:
                                month_num = datetime.strptime(month, '%B').month
                            
                            start_date = datetime(int(year), month_num, int(day)).date()
                            break
                        except Exception as e:
                            continue
            # Look for end date patterns (if present)
            if date_text:
                end_patterns = [
                    r'Ended\s+(\d+)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
                    r'Ended on\s+(\d+)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
                ]
                
                for pattern in end_patterns:
                    end_match = re.search(pattern, date_text, re.IGNORECASE)
                    if end_match:
                        day, month, year = end_match.groups()
                        try:
                            try:
                                month_num = datetime.strptime(month[:3], '%b').month
                            except:
                                month_num = datetime.strptime(month, '%B').month
                            end_date = datetime(int(year), month_num, int(day)).date()
                            break
                        except:
                            continue
        except Exception as e:
            pass
        
        return start_date, end_date
    
    def extract_asset(self, element) -> tuple:
        """Extract ad asset (image/video) URL."""
        asset_url = None
        asset_type = 'image'
        
        try:
            # Look for the main ad image - it's in the ad content area
            # The large image is typically in a div with class containing 'x1ywc1zp' or similar
            # Try to find the largest image (the actual ad asset, not the profile pic)
            
            # First, try to find images in the ad content container
            ad_content = element.find_elements(By.CSS_SELECTOR, "div[data-testid='ad-library-dynamic-content-container']")
            if ad_content:
                # Look for large images (s600x600) which are the ad assets
                img_elements = ad_content[0].find_elements(By.CSS_SELECTOR, "img[src*='s600x600'], img[src*='s1080x1080']")
                if img_elements:
                    asset_url = img_elements[0].get_attribute('src')
                    asset_type = 'image'
            
            # Fallback: try any large image in the element
            if not asset_url:
                img_elements = element.find_elements(By.CSS_SELECTOR, "img[src*='fbcdn.net'][src*='s600x600'], img[src*='fbcdn.net'][src*='s1080x1080']")
                if img_elements:
                    asset_url = img_elements[0].get_attribute('src')
                    asset_type = 'image'
            
            # Check for video
            video_elements = element.find_elements(By.CSS_SELECTOR, "video")
            if video_elements:
                asset_url = video_elements[0].get_attribute('src')
                if not asset_url:
                    # Try poster image
                    poster = video_elements[0].get_attribute('poster')
                    if poster:
                        asset_url = poster
                        asset_type = 'image'
                else:
                    asset_type = 'video'
        except Exception as e:
            pass
        
        return asset_url, asset_type
    
    def extract_multiple_versions(self, element) -> bool:
        """Check if ad has multiple versions."""
        try:
            # Look for "This ad has multiple versions" text
            multiple_versions_elements = element.find_elements(
                By.XPATH, 
                ".//span[contains(text(), 'This ad has multiple versions')]"
            )
            return len(multiple_versions_elements) > 0
        except:
            return False
    
    def extract_ad_data(self, element, index: int) -> Optional[Dict]:
        """Extract all data from a single ad element."""
        try:
            ad_id = self.extract_ad_id(element)
            if not ad_id:
                # Skip if we can't get a valid Library ID
                return None
            
            status = self.extract_status(element)
            platforms = self.extract_platforms(element)
            start_date, end_date = self.extract_dates(element)
            asset_url, asset_type = self.extract_asset(element)
            multiple_versions = self.extract_multiple_versions(element)
            
            # Download asset if URL is available
            asset_path = None
            if asset_url:
                asset_path = self.download_asset(asset_url, asset_type, ad_id)
            
            ad_data = {
                'ad_id': ad_id,
                'status': status,
                'platforms': platforms,
                'start_date': start_date,
                'end_date': end_date,
                'asset_url': asset_url,
                'asset_type': asset_type,
                'asset_path': asset_path,  # Local file path
                'multiple_versions': multiple_versions
            }
            
            return ad_data
        except Exception as e:
            print(f"    ✗ Error extracting ad data: {e}")
            return None
    
    def scrape_ads(self) -> List[Dict]:
        """Main scraping method."""
        if not self.setup_driver():
            return []
        
        try:
            print(f"  Navigating to: {self.ads_url}")
            self.driver.get(self.ads_url)
            
            # Wait for page to load
            print("  Waiting for page to load...")
            time.sleep(5)
            
            # Scroll and extract ads until we have enough
            self.scroll_and_extract_ads(self.max_ads)
            
            # Count downloaded assets
            assets_downloaded = sum(1 for ad in self.scraped_ads if ad.get('asset_path'))
            print(f"\n✓ Successfully scraped {len(self.scraped_ads)} ads")
            print(f"✓ Downloaded {assets_downloaded} assets (saved locally)")
            return self.scraped_ads
            
        except Exception as e:
            print(f"✗ Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if self.driver:
                self.driver.quit()
                print("✓ WebDriver closed")
    
    def close(self):
        """Close database connection."""
        self.db.close()


def main():
    """Main entry point."""
    print("=" * 60)
    print("Facebook Ads Library Scraper - Nike")
    print("=" * 60)
    
    scraper = FacebookAdsScraper(max_ads=50)
    
    try:
        ads = scraper.scrape_ads()
        
        if ads:
            print(f"\n✓ Scraping completed. Found {len(ads)} ads")
            print(f"✓ Data saved to PostgreSQL database")
        else:
            print("\n✗ No ads were scraped")
    
    except KeyboardInterrupt:
        print("\n\n✗ Scraping interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

