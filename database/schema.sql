-- TradeSense AI Database Schema

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User Challenges table
CREATE TABLE user_challenges (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    plan_type ENUM('starter', 'pro', 'elite') NOT NULL,
    initial_balance DECIMAL(10,2) NOT NULL,
    current_balance DECIMAL(10,2) NOT NULL,
    status ENUM('active', 'completed', 'failed') DEFAULT 'active',
    daily_loss_limit DECIMAL(10,2) DEFAULT -500.00,
    total_loss_limit DECIMAL(10,2) DEFAULT -1000.00,
    profit_target DECIMAL(10,2) DEFAULT 1000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Trades table
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_challenge_id INTEGER NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    trade_type ENUM('buy', 'sell') NOT NULL,
    quantity INTEGER NOT NULL,
    entry_price DECIMAL(10,4) NOT NULL,
    exit_price DECIMAL(10,4),
    pnl DECIMAL(10,4),
    status ENUM('open', 'closed') DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_challenge_id) REFERENCES user_challenges(id)
);

-- Payments table
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    plan_type ENUM('starter', 'pro', 'elite') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'MAD',
    payment_method VARCHAR(50),
    transaction_id VARCHAR(255),
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Market data table
CREATE TABLE market_data (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    price DECIMAL(10,4) NOT NULL,
    change_percent DECIMAL(5,2),
    volume BIGINT,
    market VARCHAR(10) DEFAULT 'US',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_symbol_market (symbol, market)
);

-- Insert default admin user
INSERT INTO users (email, full_name, password_hash, role) VALUES 
('admin@tradesense.ai', 'Admin User', '$2b$12$LQv3c6iwE2z2W1Z4.xCE8.JBqj6xYKD.LeW1NZ4MYNNpNt9.mEp5y', 'admin');

-- Insert sample market data
INSERT INTO market_data (symbol, name, price, change_percent, volume, market) VALUES
('AAPL', 'Apple Inc.', 175.50, 1.25, 50000000, 'US'),
('MSFT', 'Microsoft Corp.', 407.50, 0.85, 35000000, 'US'),
('GOOGL', 'Alphabet Inc.', 145.20, -0.50, 25000000, 'US'),
('TSLA', 'Tesla Inc.', 248.50, 2.10, 75000000, 'US'),
('BTC-USD', 'Bitcoin USD', 43250.00, 3.25, 1, 'CRYPTO'),
('ETH-USD', 'Ethereum USD', 2650.00, 1.80, 1, 'CRYPTO'),
('IAM', 'IAM', 125.00, 0.50, 100000, 'MA'),
('ATW', 'Attijariwafa Bank', 89.25, -0.25, 75000, 'MA');