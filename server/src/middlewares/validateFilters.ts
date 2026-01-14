import { Request, Response, NextFunction } from 'express';

export const validateFilters = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const { status, platform, startDate, endDate, multipleVersions } = req.query;

  // Validate status
  if (status && status !== 'active' && status !== 'inactive') {
    res.status(400).json({ error: 'Invalid status. Must be "active" or "inactive"' });
    return;
  }

  // Validate dates
  if (startDate && isNaN(Date.parse(startDate as string))) {
    res.status(400).json({ error: 'Invalid startDate format' });
    return;
  }

  if (endDate && isNaN(Date.parse(endDate as string))) {
    res.status(400).json({ error: 'Invalid endDate format' });
    return;
  }

  // Validate date range
  if (startDate && endDate && new Date(startDate as string) > new Date(endDate as string)) {
    res.status(400).json({ error: 'startDate must be before endDate' });
    return;
  }

  // Validate multipleVersions
  if (multipleVersions !== undefined && multipleVersions !== 'true' && multipleVersions !== 'false') {
    res.status(400).json({ error: 'multipleVersions must be "true" or "false"' });
    return;
  }

  next();
};

