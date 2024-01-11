USE Arb

-- SQL script to delete everything in the DB 
-- Commands are ordered to avoid foreign key constraints

-- Drop Urls table
-- !! TO BE DONE FIRST !!
DROP TABLE IF EXISTS Urls;

-- Drop the Arbitrage_Outcomes table (if it exists)
DROP TABLE IF EXISTS Arbitrage_Outcomes;

-- Drop the Odds table (if it exists)
DROP TABLE IF EXISTS Odds;

-- Drop the Arbitrage table (if it exists)
DROP TABLE IF EXISTS Arbitrage;

-- Drop the Bookmakers table (if it exists)
DROP TABLE IF EXISTS Bookmakers;

-- Drop the Events table (if it exists)
DROP TABLE IF EXISTS Events;

-- Drop the Markets table (if it exists)
DROP TABLE IF EXISTS Markets;

-- Drop the Sports table (if it exists)
DROP TABLE IF EXISTS Sports;
