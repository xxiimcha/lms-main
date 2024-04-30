from decouple import config


KEY = config('SECRET_KEY', cast=str)
DEV = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL')
PRODUCTION = config("PRODUCTION", cast=bool, default=True)

DB_USER =  config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_NAME = config("DB_NAME")