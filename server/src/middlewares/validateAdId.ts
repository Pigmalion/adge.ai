import { Request, Response, NextFunction } from 'express';

export const validateAdId = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const { adId } = req.params;

  if (!adId || adId.trim() === '') {
    res.status(400).json({ error: 'Ad ID is required' });
    return;
  }

  // Basic validation - ad ID should be alphanumeric
  if (!/^[a-zA-Z0-9]+$/.test(adId)) {
    res.status(400).json({ error: 'Invalid Ad ID format' });
    return;
  }

  next();
};

