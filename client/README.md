# Frontend Client

React/TypeScript frontend dashboard for visualizing Facebook Ads Library data.

## Overview

Modern React application built with TypeScript and SCSS, providing an interactive dashboard for viewing and filtering scraped Facebook ads.

## Architecture

- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: SCSS
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Build Tool**: Create React App

## Project Structure

```
client/
├── src/
│   ├── components/      # React components
│   │   ├── AdCard/      # Ad display card
│   │   ├── Charts/      # Chart components
│   │   ├── Filters/     # Filter controls
│   │   └── StatsCards/  # Statistics cards
│   ├── services/        # API service layer
│   ├── types/           # TypeScript type definitions
│   ├── App.tsx          # Main application component
│   └── index.tsx        # Application entry point
├── public/              # Static assets
├── build/               # Production build (generated)
├── Dockerfile           # Docker configuration
├── nginx.conf           # Nginx configuration for production
└── package.json
```

## Setup

### 1. Install Dependencies

```bash
npm install --legacy-peer-deps
```

**Note**: The `--legacy-peer-deps` flag is required due to TypeScript version conflicts with `react-scripts`.

### 2. Environment Variables (Optional)

Create a `.env` file in the `client/` directory if you need to customize the API URL:

```env
REACT_APP_API_URL=http://localhost:3001/api
```

By default, the app uses `/api` which works with the proxy configuration in `package.json`.

## Running

### Development Mode

```bash
npm start
```

Runs the app in development mode at http://localhost:3000

The page will reload if you make edits. You will also see any lint errors in the console.

### Production Build

```bash
npm run build
```

Builds the app for production to the `build` folder. The build is optimized and minified.

### Production with Docker

The client is containerized with Nginx. See the root `docker-compose.yml` for configuration.

## Features

### Dashboard Components

1. **Statistics Cards**
   - Total ads count
   - Active ads count
   - Inactive ads count
   - Multiple versions count

2. **Charts**
   - **Ads Over Time**: Line chart showing ad distribution by date
   - **Ads by Platform**: Bar chart showing platform distribution

3. **Filters**
   - Status filter (Active/Inactive)
   - Platform filter (Facebook/Instagram)
   - Date range filter (Start date from/to)
   - Multiple versions toggle

4. **Ad Grid**
   - Responsive grid layout
   - Ad cards with:
     - Ad ID (Library ID)
     - Status badge
     - Platforms
     - Start/End dates
     - Asset preview (image/video)
     - Multiple versions indicator

## API Integration

The frontend communicates with the backend API through the `services/api.ts` module.

### API Service

- `getAllAds(filters?)` - Fetch ads with optional filters
- `getAdById(adId)` - Fetch a specific ad
- `getStats()` - Fetch aggregated statistics
- `getAssetUrl(assetPath)` - Generate asset URL for images/videos

### API Base URL

- Development: Uses proxy to `http://localhost:3001` (configured in `package.json`)
- Production: Uses `/api` (handled by Nginx reverse proxy)

## Styling

- **SCSS Modules**: Component-specific styles
- **Responsive Design**: Mobile-friendly layout
- **Modern UI**: Clean, professional design inspired by Facebook's design system

## Components

### AdCard

Displays individual ad information with asset preview.

### StatsCards

Shows key statistics in card format.

### Charts

- `AdsOverTimeChart` - Line chart for temporal data
- `PlatformChart` - Bar chart for platform distribution

### Filters

Interactive filter controls with validation.

## Build Output

The production build creates:
- Optimized JavaScript bundle
- Minified CSS
- Source maps for debugging
- Static assets

## Docker

The client is served via Nginx in production. The Dockerfile uses a multi-stage build:
1. Build stage: Compiles React app
2. Production stage: Serves via Nginx

Nginx configuration:
- Serves static files
- Proxies `/api` requests to backend
- Handles client-side routing

## Troubleshooting

### Dependency Installation Issues

If `npm install` fails:
```bash
npm install --legacy-peer-deps
```

### API Connection Issues

- Verify backend is running on port 3001
- Check browser console for CORS errors
- Ensure proxy is configured in `package.json`

### Build Errors

- Clear `node_modules` and reinstall
- Check TypeScript errors: `npm run build`
- Verify all environment variables are set

### Asset Loading Issues

- Check asset paths in database
- Verify backend asset serving endpoint
- Check browser network tab for 404 errors

