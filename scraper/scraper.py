#!/usr/bin/env python3
"""
Main entry point for Facebook Ads Library scraper.
Runs the scraper and generates HTML report.
"""

import os
import sys
import webbrowser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from facebook_ads_scraper import FacebookAdsScraper
from html_report import HTMLReportGenerator


def main():
    """Main entry point - runs scraper and generates report."""
    print("=" * 60)
    print("Facebook Ads Library Scraper - Nike")
    print("=" * 60)
    print()
    
    # Step 1: Scrape ads
    print("Step 1: Scraping ads from Facebook Ads Library...")
    scraper = FacebookAdsScraper(max_ads=50)
    
    try:
        ads = scraper.scrape_ads()
        
        if not ads:
            print("\n✗ No ads were scraped. Exiting.")
            return
        
        print(f"\n✓ Successfully scraped {len(ads)} ads")
        scraper.close()
        
    except KeyboardInterrupt:
        print("\n\n✗ Scraping interrupted by user")
        scraper.close()
        return
    except Exception as e:
        print(f"\n✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        scraper.close()
        return
    
    # Step 2: Generate HTML report
    print("\n" + "=" * 60)
    print("Step 2: Generating HTML report...")
    print("=" * 60)
    
    report_generator = HTMLReportGenerator()
    
    try:
        report_path = report_generator.generate_report()
        report_abs_path = os.path.abspath(report_path)
        print(f"\n✓ Report generated successfully!")
        print(f"  Report location: {report_abs_path}")
        
        # Open report in browser
        print("  Opening report in browser...")
        webbrowser.open(f'file://{report_abs_path}')
        print("  ✓ Report opened in browser")
    except Exception as e:
        print(f"\n✗ Error generating report: {e}")
        import traceback
        traceback.print_exc()
    finally:
        report_generator.close()
    
    print("\n" + "=" * 60)
    print("✓ Process completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

