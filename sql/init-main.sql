-- Main database
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Basic index
CREATE INDEX idx_users_user_id ON users(user_id);
CREATE INDEX idx_users_city ON users(city);

-- Stats view
CREATE VIEW user_stats AS 
SELECT 
    COUNT(*) as total_users,
    COUNT(DISTINCT city) as total_cities,
    AVG(age) as avg_age
FROM users;
