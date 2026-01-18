-- TradeSense Prop Trading Platform Database Schema
-- Generated SQL schema with proper relationships and indexes

PRAGMA foreign_keys = ON;

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_superadmin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_users_created_at ON users(created_at);

-- User challenges table
CREATE TABLE user_challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_type VARCHAR(50) NOT NULL, -- 'starter', 'pro', 'elite'
    initial_balance DECIMAL(15, 2) NOT NULL,
    current_balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE', -- 'ACTIVE', 'PASSED', 'FAILED', 'COMPLETED'
    profit_target DECIMAL(15, 2) NOT NULL,
    max_daily_loss DECIMAL(15, 2) NOT NULL,
    max_total_loss DECIMAL(15, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for user_challenges table
CREATE INDEX idx_user_challenges_user_id ON user_challenges(user_id);
CREATE INDEX idx_user_challenges_status ON user_challenges(status);
CREATE INDEX idx_user_challenges_created_at ON user_challenges(created_at);
CREATE INDEX idx_user_challenges_user_status ON user_challenges(user_id, status);

-- Trades table
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    trade_type VARCHAR(10) NOT NULL, -- 'buy', 'sell'
    quantity DECIMAL(15, 8) NOT NULL,
    entry_price DECIMAL(15, 8) NOT NULL,
    exit_price DECIMAL(15, 8),
    profit_loss DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL DEFAULT 'open', -- 'open', 'closed'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (challenge_id) REFERENCES user_challenges(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for trades table
CREATE INDEX idx_trades_challenge_id ON trades(challenge_id);
CREATE INDEX idx_trades_user_id ON trades(user_id);
CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_trades_status ON trades(status);
CREATE INDEX idx_trades_created_at ON trades(created_at);
CREATE INDEX idx_trades_challenge_status ON trades(challenge_id, status);

-- Payments table
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    challenge_id INTEGER,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    payment_method VARCHAR(50) NOT NULL, -- 'paypal', 'cmi', 'crypto', 'mock'
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'completed', 'failed', 'refunded'
    transaction_id VARCHAR(100) UNIQUE,
    paypal_order_id VARCHAR(100), -- PayPal specific
    paypal_payer_id VARCHAR(100), -- PayPal specific
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES user_challenges(id) ON DELETE SET NULL
);

-- Indexes for payments table
CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_challenge_id ON payments(challenge_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_transaction_id ON payments(transaction_id);
CREATE INDEX idx_payments_created_at ON payments(created_at);

-- Admin settings table
CREATE TABLE admin_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(255) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- PayPal settings table (specific to PayPal integration)
CREATE TABLE paypal_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode VARCHAR(20) DEFAULT 'sandbox', -- 'sandbox' or 'live'
    client_id VARCHAR(200) NOT NULL,
    client_secret VARCHAR(200) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    updated_by INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes for admin_settings table
CREATE INDEX idx_admin_settings_key ON admin_settings(setting_key);
CREATE INDEX idx_admin_settings_updated_by ON admin_settings(updated_by);

-- Trigger to update updated_at timestamps
CREATE TRIGGER update_timestamp_users 
    AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_timestamp_user_challenges 
    AFTER UPDATE ON user_challenges
BEGIN
    UPDATE user_challenges SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_timestamp_trades 
    AFTER UPDATE ON trades
BEGIN
    UPDATE trades SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_timestamp_payments 
    AFTER UPDATE ON payments
BEGIN
    UPDATE payments SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_timestamp_admin_settings 
    AFTER UPDATE ON admin_settings
BEGIN
    UPDATE admin_settings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Sample data for initial setup
INSERT INTO users (email, full_name, password_hash, is_superadmin, is_active) VALUES
('admin@tradesense.ai', 'Administrator', '$2b$12$hashed_password_example', TRUE, TRUE);

-- Insert default admin settings
INSERT INTO admin_settings (setting_key, setting_value, description) VALUES
('platform_enabled', 'true', 'Enable/disable platform access'),
('maintenance_mode', 'false', 'Maintenance mode status'),
('registration_enabled', 'true', 'Allow new user registrations');

-- Insert PayPal default settings (these will be updated by admin)
INSERT INTO paypal_settings (mode, client_id, client_secret, is_active) VALUES
('sandbox', 'sandbox_client_id_placeholder', 'sandbox_secret_placeholder', FALSE);

COMMIT;