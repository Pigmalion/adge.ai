import { Router } from 'express';
import { getVersion } from '../controllers/versionController';

const router = Router();

// GET /version - Get version information
router.get('/', getVersion);

export default router;

