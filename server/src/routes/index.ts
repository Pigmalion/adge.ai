import { Router } from 'express';
import adsRoutes from './adsRoutes';
import healthRoutes from './healthRoutes';

const router = Router();

// API Routes
router.use('/health', healthRoutes);
router.use('/ads', adsRoutes);

export default router;

