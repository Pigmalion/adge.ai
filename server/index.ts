import express, { Request, Response } from 'express';
import fs from 'fs';
import path from 'path';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3001;
const FINDINGS_DIR = path.join(__dirname, '..', 'findings');

interface Finding {
  filename: string;
  timestamp: string;
  url: string;
  data: any;
}

interface FindingsResponse {
  findings: Finding[];
}

// Middleware
app.use(cors());
app.use(express.json());

// Ensure findings directory exists
if (!fs.existsSync(FINDINGS_DIR)) {
  fs.mkdirSync(FINDINGS_DIR, { recursive: true });
}

// API Routes

// Get all findings
app.get('/api/findings', (req: Request, res: Response) => {
  try {
    const files = fs.readdirSync(FINDINGS_DIR)
      .filter(file => file.endsWith('.json'))
      .sort()
      .reverse(); // Most recent first

    const findings: Finding[] = files.map(filename => {
      const filepath = path.join(FINDINGS_DIR, filename);
      const content = fs.readFileSync(filepath, 'utf-8');
      const data = JSON.parse(content);
      return {
        filename,
        ...data
      };
    });

    const response: FindingsResponse = { findings };
    res.json(response);
  } catch (error) {
    console.error('Error reading findings:', error);
    res.status(500).json({ error: 'Failed to read findings' });
  }
});

// Get a specific finding by filename
app.get('/api/findings/:filename', (req: Request, res: Response) => {
  try {
    const filename = req.params.filename;
    const filepath = path.join(FINDINGS_DIR, filename);

    if (!fs.existsSync(filepath)) {
      return res.status(404).json({ error: 'Finding not found' });
    }

    const content = fs.readFileSync(filepath, 'utf-8');
    const data = JSON.parse(content);

    res.json(data);
  } catch (error) {
    console.error('Error reading finding:', error);
    res.status(500).json({ error: 'Failed to read finding' });
  }
});

// Health check
app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Serve React app in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, '../client/build')));
  
  app.get('*', (req: Request, res: Response) => {
    res.sendFile(path.join(__dirname, '../client/build/index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

