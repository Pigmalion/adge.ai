export interface Ad {
  id: number;
  ad_id: string;
  status: 'active' | 'inactive' | 'unknown';
  platforms: string[];
  start_date: string | null;
  end_date: string | null;
  asset_url: string | null;
  asset_type: 'image' | 'video' | null;
  asset_path: string | null;
  multiple_versions: boolean;
  scraped_at: string;
  created_at: string;
  updated_at: string;
}

export interface AdStats {
  total: number;
  active: number;
  inactive: number;
  byPlatform: Record<string, number>;
  byDate: Array<{ date: string; count: number }>;
  withMultipleVersions: number;
}

export interface AdFilters {
  status?: 'active' | 'inactive';
  platform?: string;
  startDate?: string;
  endDate?: string;
  multipleVersions?: boolean;
}


