# Facebook Ads Library Dashboard

A full-stack application for scraping and visualizing Facebook Ads Library data for Nike ads.

## Project Structure

```
adge.ai/
├── scraper/          # Python scraper
│   ├── scraper.py    # Main scraper script
│   ├── assets/       # Downloaded ad assets (images/videos)
│   └── requirements.txt
├── server/           # Node.js TypeScript backend
│   ├── src/
│   │   ├── config/   # Database configuration
│   │   ├── services/ # Business logic
│   │   ├── routes/   # API routes
│   │   └── types/     # TypeScript types
│   └── Dockerfile
├── client/           # React TypeScript frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── services/    # API services
│   │   └── types/       # TypeScript types
│   └── Dockerfile
└── docker-compose.yml
```

## Features

### Scraper
- Scrapes up to 50 Nike ads from Facebook Ads Library
- Extracts: Ad ID, Status, Platforms, Dates, Assets
- Downloads and stores ad assets (images/videos) locally
- Saves data to PostgreSQL database
- Generates HTML reports

### Backend API
- RESTful API endpoints for ads data
- PostgreSQL database integration
- Filtering and statistics endpoints
- Asset serving

### Frontend Dashboard
- Interactive charts (ads over time, by platform)
- Real-time statistics cards
- Advanced filtering (status, platform, date range)
- Ad cards with asset display
- Responsive design

## Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

## Setup

### 1. Database Setup

Create PostgreSQL database and configure credentials in `scraper/.env`:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=tempadsdb
DB_USER=app_user
DB_PASSWORD=your_password
```

### 2. Scraper Setup

```bash
cd scraper
pip install -r requirements.txt
```

### 3. Backend Setup

```bash
cd server
npm install
npm run build
```

Create `server/.env`:
```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=tempadsdb
DB_USER=app_user
DB_PASSWORD=your_password
PORT=3001
```

### 4. Frontend Setup

```bash
cd client
npm install
```

## Running

### Development Mode

**Terminal 1 - Backend:**
```bash
cd server
npm run dev
```

**Terminal 2 - Frontend:**
```bash
cd client
npm start
```

**Terminal 3 - Scraper (when needed):**
```bash
cd scraper
python3 scraper.py
```

### Production with Docker

```bash
docker-compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001

## API Endpoints

- `GET /api/ads` - Get all ads (with optional filters)
  - Query params: `status`, `platform`, `startDate`, `endDate`, `multipleVersions`
- `GET /api/ads/:adId` - Get specific ad
- `GET /api/ads/stats/summary` - Get statistics
- `GET /api/ads/assets/:type/:filename` - Serve asset files
- `GET /api/health` - Health check

## Dashboard Features

- **Statistics Cards**: Total ads, active/inactive counts, multiple versions
- **Charts**: 
  - Ads over time (line chart)
  - Ads by platform (bar chart)
- **Filters**:
  - Status (active/inactive)
  - Platform (Facebook/Instagram)
  - Date range
  - Multiple versions toggle
- **Ad Grid**: Display ads with assets, status, platforms, dates

## Technologies

- **Backend**: Node.js, Express, TypeScript, PostgreSQL
- **Frontend**: React, TypeScript, SCSS, Recharts
- **Scraper**: Python, Selenium, PostgreSQL
- **Docker**: Containerized deployment

## License

ISC
