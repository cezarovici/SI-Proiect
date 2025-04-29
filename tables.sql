-- USE encryption_db;

-- Tabela Algorithms
CREATE TABLE algorithms (
    algorithm_id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    type ENUM('symmetric', 'asymmetric') NOT NULL,
    parameters TEXT
);

-- Tabela Keys
CREATE TABLE keys (
    key_id INT AUTO_INCREMENT PRIMARY KEY,
    algorithm_id INT NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    key_value TEXT,
    public_key TEXT,
    private_key TEXT,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiration_date DATETIME,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(algorithm_id)
);

-- Tabela Files
CREATE TABLE files (
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    original_path VARCHAR(255) NOT NULL,
    encrypted_path VARCHAR(255) NOT NULL,
    hash VARCHAR(64) NOT NULL,
    algorithm_id INT NOT NULL,
    key_id INT NOT NULL,
    encryption_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(algorithm_id),
    FOREIGN KEY (key_id) REFERENCES keys(key_id)
);

-- Tabela Performance
CREATE TABLE performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    file_id INT NOT NULL,
    algorithm_id INT NOT NULL,
    key_id INT NOT NULL,
    operation_type ENUM('encrypt', 'decrypt') NOT NULL,
    execution_time FLOAT NOT NULL,
    memory_usage FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(file_id),
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(algorithm_id),
    FOREIGN KEY (key_id) REFERENCES keys(key_id)
);