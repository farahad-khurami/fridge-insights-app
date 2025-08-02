CREATE DATABASE IF NOT EXISTS tastebuds CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tastebuds;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    google_id VARCHAR(255) UNIQUE,
    apple_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE allergies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user_allergies (
    user_id INT,
    allergy_id INT,
    PRIMARY KEY (user_id, allergy_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (allergy_id) REFERENCES allergies(id) ON DELETE CASCADE
);

CREATE TABLE preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user_preferences (
    user_id INT,
    preference_id INT,
    PRIMARY KEY (user_id, preference_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (preference_id) REFERENCES preferences(id) ON DELETE CASCADE
);

CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    image_url VARCHAR(512) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    photo_id INT,
    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_json JSON,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE SET NULL
);

INSERT IGNORE INTO allergies (name) VALUES
  ('milk'), ('eggs'), ('fish'), ('crustacean shellfish'),
  ('tree nuts'), ('peanuts'), ('wheat'), ('soybeans'), ('sesame');