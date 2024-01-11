-- SQL script to recreate the database schema locally

CREATE DATABASE IF NOT EXISTS Arb;

USE Arb;

-- Create the Bookmakers table
CREATE TABLE Bookmakers (
    bookmaker_id INT PRIMARY KEY AUTO_INCREMENT,
    bookmaker_name VARCHAR(255) NOT NULL
);

-- Create the Sports table
CREATE TABLE Sports (
    sport_id INT PRIMARY KEY AUTO_INCREMENT,
    sport_name VARCHAR(255) NOT NULL
);

-- Create the Events table
CREATE TABLE Events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    sport_id INT NOT NULL,
    team_name1 VARCHAR(255) NOT NULL,
    team_name2 VARCHAR(255) NOT NULL,
    league_name VARCHAR(255),
    event_date DATETIME NOT NULL,
    found_in VARCHAR(255),
    FOREIGN KEY (sport_id) REFERENCES Sports (sport_id)
);

-- Create the Markets table
CREATE TABLE Markets (
    market_id INT PRIMARY KEY AUTO_INCREMENT,
    market_type VARCHAR(255) NOT NULL
);

-- Create the Odds table
CREATE TABLE Odds (
    odd_id INT PRIMARY KEY AUTO_INCREMENT,
    bookmaker_id INT NOT NULL,
    event_id INT NOT NULL,
    market_id INT NOT NULL,
    option_title VARCHAR(255) NOT NULL,
    odds_value DECIMAL(10, 2) NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (bookmaker_id) REFERENCES Bookmakers (bookmaker_id),
    FOREIGN KEY (event_id) REFERENCES Events (event_id),
    FOREIGN KEY (market_id) REFERENCES Markets (market_id)
);


-- Create the Arbitrage table
CREATE TABLE Arbitrage (
    arbitrage_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    market_id INT NOT NULL,
    arbitrage_percentage DECIMAL(5, 2) NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Events (event_id),
    FOREIGN KEY (market_id) REFERENCES Markets (market_id)
);

-- Create the Arbitrage_Outcomes table
-- Each row in the Arbitrage_Outcomes table represents a single outcome
-- within an arbitrage opportunity. The arbitrage_id foreign key links the 
-- outcomes to the corresponding arbitrage opportunity in the Arbitrage table.
-- This design allows us to handle arbitrage opportunities with any number of outcomes,
-- whether it's two, three, or more.
CREATE TABLE Arbitrage_Outcomes (
    outcome_id INT PRIMARY KEY AUTO_INCREMENT,
    arbitrage_id INT NOT NULL,
    bookmaker_id INT NOT NULL,
    outcome_title VARCHAR(255) NOT NULL,
    outcome_odds DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (arbitrage_id) REFERENCES Arbitrage (arbitrage_id),
    FOREIGN KEY (bookmaker_id) REFERENCES Bookmakers (bookmaker_id)
);

CREATE TABLE Urls (
    url_id INT PRIMARY KEY AUTO_INCREMENT,
    bookmaker_id INT NOT NULL,
    url VARCHAR(255) NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (bookmaker_id) REFERENCES Bookmakers (bookmaker_id)
);

