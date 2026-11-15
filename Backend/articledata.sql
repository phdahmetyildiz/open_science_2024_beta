-- This file is being archived on 15.11.2026 and is not part of the new version.
CREATE TABLE IF NOT EXISTS articledata (
                        article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        article_name TEXT NOT NULL,
                        description TEXT,
                        author_id INTEGER NOT NULL,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        file_path TEXT NOT NULL,
                        file_size TEXT NOT NULL,
                        file_type TEXT NOT NULL,
                        is_approved BOOLEAN DEFAULT 0
                    );