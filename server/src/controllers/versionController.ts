import { Request, Response } from 'express';
import fs from 'fs';
import path from 'path';

export const getVersion = (req: Request, res: Response): void => {
  try {
    // Read version from version.json
    const versionPath = path.join(__dirname, '../../version.json');
    const versionData = JSON.parse(fs.readFileSync(versionPath, 'utf-8'));
    
    res.json(versionData);
  } catch (error) {
    console.error('Error reading version:', error);
    // Fallback to package.json if version.json doesn't exist
    try {
      const packagePath = path.join(__dirname, '../../package.json');
      const packageData = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));
      res.json({
        version: packageData.version,
        name: packageData.name,
        description: packageData.description,
      });
    } catch (fallbackError) {
      res.status(500).json({ error: 'Failed to read version information' });
    }
  }
};
