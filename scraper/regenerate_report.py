#!/usr/bin/env python3
"""
Regenerate HTML report from existing database data.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from html_report import HTMLReportGenerator

def main():
    """Regenerate the HTML report."""
    print("=" * 60)
    print("Regenerating HTML Report...")
    print("=" * 60)
    
    report_generator = HTMLReportGenerator()
    
    try:
        report_path = report_generator.generate_report()
        report_abs_path = os.path.abspath(report_path)
        print(f"\n✓ Report generated successfully!")
        print(f"  Report location: {report_abs_path}")
        
        # Open report in browser
        import webbrowser
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

