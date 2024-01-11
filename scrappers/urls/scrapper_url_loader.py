class Scrapper_url_loader:
    """ Loads the urls from the db for a specific bookmaker
    """

    def __init__(self, db) -> None:
        self.db = db

    def load_urls(self, bookmaker_id):
        """ Loads the urls from the db for a specific bookmaker

        Returns:
            urls: A list containing the urls from the db
        """
        sql = "SELECT * FROM Urls WHERE bookmaker_id = %s"
        values = (bookmaker_id,)
        urls = self.db.execute_query(sql, values)
        urls = [url[2] for url in urls]
        return urls