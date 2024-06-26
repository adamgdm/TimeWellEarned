CREATE DATABASE IF NOT EXISTS DB;

USE DB;

CREATE TABLE IF NOT EXISTS TASKS (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NAME VARCHAR(255) NOT NULL,
    DESCRIPTION TEXT,
    STATUS ENUM('TODO', 'IN_PROGRESS', 'DONE', 'FORGIVEN') DEFAULT 'TODO',
    REWARD ENUM('NOT_YET', 'RECEIVED') DEFAULT 'NOT_YET',
    UPLOADED_FILE_OF_COMPLETION BLOB,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS SCREEN_TIME (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    TIME INT NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS USED_SCREEN_TIME (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    TIME INT NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS SANCTIONS (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NAME VARCHAR(255) NOT NULL,
    DESCRIPTION TEXT,
    `FROM` DATE,
    `TO` DATE,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);