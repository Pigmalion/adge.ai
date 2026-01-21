# Backend Server

Node.js/Express/TypeScript backend API for the Facebook Ads Library Dashboard.

## Overview

RESTful API server that provides endpoints for querying and managing scraped Facebook ads data stored in PostgreSQL.

## Architecture

- **Framework**: Express.js
- **Language**: TypeScript
- **Database**: PostgreSQL (via `pg` library)
- **Structure**: MVC pattern with controllers, services, routes, and middlewares

## Project Structure

```
server/
├── src/
│   ├── config/          # Database configuration
│   ├── controllers/     # Request handlers
│   ├── middlewares/     # Validation and error handling
│   ├── routes/          # API route definitions
│   ├── services/        # Business logic
│   ├── types/           # TypeScript type definitions
│   └── index.ts         # Application entry point
├── dist/                # Compiled JavaScript (generated)
├── Dockerfile           # Docker configuration
├── package.json
├── tsconfig.json
└── version.json         # Version information
```

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create a `.env` file in the `server/` directory with the following variables:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5433
DB_NAME=tempadsdb
DB_USER=app_user
DB_PASSWORD=your_password

# Server Configuration
PORT=3001
NODE_ENV=development
```

#### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DB_HOST` | PostgreSQL database host | Yes | `localhost` |
| `DB_PORT` | PostgreSQL database port | Yes | `5433` |
| `DB_NAME` | PostgreSQL database name | Yes | `tempadsdb` |
| `DB_USER` | PostgreSQL database user | Yes | `app_user` |
| `DB_PASSWORD` | PostgreSQL database password | Yes | - |
| `PORT` | Server port number | No | `3001` |
| `NODE_ENV` | Environment mode (`development` or `production`) | No | `development` |

**Note for Docker**: When running in Docker, set `DB_HOST=host.docker.internal` to connect to the host machine's PostgreSQL.

### 3. Build TypeScript

```bash
npm run build
```

## Running

### Development Mode

```bash
npm run dev
```

This runs the server with hot-reload using `ts-node-dev`.

### Production Mode

```bash
npm run build
npm start
```

## API Endpoints

### Health Check

- **GET** `/api/health`
  - Returns server status and timestamp

### Version

- **GET** `/` or `/version`
  - Returns version information from `version.json`

### Ads

- **GET** `/api/ads`
  - Get all ads with optional filters
  - Query parameters:
    - `status` - Filter by status (`active` or `inactive`)
    - `platform` - Filter by platform (e.g., `Facebook`, `Instagram`)
    - `startDate` - Filter ads starting from this date (YYYY-MM-DD)
    - `endDate` - Filter ads starting before this date (YYYY-MM-DD)
    - `multipleVersions` - Filter by multiple versions (`true` or `false`)
  - Example: `/api/ads?status=active&platform=Facebook`

- **GET** `/api/ads/:adId`
  - Get a specific ad by Library ID
  - Example: `/api/ads/3117478348437475`

- **GET** `/api/ads/stats/summary`
  - Get aggregated statistics
  - Returns: total ads, active/inactive counts, platform distribution, date distribution

- **GET** `/api/ads/assets/:type/:filename`
  - Serve ad asset files (images/videos)
  - Example: `/api/ads/assets/images/3117478348437475.jpg`

## Code Structure

### Controllers

Handle HTTP requests and responses:
- `adsController.ts` - Ad-related endpoints
- `versionController.ts` - Version endpoint

### Services

Business logic layer:
- `adsService.ts` - Database queries and data processing

### Routes

Route definitions with middlewares:
- `adsRoutes.ts` - Ad API routes

### Middlewares

Request validation and error handling:
- `validateFilters.ts` - Validates query parameters
- `validateAdId.ts` - Validates ad ID parameter
- `validateAssetParams.ts` - Validates asset request parameters
- `errorHandler.ts` - Global error handler

## Database Schema

The server expects a PostgreSQL database with an `ads` table:

```sql
CREATE TABLE ads (
    id SERIAL PRIMARY KEY,
    ad_id VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL,
    platforms TEXT[],
    start_date DATE,
    end_date DATE,
    asset_url TEXT,
    asset_type VARCHAR(50),
    asset_path TEXT,
    multiple_versions BOOLEAN DEFAULT FALSE,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Docker

The server can be run in Docker. See the root `docker-compose.yml` for configuration.

When running in Docker, ensure:
- Database is accessible from the container (use `host.docker.internal` for local DB)
- Asset files are mounted as a volume (see `docker-compose.yml`)

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running
- Check environment variables in `.env`
- Ensure database exists and user has proper permissions
- For Docker: Use `host.docker.internal` instead of `localhost` for `DB_HOST`

### Port Already in Use

- Change `PORT` in `.env` file
- Or stop the process using port 3001

### TypeScript Compilation Errors

- Run `npm run build` to see detailed errors
- Check `tsconfig.json` configuration

