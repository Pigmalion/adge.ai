# Facebook Ads Library Dashboard

A full-stack application for scraping and visualizing Facebook Ads Library data for Nike ads.

## Project Structure

```
adge.ai/
├── scraper/          # Python scraper
│   ├── scraper.py    # Main scraper script
│   ├── assets/       # Downloaded ad assets (images/videos)
│   └── requirements.txt
├── server/           # Node.js TypeScript backend (API-only)
│   ├── src/
│   │   ├── config/   # Database configuration
│   │   ├── controllers/ # Request handlers
│   │   ├── middlewares/ # Validation and error handling
│   │   ├── routes/   # API route definitions
│   │   ├── services/ # Business logic
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

**Architecture**: The server and client are separate services. The server is a pure API (no UI serving), and the client is a standalone React application. They communicate via HTTP API calls.

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

Run the full stack (backend + frontend):

```bash
npm run fs-docker-run
```

Or manually:

```bash
docker-compose up -d --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001

**Note**: Make sure to set `DB_PASSWORD` environment variable for database connection:
```bash
export DB_PASSWORD=your_password
npm run fs-docker-run
```

## API Endpoints

All endpoints are under `/api`:

- `GET /api/health` - Health check endpoint
- `GET /api/ads` - Get all ads (with optional filters)
  - Query params: `status`, `platform`, `startDate`, `endDate`, `multipleVersions`
- `GET /api/ads/:adId` - Get specific ad by Library ID
- `GET /api/ads/stats/summary` - Get aggregated statistics
- `GET /api/ads/assets/:type/:filename` - Serve asset files (images/videos)

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

## NPM Scripts

### Development
- `npm run dev` - Start backend server in development mode
- `npm run client` - Start frontend in development mode
- `npm run scraper` - Run the Python scraper

### Docker
- `npm run fs-docker-run` - Build and start full stack (backend + frontend) in Docker
- `npm run docker:build` - Build Docker images
- `npm run docker:up` - Start containers
- `npm run docker:down` - Stop containers
- `npm run docker:logs` - View logs from all services
- `npm run docker:ps` - Show container status

## Technologies

- **Backend**: Node.js, Express, TypeScript, PostgreSQL
- **Frontend**: React, TypeScript, SCSS, Recharts
- **Scraper**: Python, Selenium, PostgreSQL
- **Docker**: Containerized deployment

## License

ISC
