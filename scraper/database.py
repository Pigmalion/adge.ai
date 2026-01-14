"""
Database connection and schema setup for ads storage.
"""

import psycopg2
import os
from typing import Optional
from psycopg2.extras import RealDictCursor


class Database:
    """PostgreSQL database connection and operations."""
    
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_schema()
    
    def connect(self):
        """Connect to PostgreSQL database using environment variables."""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'tempAdsDB'),
                user=os.getenv('DB_USER', 'app_user'),
                password=os.getenv('DB_PASSWORD', '')
            )
            print("✓ Connected to PostgreSQL database")
        except Exception as e:
            print(f"✗ Error connecting to database: {e}")
            raise
    
    def create_schema(self):
        """Create the ads table if it doesn't exist."""
        cursor = self.conn.cursor()
        
        try:
            # Check if table already exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'ads'
                )
            """)
            table_exists = cursor.fetchone()[0]
            
            if table_exists:
                print("✓ Ads table already exists, skipping creation")
            else:
                # Try to create table
                try:
                    cursor.execute("""
                        CREATE TABLE ads (
                            id SERIAL PRIMARY KEY,
                            ad_id VARCHAR(255) UNIQUE NOT NULL,
                            status VARCHAR(50) NOT NULL,
                            platforms TEXT[],
                            start_date DATE,
                            end_date DATE,
                            asset_url TEXT,
                            asset_type VARCHAR(50),
                            asset_path TEXT,
                            multiple_versions BOOLEAN DEFAULT FALSE,
                            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    
                    # Create indexes
                    cursor.execute("""
                        CREATE INDEX idx_ad_id ON ads(ad_id)
                    """)
                    cursor.execute("""
                        CREATE INDEX idx_status ON ads(status)
                    """)
                    cursor.execute("""
                        CREATE INDEX idx_start_date ON ads(start_date)
                    """)
                    cursor.execute("""
                        CREATE INDEX idx_platforms ON ads USING GIN(platforms)
                    """)
                    
                    self.conn.commit()
                    print("✓ Database schema created")
                except Exception as create_error:
                    print(f"⚠️  Could not create table: {create_error}")
                    print("   The table needs to be created manually as postgres user.")
                    self.conn.rollback()
                    raise Exception("Table does not exist and could not be created. Please create it manually.")
            
            # Verify table exists and is accessible
            cursor.execute("SELECT COUNT(*) FROM ads")
            count = cursor.fetchone()[0]
            print(f"✓ Database schema verified (current ads: {count})")
            
        except Exception as e:
            print(f"✗ Error with schema: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()
    
    def insert_ad(self, ad_data: dict) -> Optional[int]:
        """Insert or update an ad in the database."""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO ads (ad_id, status, platforms, start_date, end_date, asset_url, asset_type, asset_path, multiple_versions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ad_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    platforms = EXCLUDED.platforms,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date,
                    asset_url = EXCLUDED.asset_url,
                    asset_type = EXCLUDED.asset_type,
                    asset_path = EXCLUDED.asset_path,
                    multiple_versions = EXCLUDED.multiple_versions,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """, (
                ad_data.get('ad_id'),
                ad_data.get('status', 'unknown'),
                ad_data.get('platforms', []),
                ad_data.get('start_date'),
                ad_data.get('end_date'),
                ad_data.get('asset_url'),
                ad_data.get('asset_type', 'image'),
                ad_data.get('asset_path'),
                ad_data.get('multiple_versions', False)
            ))
            
            result = cursor.fetchone()
            self.conn.commit()
            return result[0] if result else None
        except Exception as e:
            print(f"✗ Error inserting ad {ad_data.get('ad_id')}: {e}")
            self.conn.rollback()
            return None
        finally:
            cursor.close()
    
    def get_all_ads(self) -> list:
        """Get all ads from the database."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT * FROM ads 
                ORDER BY scraped_at DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"✗ Error fetching ads: {e}")
            return []
        finally:
            cursor.close()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")

