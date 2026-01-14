import { Request, Response, NextFunction } from 'express';

export const validateAssetParams = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const { type, filename } = req.params;

  if (!type || (type !== 'images' && type !== 'videos')) {
    res.status(400).json({ error: 'Invalid asset type. Must be "images" or "videos"' });
    return;
  }

  if (!filename || filename.trim() === '') {
    res.status(400).json({ error: 'Filename is required' });
    return;
  }

  // Basic filename validation - prevent directory traversal
  if (filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
    res.status(400).json({ error: 'Invalid filename' });
    return;
  }

  next();
};

