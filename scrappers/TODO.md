# GENERAL SCRAPPER TODOS
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


# DOCKER TODOS
- Dockerize app --> done prototype
- Retry module to wait for db init on docker compose run --> done but not needed
- Add db setup script to replicate db structure --> done
- implement layer caching for faster builds on dockerfile --> done


# INFRA TODOS
- Set up db in raspberry pi cluster with 1 main db + scrapper and 2 scrapper only


# BACKEND TODOS
- revisit backend architecture


# FRONTEND TODOS
- Add frontend in Vue.js
- Add discord bots for notifs on arbitrage opportunities


