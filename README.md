# OpenAssetManager
Product for asset documentation for home to big business. Free base-system and non-free (paid) addons.

## Products

All of the projects are located in this project. This is a monorepo. Make sure you have ASDF installed. 

### Web

All web projects are under `web`, they are react projects. 

### API's
Our folder structure for the APIs:
```
fastapi-project
├── migrations/
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
├── router.py         # auth main router with all the endpoints
├── schemas.py        # pydantic models
├── models.py         # database models
│   ├── dependencies.py   # router dependencies
│   ├── config.py         # local configs
│   ├── constants.py      # module-specific constants
│   ├── exceptions.py     # module-specific errors
│   ├── service.py        # module-specific business logic
│   └── utils.py          # any other non-business logic functions
├── aws
│   ├── client.py  # client model for external service communication
│   ├── schemas.py
│   ├── config.py
│   ├── constants.py
│   ├── exceptions.py
│   └── utils.py
└── posts
│   ├── router.py
│   ├── schemas.py
│   ├── models.py
│   ├── dependencies.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── service.py
│   └── utils.py
├── config.py      # global configs
├── models.py      # global database models
├── exceptions.py  # global exceptions
├── pagination.py  # global module e.g. pagination
├── database.py    # db connection related stuff
├── main.py
├── .env
├── .gitignore
├── logging.ini
└── pyproject.toml
```
