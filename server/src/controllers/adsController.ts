import { Request, Response } from 'express';
import adsService from '../services/adsService';
import { AdFilters } from '../types';

export const getAllAds = async (req: Request, res: Response): Promise<void> => {
  try {
    const filters: AdFilters = {};

    if (req.query.status) {
      filters.status = req.query.status as 'active' | 'inactive';
    }

    if (req.query.platform) {
      filters.platform = req.query.platform as string;
    }

    if (req.query.startDate) {
      filters.startDate = req.query.startDate as string;
    }

    if (req.query.endDate) {
      filters.endDate = req.query.endDate as string;
    }

    if (req.query.multipleVersions !== undefined) {
      filters.multipleVersions = req.query.multipleVersions === 'true';
    }

    const ads = await adsService.getAllAds(filters);
    res.json({ ads });
  } catch (error) {
    console.error('Error fetching ads:', error);
    res.status(500).json({ error: 'Failed to fetch ads' });
  }
};

export const getAdById = async (req: Request, res: Response): Promise<void> => {
  try {
    const { adId } = req.params;
    const ad = await adsService.getAdById(adId);
    
    if (!ad) {
      res.status(404).json({ error: 'Ad not found' });
      return;
    }
    
    res.json({ ad });
  } catch (error) {
    console.error('Error fetching ad:', error);
    res.status(500).json({ error: 'Failed to fetch ad' });
  }
};

export const getStats = async (req: Request, res: Response): Promise<void> => {
  try {
    const stats = await adsService.getStats();
    res.json(stats);
  } catch (error) {
    console.error('Error fetching stats:', error);
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
};

import path from 'path';
import fs from 'fs';

export const serveAsset = (req: Request, res: Response): void => {
  try {
    const { type, filename } = req.params;
    
    // Path calculation:
    // - In development: __dirname is server/dist/controllers, go up 3 levels to project root
    // - In Docker: assets are mounted at /app/scraper/assets (WORKDIR is /app)
    // Try multiple path strategies for compatibility
    let assetsDir: string;
    
    // Strategy 1: From __dirname (works when compiled)
    // __dirname in compiled code: server/dist/controllers
    // Go up 3 levels: server/dist/controllers -> server/dist -> server -> project root
    const fromDist = path.join(__dirname, '../../../scraper/assets');
    
    // Strategy 2: From process.cwd() (works in Docker where cwd is /app)
    const fromCwd = path.join(process.cwd(), 'scraper', 'assets');
    
    // Strategy 3: Absolute path for Docker (assets mounted at /app/scraper/assets)
    const dockerPath = '/app/scraper/assets';
    
    // Use the first path that exists, or default to fromCwd
    if (fs.existsSync(fromDist)) {
      assetsDir = fromDist;
    } else if (fs.existsSync(fromCwd)) {
      assetsDir = fromCwd;
    } else if (fs.existsSync(dockerPath)) {
      assetsDir = dockerPath;
    } else {
      assetsDir = fromCwd; // Default fallback
    }
    
    const filePath = path.join(assetsDir, type, filename);

    // Security check - ensure file is within assets directory (resolve to absolute path)
    const resolvedAssetsDir = path.resolve(assetsDir);
    const resolvedFilePath = path.resolve(filePath);
    
    if (!resolvedFilePath.startsWith(resolvedAssetsDir)) {
      res.status(403).json({ error: 'Access denied' });
      return;
    }

    if (!fs.existsSync(filePath)) {
      console.error(`Asset not found: ${filePath}`);
      console.error(`Assets dir: ${assetsDir} (resolved: ${resolvedAssetsDir})`);
      res.status(404).json({ error: 'Asset not found' });
      return;
    }

    res.sendFile(filePath);
  } catch (error) {
    console.error('Error serving asset:', error);
    res.status(500).json({ error: 'Failed to serve asset' });
  }
};

