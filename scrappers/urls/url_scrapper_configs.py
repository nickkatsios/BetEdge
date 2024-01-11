from scrappers.configs.general_scrapper_configs import Bookmaker, Sport


# The league list urls to extract each individual league url
base_urls = {
    Bookmaker.NOVIBET.value : { 
        Sport.FOOTBALL.value: "https://www.novibet.gr/en/sports/podosfairo/4372606",
        Sport.BASKETBALL.value: None,
        Sport.TENNIS.value : None
    },
    Bookmaker.BETSHOP.value : { 
        Sport.FOOTBALL.value: "https://www.betshop.gr/sports/game/stoixima-podosfairo/1",
        Sport.BASKETBALL.value: None,
        Sport.TENNIS.value : None
    },
    Bookmaker.STOIXIMAN.value : { 
        Sport.FOOTBALL.value: "https://en.stoiximan.gr/sport/soccer/",
        Sport.BASKETBALL.value: None,
        Sport.TENNIS.value : None
    },
    Bookmaker.BETSSON.value : {
        Sport.FOOTBALL.value: "https://www.betsson.gr/en/sportsbook",
        Sport.BASKETBALL.value: None,
        Sport.TENNIS.value : None
    },
}