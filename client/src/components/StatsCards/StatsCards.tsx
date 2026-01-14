import React from 'react';
import { AdStats } from '../../types';
import './StatsCards.scss';

interface StatsCardsProps {
  stats: AdStats;
}

const StatsCards: React.FC<StatsCardsProps> = ({ stats }) => {
  return (
    <div className="stats-cards">
      <div className="stat-card">
        <div className="stat-label">Total Ads</div>
        <div className="stat-value">{stats.total}</div>
      </div>
      <div className="stat-card active">
        <div className="stat-label">Active</div>
        <div className="stat-value">{stats.active}</div>
      </div>
      <div className="stat-card inactive">
        <div className="stat-label">Inactive</div>
        <div className="stat-value">{stats.inactive}</div>
      </div>
      <div className="stat-card">
        <div className="stat-label">Multiple Versions</div>
        <div className="stat-value">{stats.withMultipleVersions}</div>
      </div>
    </div>
  );
};

export default StatsCards;


