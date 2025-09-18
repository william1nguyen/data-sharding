CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_users_user_id ON users(user_id);
CREATE INDEX idx_users_city ON users(city);

-- Sharding stats view
CREATE VIEW shard_stats AS
SELECT 
    COUNT(*) as total_users,
    MIN(user_id) as min_user_id,
    MAX(user_id) as max_user_id,
    COUNT(DISTINCT city) as total_cities
FROM users;