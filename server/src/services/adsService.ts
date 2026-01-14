import pool from '../config/database';
import { Ad, AdStats, AdFilters } from '../types';

export class AdsService {
  async getAllAds(filters?: AdFilters): Promise<Ad[]> {
    let query = 'SELECT * FROM ads WHERE 1=1';
    const params: any[] = [];
    let paramIndex = 1;

    if (filters?.status) {
      query += ` AND status = $${paramIndex}`;
      params.push(filters.status);
      paramIndex++;
    }

    if (filters?.platform) {
      query += ` AND $${paramIndex} = ANY(platforms)`;
      params.push(filters.platform);
      paramIndex++;
    }

    if (filters?.startDate) {
      query += ` AND start_date >= $${paramIndex}`;
      params.push(filters.startDate);
      paramIndex++;
    }

    if (filters?.endDate) {
      query += ` AND start_date <= $${paramIndex}`;
      params.push(filters.endDate);
      paramIndex++;
    }

    if (filters?.multipleVersions !== undefined) {
      query += ` AND multiple_versions = $${paramIndex}`;
      params.push(filters.multipleVersions);
      paramIndex++;
    }

    query += ' ORDER BY start_date DESC NULLS LAST, scraped_at DESC';

    const result = await pool.query(query, params);
    return result.rows.map(this.mapRowToAd);
  }

  async getAdById(adId: string): Promise<Ad | null> {
    const result = await pool.query('SELECT * FROM ads WHERE ad_id = $1', [adId]);
    if (result.rows.length === 0) {
      return null;
    }
    return this.mapRowToAd(result.rows[0]);
  }

  async getStats(): Promise<AdStats> {
    const totalResult = await pool.query('SELECT COUNT(*) as count FROM ads');
    const total = parseInt(totalResult.rows[0].count);

    const activeResult = await pool.query("SELECT COUNT(*) as count FROM ads WHERE status = 'active'");
    const active = parseInt(activeResult.rows[0].count);

    const inactiveResult = await pool.query("SELECT COUNT(*) as count FROM ads WHERE status = 'inactive'");
    const inactive = parseInt(inactiveResult.rows[0].count);

    const multipleVersionsResult = await pool.query('SELECT COUNT(*) as count FROM ads WHERE multiple_versions = true');
    const withMultipleVersions = parseInt(multipleVersionsResult.rows[0].count);

    // Get platform counts
    const platformResult = await pool.query(`
      SELECT platform, COUNT(*) as count
      FROM (
        SELECT unnest(platforms) as platform
        FROM ads
      ) platforms
      GROUP BY platform
      ORDER BY count DESC
    `);

    const byPlatform: Record<string, number> = {};
    platformResult.rows.forEach((row: any) => {
      byPlatform[row.platform] = parseInt(row.count);
    });

    // Get ads by date
    const dateResult = await pool.query(`
      SELECT start_date::text as date, COUNT(*) as count
      FROM ads
      WHERE start_date IS NOT NULL
      GROUP BY start_date
      ORDER BY start_date DESC
      LIMIT 30
    `);

    const byDate = dateResult.rows.map((row: any) => ({
      date: row.date,
      count: parseInt(row.count),
    }));

    return {
      total,
      active,
      inactive,
      byPlatform,
      byDate,
      withMultipleVersions,
    };
  }

  private mapRowToAd(row: any): Ad {
    return {
      id: row.id,
      ad_id: row.ad_id,
      status: row.status,
      platforms: row.platforms || [],
      start_date: row.start_date ? row.start_date.toISOString().split('T')[0] : null,
      end_date: row.end_date ? row.end_date.toISOString().split('T')[0] : null,
      asset_url: row.asset_url,
      asset_type: row.asset_type,
      asset_path: row.asset_path,
      multiple_versions: row.multiple_versions || false,
      scraped_at: row.scraped_at.toISOString(),
      created_at: row.created_at.toISOString(),
      updated_at: row.updated_at.toISOString(),
    };
  }
}

export default new AdsService();


