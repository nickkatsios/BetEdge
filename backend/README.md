# BetEdge-Backend
## The backend and APIs of the BetEdge project.

### Getting Started
1. Clone the repository
```bash
git clone https://github.com/nickkatsios/BetEdge-Backend.git
```
2. Create and activate the virtual environment
```bash
python -m venv myenv
source myenv/bin/activate
```
3. Install the dependencies
````bash
pip install -r requirements.txt
````
## Database Setup
Assuming you already have set up the Mysql db needed for the scrappers, you need to migrate the models to the db.
```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the server
```bash
python manage.py runserver
```
### API Endpoints
- / - Django admin panel
- /bookmakers - List of currently integrated bookmakers
- /bookmaker/<int:primary-key> - Details of an individual bookmaker
- /events - List of currently scrapped events
- /event/<int:primary-key> - Details of an individual event
- /markets - List of currently scrapped markets
- /market/<int:pk> - Details of an individual market
- /arbitrage - List of currently calculated and stored arbitrage opportunities

### Finding Arbitrage Opportunities
To manually find and calculate arbitrage opportunities and store them in the db, run the following command:
```bash
python manage.py find_arb
```

### Purging Stale Arbitrage Opportunities
To manually purge stale arbitrage opportunities from the db, run the following command:
```bash
python manage.py purge_arbs
```

## Celery Setup
- This app uses [Celery](https://github.com/celery/celery) , a distributed task queue to run the arbitrage finder in the background. The arbitrage finder is defined as a task in ```tasks.py``` along with other helper functions.
- Celery is configured to use [Redis](https://redis.io/) as a message broker along with django-celery-results to store the results of the tasks in the db. That way, the results can be accessed later from the API endpoints.
- For the results to be stored in the db, you need to run the migrations for django-celery-results:
```bash
python manage.py migrate django_celery_results
```

- Celery setup followed from [here](https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html#starting-the-worker-process)

## Running the Celery worker
To start the worker, run the following command:
```bash
celery -A ArbBackend worker -l <log_level> -B
```
Where log_level is one of the following:
- DEBUG
- INFO
Depending on the level of logging detail you want to see in the terminal.
By default, the worker will run the arbitrage finder **every minute** and purge stale arbs **every hour**. To change this, edit the ```CELERY_BEAT_SCHEDULE``` crontab in ```settings.py```.


