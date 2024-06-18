CREATE TABLE IF NOT EXISTS userdata (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        date_of_birth DATE NOT NULL,
                        phone_number TEXT,
                        address TEXT,
                        city TEXT,
                        country TEXT,
                        postal_code TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );