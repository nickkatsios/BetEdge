# Scrappers
- Docs for urls --> done
- fix readme for usage with poetry --> done
- fix all prev main scrappers --> done
- add robust error handling
- add email notification system for errors --> done
- account for missing data when scrapping before db insertion ex: missing price, missing date (see schema not null).
If none values are present in the matching and the 2 events match (by either name or date), the none values must be replaced with the corresponding values from the complete info event or the incomplete event must be discarded.
- Add tests
- Add CI/CD in github actions --> done prototype
- Add support and options for firefox --> done
- Add logging --> done
- Add top level logger for general container logs --> done
- guide for running on windows
- add examples for various use cases
- create and add handlers in scrapper manager and not in __init__ of scrapper
- pack all 3 .env files in one file
- Better url scrapping with classes for each bookamer like main scrapping --> done
- Add url scrapping error handling , scheduling , logging retrying etc --> scheduling done

# Backend
- change id db naming as outlined here
https://stackoverflow.com/questions/37839867/valueerror-cannot-assign-must-be-an-instance
- delete venv from git and add requirements.txt -> done 
- schedule arb check (with celery? or cron?) --> done
- arb error handling
- add logging
- add tests
- add docker , to be added to main docker-compose.yml 
- add celery result ui with django-celery-beat 
- reasearch in django best practices for project structure
- configure docker build to start celery worker
- add helper arb functions in /managment/commands/
- add tasks to celery worker to clean db from old events, markets, arb opportunities
- check if arb already exists in db before adding it --> done

# Frontend
- Build simple frontend in Vue.js to display arb opportunities
- dockerize frontend
- Add discord bots for notifs on arbitrage opportunities