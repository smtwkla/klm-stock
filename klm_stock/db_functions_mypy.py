import mysql.connector as mysql
from app_secrets import DB_SETTINGS


def connect_db(db_settings):
    """
    Connects to db as per settings dict given
    :param db_settings: dict, needs host, user, password, db keys
    :return: mysql connector
    """
    print(f"Connecting to DB...")
    myc = mysql.connect(host=db_settings["host"],
                        user=db_settings["user"],
                        password=db_settings["password"],
                        db=db_settings["db"])
    return myc


# global variable dbc
# all modules import this, but connection happens once only
dbc = connect_db(DB_SETTINGS)
