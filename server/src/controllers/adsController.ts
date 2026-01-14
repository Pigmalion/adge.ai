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
    
    // Path from server/dist to scraper/assets
    const assetsDir = path.join(__dirname, '../../../scraper/assets');
    const filePath = path.join(assetsDir, type, filename);

    // Security check - ensure file is within assets directory
    if (!filePath.startsWith(assetsDir)) {
      res.status(403).json({ error: 'Access denied' });
      return;
    }

    if (!fs.existsSync(filePath)) {
      res.status(404).json({ error: 'Asset not found' });
      return;
    }

    res.sendFile(filePath);
  } catch (error) {
    console.error('Error serving asset:', error);
    res.status(500).json({ error: 'Failed to serve asset' });
  }
};

