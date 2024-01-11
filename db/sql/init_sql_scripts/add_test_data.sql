USE Arb

-- Insert two sample rows into the Bookmakers table
INSERT INTO Bookmakers (bookmaker_name)
VALUES
    ('Novibet'),
    ('Stoiximan'),
    ('Betshop'),
    ('Betsson');

-- Insert two sample rows into the Markets table
INSERT INTO Markets (market_type)
VALUES
    ('Match Winner'),
    ('Over/Under');

-- Insert two sample rows into the Sports table
INSERT INTO Sports (sport_name)
VALUES
    ('Football'),
    ('Basketball');

INSERT INTO Urls (bookmaker_id, url, timestamp) VALUES 
(1, 'https://www.novibet.gr/en/sports/matches/ofi-asteras-tripolis/e33028656', '2023-12-17 12:34:56'), 
(2, 'https://en.stoiximan.gr/match-odds/ofi-crete-asteras-tripolis/42192282/', '2023-12-17 12:34:56'), 
(3, 'https://www.betshop.gr/sports/sportevent/stoixima-podosfairo/spain-laliga/villarreal-real-sociedad/5748674', '2023-12-17 12:34:56'), 
(4, 'https://www.betsson.gr/en/sportsbook/football/greece/greece-super-league-1', '2023-12-17 12:34:56');