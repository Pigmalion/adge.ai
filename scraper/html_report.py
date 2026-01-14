"""
HTML report generator for scraped ads.
"""

import os
from datetime import datetime
from typing import List
from database import Database


class HTMLReportGenerator:
    """Generate HTML reports from scraped ads."""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.db = Database()
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_report(self) -> str:
        """Generate HTML report from database."""
        ads = self.db.get_all_ads()
        
        if not ads:
            return self._generate_empty_report()
        
        # Convert RealDictRow to regular dict
        # RealDictRow preserves date objects correctly when converted to dict
        ads_list = []
        for ad in ads:
            ad_dict = dict(ad)
            # Ensure date objects are preserved
            ads_list.append(ad_dict)
        
        # Sort ads: active first, then inactive
        ads_list.sort(key=lambda x: (x.get('status', 'unknown') != 'active', x.get('ad_id', '')))
        
        html_content = self._generate_html(ads_list)
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ads_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML report generated: {filepath}")
        return filepath
    
    def _generate_empty_report(self) -> str:
        """Generate empty report when no ads found."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Ads Report - No Data</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
        .empty { color: #666; margin-top: 50px; }
    </style>
</head>
<body>
    <h1>Facebook Ads Library Report</h1>
    <div class="empty">
        <p>No ads found in database.</p>
        <p>Please run the scraper first.</p>
    </div>
</body>
</html>"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ads_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
    
    def _generate_html(self, ads: List[dict]) -> str:
        """Generate full HTML report."""
        total_ads = len(ads)
        active_ads = sum(1 for ad in ads if ad.get('status') == 'active')
        inactive_ads = total_ads - active_ads
        
        # Count platforms
        platform_counts = {}
        for ad in ads:
            platforms = ad.get('platforms', [])
            if isinstance(platforms, list):
                for platform in platforms:
                    platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Ads Report - Nike</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        h1 {{
            color: #1877f2;
            margin-bottom: 10px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .stat-card {{
            background: #f0f2f5;
            padding: 15px 20px;
            border-radius: 6px;
            flex: 1;
            min-width: 150px;
        }}
        .stat-label {{
            font-size: 12px;
            color: #65676b;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #1877f2;
        }}
        .ads-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .ad-card {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .ad-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .ad-header {{
            padding: 15px;
            border-bottom: 1px solid #e4e6eb;
        }}
        .ad-id {{
            font-size: 12px;
            color: #65676b;
            margin-bottom: 5px;
        }}
        .ad-status {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .status-active {{
            background: #42b72a;
            color: white;
        }}
        .status-inactive {{
            background: #e4e6eb;
            color: #65676b;
        }}
        .ad-platforms {{
            font-size: 12px;
            color: #65676b;
            margin-top: 5px;
        }}
        .ad-dates {{
            font-size: 11px;
            color: #8a8d91;
            margin-top: 5px;
        }}
        .ad-asset {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .ad-asset-container {{
            background: #f0f2f5;
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .no-asset {{
            color: #8a8d91;
            padding: 40px;
            text-align: center;
        }}
        .generated-at {{
            text-align: center;
            color: #8a8d91;
            font-size: 12px;
            margin-top: 30px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Facebook Ads Library Report - Nike</h1>
            <p>Scraped from Facebook Ads Library</p>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-label">Total Ads</div>
                    <div class="stat-value">{total_ads}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Active</div>
                    <div class="stat-value" style="color: #42b72a;">{active_ads}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Inactive</div>
                    <div class="stat-value" style="color: #8a8d91;">{inactive_ads}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Platforms</div>
                    <div class="stat-value" style="font-size: 18px;">{', '.join(platform_counts.keys()) if platform_counts else 'N/A'}</div>
                </div>
            </div>
        </header>
        
        <div class="ads-grid">
"""
        
        # Generate ad cards
        for ad in ads:
            status_class = 'status-active' if ad.get('status') == 'active' else 'status-inactive'
            status_text = ad.get('status', 'unknown').title()
            
            platforms = ad.get('platforms', [])
            if isinstance(platforms, list):
                platforms_text = ', '.join(platforms) if platforms else 'Unknown'
            else:
                platforms_text = str(platforms)
            
            start_date = ad.get('start_date')
            end_date = ad.get('end_date')
            dates_text = ""
            
            # Format dates properly (handle both date objects and strings)
            # Check for None explicitly and handle date objects
            if start_date is not None:
                try:
                    if isinstance(start_date, str):
                        dates_text += f"Started: {start_date}"
                    elif hasattr(start_date, 'strftime'):
                        # It's a date/datetime object
                        dates_text += f"Started: {start_date.strftime('%Y-%m-%d')}"
                    else:
                        # Fallback: convert to string
                        dates_text += f"Started: {str(start_date)}"
                except Exception as e:
                    # If formatting fails, just use string representation
                    dates_text += f"Started: {str(start_date)}"
            
            if end_date is not None:
                try:
                    if isinstance(end_date, str):
                        if dates_text:
                            dates_text += " | "
                        dates_text += f"Ended: {end_date}"
                    elif hasattr(end_date, 'strftime'):
                        # It's a date/datetime object
                        if dates_text:
                            dates_text += " | "
                        dates_text += f"Ended: {end_date.strftime('%Y-%m-%d')}"
                    else:
                        # Fallback: convert to string
                        if dates_text:
                            dates_text += " | "
                        dates_text += f"Ended: {str(end_date)}"
                except Exception as e:
                    # If formatting fails, just use string representation
                    if dates_text:
                        dates_text += " | "
                    dates_text += f"Ended: {str(end_date)}"
            
            if not dates_text:
                dates_text = "Date: Unknown"
            
            multiple_versions = ad.get('multiple_versions', False)
            multiple_versions_badge = "🔀 Multiple Versions" if multiple_versions else ""
            
            asset_url = ad.get('asset_url', '')
            asset_type = ad.get('asset_type', 'image')
            
            html += f"""
            <div class="ad-card">
                <div class="ad-header">
                    <div class="ad-id">Library ID: {ad.get('ad_id', 'N/A')}</div>
                    <span class="ad-status {status_class}">{status_text}</span>
                    {f'<div style="font-size: 11px; color: #1877f2; margin-top: 5px;">{multiple_versions_badge}</div>' if multiple_versions else ''}
                    <div class="ad-platforms">Platforms: {platforms_text}</div>
                    <div class="ad-dates">{dates_text}</div>
                </div>
                <div class="ad-asset-container">
"""
            
            if asset_url:
                if asset_type == 'video':
                    html += f'                    <video class="ad-asset" controls><source src="{asset_url}" type="video/mp4"></video>'
                else:
                    html += f'                    <img class="ad-asset" src="{asset_url}" alt="Ad asset" onerror="this.parentElement.innerHTML=\'<div class=\\\'no-asset\\\'>Image failed to load</div>\'">'
            else:
                html += '                    <div class="no-asset">No asset available</div>'
            
            html += """
                </div>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="generated-at">
            Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def close(self):
        """Close database connection."""
        self.db.close()

