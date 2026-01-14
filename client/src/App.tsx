import React, { useState, useEffect } from 'react';
import { Ad, AdStats, AdFilters } from './types';
import { adsApi } from './services/api';
import StatsCards from './components/StatsCards/StatsCards';
import Filters from './components/Filters/Filters';
import AdsOverTimeChart from './components/Charts/AdsOverTimeChart';
import PlatformChart from './components/Charts/PlatformChart';
import AdCard from './components/AdCard/AdCard';
import './App.scss';

const App: React.FC = () => {
  const [ads, setAds] = useState<Ad[]>([]);
  const [stats, setStats] = useState<AdStats | null>(null);
  const [filters, setFilters] = useState<AdFilters>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, [filters]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [adsData, statsData] = await Promise.all([
        adsApi.getAllAds(filters),
        adsApi.getStats(),
      ]);

      setAds(adsData);
      setStats(statsData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch data';
      setError(errorMessage);
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const availablePlatforms = stats
    ? Object.keys(stats.byPlatform)
    : [];

  if (loading && !stats) {
    return (
      <div className="app">
        <div className="container">
          <div className="loading">Loading dashboard...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="container">
          <div className="error">
            <h2>Error</h2>
            <p>{error}</p>
            <button onClick={fetchData}>Retry</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="container">
        <header>
          <h1>📊 Facebook Ads Library Dashboard - Nike</h1>
          <button className="refresh-button" onClick={fetchData}>
            Refresh
          </button>
        </header>

        {stats && (
          <>
            <StatsCards stats={stats} />

            <div className="charts-grid">
              <AdsOverTimeChart stats={stats} />
              <PlatformChart stats={stats} />
            </div>
          </>
        )}

        <Filters
          filters={filters}
          onFiltersChange={setFilters}
          availablePlatforms={availablePlatforms}
        />

        <div className="ads-section">
          <h2>Ads ({ads.length})</h2>
          {ads.length === 0 ? (
            <div className="empty-state">
              <p>No ads found matching the current filters.</p>
            </div>
          ) : (
            <div className="ads-grid">
              {ads.map((ad) => (
                <AdCard key={ad.id} ad={ad} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
