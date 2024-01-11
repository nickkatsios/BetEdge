from enum import Enum

class Bookmaker(Enum):
    """Bookmaker Enum for uniform reference to bookmaker names.
    Enum standardized for all scrappers

    Every company we plan on betting should be inserted in the Company Enum

    Usage:
        e.g Bookmaker.STOIXIMAN.value corresponds to "stoiximan"
    """
    STOIXIMAN = "stoiximan"
    NOVIBET = "novibet"
    BETSHOP = "betshop"
    BETSSON = "betsson"

class Sport(Enum):
    """Sport Enum for uniform reference to sport names.

    Every sport we plan on including in the arb
    should be inserted in the Sport Enum

    Usage:
        e.g Sport.FOOTBALL.value corresponds to "football"
    """
    FOOTBALL = 1
    BASKETBALL = 2
    TENNIS = 3

# bookmaker ids for db
bookmaker_ids = {
    "novibet": 1,
    "stoiximan": 2,
    "betshop": 3,
    "betsson": 4,
    # Add more bookmakers here
}

asci_art = """
            #  ██████╗ ███████╗████████╗███████╗██████╗  ██████╗ ███████╗
            #  ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝ ██╔════╝
            #  ██████╔╝█████╗     ██║   █████╗  ██║  ██║██║  ███╗█████╗  
            #  ██╔══██╗██╔══╝     ██║   ██╔══╝  ██║  ██║██║   ██║██╔══╝  
            #  ██████╔╝███████╗   ██║   ███████╗██████╔╝╚██████╔╝███████╗
            #  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═════╝  ╚═════╝ ╚══════╝
            #                                                            
            """

