CREATE TABLE IF NOT EXISTS simrs_web_audit_trail (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  module VARCHAR(50) NOT NULL,
  action VARCHAR(50) NOT NULL,
  entity_name VARCHAR(100) NOT NULL,
  entity_id VARCHAR(100) NOT NULL,
  actor_id VARCHAR(50) NOT NULL,
  actor_name VARCHAR(100) NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  before_payload JSON,
  after_payload JSON,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
