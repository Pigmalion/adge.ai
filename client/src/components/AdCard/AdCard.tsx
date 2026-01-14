import React from 'react';
import { Ad } from '../../types';
import { adsApi } from '../../services/api';
import './AdCard.scss';

interface AdCardProps {
  ad: Ad;
}

const AdCard: React.FC<AdCardProps> = ({ ad }) => {
  const assetUrl = adsApi.getAssetUrl(ad.asset_path);
  const statusClass = ad.status === 'active' ? 'active' : 'inactive';

  return (
    <div className="ad-card">
      <div className="ad-header">
        <div className="ad-id">Library ID: {ad.ad_id}</div>
        <span className={`ad-status ${statusClass}`}>{ad.status}</span>
        {ad.multiple_versions && (
          <div className="multiple-versions-badge">🔀 Multiple Versions</div>
        )}
      </div>

      <div className="ad-info">
        <div className="ad-platforms">
          <strong>Platforms:</strong> {ad.platforms.join(', ')}
        </div>
        <div className="ad-dates">
          {ad.start_date && (
            <span>Started: {new Date(ad.start_date).toLocaleDateString()}</span>
          )}
          {ad.end_date && (
            <span> | Ended: {new Date(ad.end_date).toLocaleDateString()}</span>
          )}
          {!ad.start_date && !ad.end_date && <span>Date: Unknown</span>}
        </div>
      </div>

      {assetUrl && (
        <div className="ad-asset">
          {ad.asset_type === 'video' ? (
            <video controls src={assetUrl} />
          ) : (
            <img src={assetUrl} alt={`Ad ${ad.ad_id}`} />
          )}
        </div>
      )}

      {!assetUrl && (
        <div className="no-asset">No asset available</div>
      )}
    </div>
  );
};

export default AdCard;


