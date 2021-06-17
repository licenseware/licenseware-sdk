import os


def add_test_environment_vars():
    # Using this for tests
        
    if os.getenv('ENVIRONMENT') is None:
        
        MONGO_ROOT_USERNAME = 'licensewaredev'
        MONGO_ROOT_PASSWORD ='license123ware'
        MONGO_DATABASE_NAME='db'
        MONGO_HOSTNAME= 'localhost' #for a docker environment use 'mongodb' (service name)
        MONGO_PORT=27017

        os.environ['MONGO_DATABASE_NAME'] = MONGO_DATABASE_NAME
        os.environ['MONGO_CONNECTION_STRING'] = f"mongodb://{MONGO_ROOT_USERNAME}:{MONGO_ROOT_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}"

