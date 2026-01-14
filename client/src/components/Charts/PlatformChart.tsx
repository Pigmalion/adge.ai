import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { AdStats } from '../../types';
import './Charts.scss';

interface PlatformChartProps {
  stats: AdStats;
}

const PlatformChart: React.FC<PlatformChartProps> = ({ stats }) => {
  const data = Object.entries(stats.byPlatform).map(([platform, count]) => ({
    platform,
    count,
  }));

  return (
    <div className="chart-container">
      <h3>Ads by Platform</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="platform" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#1877f2" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PlatformChart;


