# Facebook Ads Library Scraper

Scraper for extracting Nike ads from Facebook Ads Library and storing them in PostgreSQL database.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install ChromeDriver

The scraper uses Selenium with Chrome. You need ChromeDriver installed:

**macOS:**
```bash
brew install chromedriver
```

**Linux:**
```bash
# Download from https://chromedriver.chromium.org/
# Or use package manager
sudo apt-get install chromium-chromedriver
```

**Windows:**
Download from https://chromedriver.chromium.org/ and add to PATH

### 3. Configure Environment Variables

Create a `.env` file in the `scraper/` directory with the following variables:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=tempadsdb
DB_USER=app_user
DB_PASSWORD=your_password_here
HEADLESS=true
MAX_ADS=50
```

#### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DB_HOST` | PostgreSQL database host | Yes | `localhost` |
| `DB_PORT` | PostgreSQL database port | Yes | `5432` |
| `DB_NAME` | PostgreSQL database name | Yes | `tempAdsDB` |
| `DB_USER` | PostgreSQL database user | Yes | `app_user` |
| `DB_PASSWORD` | PostgreSQL database password | Yes | - |
| `HEADLESS` | Run Chrome in headless mode (`true` or `false`) | No | `true` |
| `MAX_ADS` | Maximum number of ads to scrape | No | `50` |

### 4. Create Database

Make sure PostgreSQL is running and create the database:

```sql
CREATE DATABASE tempAdsDB;
```

The scraper will automatically create the required tables on first run.

## Usage

### Run the Scraper

```bash
python scraper/scraper.py
```

Or:

```bash
cd scraper
python scraper.py
```

The scraper will:
1. Connect to Facebook Ads Library
2. Scroll to load ads (up to 50)
3. Extract ad data (ID, status, platforms, dates, assets)
4. Save to PostgreSQL database
5. Generate an HTML report in `reports/` directory

### Generate HTML Report Only

If you want to regenerate the HTML report from existing database data:

```python
from html_report import HTMLReportGenerator

generator = HTMLReportGenerator()
report_path = generator.generate_report()
generator.close()
```

## Data Extracted

For each ad, the scraper extracts:
- **Ad ID**: Library ID from Facebook
- **Status**: Active or Inactive
- **Platforms**: Facebook, Instagram, etc.
- **Start Date**: When the ad started running
- **End Date**: When the ad ended (if applicable)
- **Asset URL**: Image or video URL
- **Asset Type**: Image or video

## Output

- **Database**: All ads are stored in PostgreSQL `ads` table
- **HTML Report**: Generated in `scraper/reports/ads_report_TIMESTAMP.html`

## Troubleshooting

### ChromeDriver Issues
- Make sure ChromeDriver version matches your Chrome version
- Check that ChromeDriver is in your PATH

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

### Scraping Issues
- Facebook may block automated access - try running with `HEADLESS=false` to see what's happening
- Increase wait times if ads aren't loading
- Check your internet connection

## Notes

- The scraper scrolls the page to load ads dynamically
- Facebook's HTML structure may change, requiring selector updates
- Some ads may not have all fields (dates, assets, etc.)

