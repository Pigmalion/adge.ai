import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { AdStats } from '../../types';
import './Charts.scss';

interface AdsOverTimeChartProps {
  stats: AdStats;
}

const AdsOverTimeChart: React.FC<AdsOverTimeChartProps> = ({ stats }) => {
  const data = stats.byDate.map((item) => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    count: item.count,
  })).reverse();

  return (
    <div className="chart-container">
      <h3>Ads Over Time</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="count"
            stroke="#1877f2"
            strokeWidth={2}
            name="Ads"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AdsOverTimeChart;


