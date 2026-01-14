import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import adsRoutes from './routes/adsRoutes';
import { errorHandler } from './middlewares/errorHandler';
import { getVersion } from './controllers/versionController';
import path from 'path';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Version endpoints
app.get('/', getVersion);
app.get('/version', getVersion);

// API Routes
app.use('/api/ads', adsRoutes);

// Error handling middleware (must be last)
app.use(errorHandler);

// Serve React app in production
if (process.env.NODE_ENV === 'production') {
  const clientBuildPath = path.join(__dirname, '../../client/build');
  app.use(express.static(clientBuildPath));

  app.get('*', (req: Request, res: Response) => {
    res.sendFile(path.join(clientBuildPath, 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📊 API available at http://localhost:${PORT}/api/ads`);
});


