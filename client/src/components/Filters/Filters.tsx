import React from 'react';
import { AdFilters } from '../../types';
import './Filters.scss';

interface FiltersProps {
  filters: AdFilters;
  onFiltersChange: (filters: AdFilters) => void;
  availablePlatforms: string[];
}

const Filters: React.FC<FiltersProps> = ({ filters, onFiltersChange, availablePlatforms }) => {
  const handleChange = (key: keyof AdFilters, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value || undefined,
    });
  };

  return (
    <div className="filters">
      <h3>Filters</h3>
      <div className="filters-grid">
        <div className="filter-group">
          <label>Status</label>
          <select
            value={filters.status || ''}
            onChange={(e) => handleChange('status', e.target.value || undefined)}
          >
            <option value="">All</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Platform</label>
          <select
            value={filters.platform || ''}
            onChange={(e) => handleChange('platform', e.target.value || undefined)}
          >
            <option value="">All Platforms</option>
            {availablePlatforms.map((platform) => (
              <option key={platform} value={platform}>
                {platform}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Start Date From</label>
          <input
            type="date"
            value={filters.startDate || ''}
            onChange={(e) => handleChange('startDate', e.target.value || undefined)}
          />
        </div>

        <div className="filter-group">
          <label>Start Date To</label>
          <input
            type="date"
            value={filters.endDate || ''}
            onChange={(e) => handleChange('endDate', e.target.value || undefined)}
          />
        </div>

        <div className="filter-group">
          <label>
            <input
              type="checkbox"
              checked={filters.multipleVersions || false}
              onChange={(e) => handleChange('multipleVersions', e.target.checked || undefined)}
            />
            Multiple Versions Only
          </label>
        </div>

        <div className="filter-group">
          <button
            className="clear-filters"
            onClick={() => onFiltersChange({})}
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default Filters;


