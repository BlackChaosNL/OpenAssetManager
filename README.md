# OpenAssetManager
Product for asset documentation for home to big business. Free base-system and non-free (paid) addons.

Our folder structure:
```
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── router.py         # auth main router with all the endpoints
│   │   ├── schemas.py        # pydantic models
│   │   ├── models.py         # database models
│   │   ├── dependencies.py   # router dependencies
│   │   ├── config.py         # local configs
│   │   ├── constants.py      # module-specific constants
│   │   ├── exceptions.py     # module-specific errors
│   │   ├── service.py        # module-specific business logic
│   │   └── utils.py          # any other non-business logic functions
│   ├── aws
│   │   ├── client.py  # client model for external service communication
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   └── posts
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── config.py      # global configs
│   ├── models.py      # global database models
│   ├── exceptions.py  # global exceptions
│   ├── pagination.py  # global module e.g. pagination
│   ├── database.py    # db connection related stuff
│   └── main.py
├── tests/
│   ├── auth
│   ├── aws
│   └── posts
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
├── logging.ini
└── alembic.ini
```
