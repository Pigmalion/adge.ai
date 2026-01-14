import { Router } from 'express';
import * as adsController from '../controllers/adsController';
import { validateFilters } from '../middlewares/validateFilters';
import { validateAdId } from '../middlewares/validateAdId';
import { validateAssetParams } from '../middlewares/validateAssetParams';

const router = Router();

// Named routes with middlewares and controllers

// GET /api/ads - Get all ads with optional filters
router.get(
  '/',
  validateFilters,
  adsController.getAllAds
);

// GET /api/ads/stats/summary - Get statistics
router.get(
  '/stats/summary',
  adsController.getStats
);

// GET /api/ads/assets/:type/:filename - Serve asset files
router.get(
  '/assets/:type/:filename',
  validateAssetParams,
  adsController.serveAsset
);

// GET /api/ads/:adId - Get ad by ID
router.get(
  '/:adId',
  validateAdId,
  adsController.getAdById
);

export default router;
