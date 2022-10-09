import pymysql as mysql
import pymysql.connections
from app_secrets import DB_SETTINGS


def connect_db(db_settings) -> pymysql.connections.Connection:
    myc = mysql.connect(host=db_settings["host"],
                user=db_settings["user"],
                password=db_settings["password"],
                db=db_settings["db"])
    return myc


dbc: pymysql.connections.Connection = connect_db(DB_SETTINGS)