import datetime

import db_functions
import scripts


def create_tables():
    create_commands = [
        "CREATE TABLE IF NOT EXISTS sectors "
        "(code CHAR(10) NOT NULL PRIMARY KEY,"
        "full_name VARCHAR(50));",

        "CREATE TABLE IF NOT EXISTS scripts"
        "(id INT AUTO_INCREMENT PRIMARY KEY, "
        "script_code CHAR(15) NOT NULL,"
        "script_name VARCHAR(50) NOT NULL,"
        "sector_code CHAR(10) NOT NULL,"
        "CONSTRAINT scripts_pk UNIQUE(script_code));",

        "CREATE TABLE IF NOT EXISTS transactions"
        "(id INT AUTO_INCREMENT PRIMARY KEY,"
        "script_id     INT           NOT NULL,"
        "date_of_trans DATE          NOT NULL,"
        "qty           INT           NOT NULL,"
        "price         DECIMAL(8, 2) NOT NULL);",

        "CREATE TABLE IF NOT EXISTS ltp"
        "(script_id INT NOT NULL PRIMARY KEY,"
        "ts        DATETIME      NOT NULL,"
        "ltp       DECIMAL(8, 2) NOT NULL);"
    ]
    cur = db_functions.dbc.cursor()
    for cmd in create_commands:
        print(cmd)
        cur.execute(cmd)
    db_functions.dbc.commit()


def create_sector_records():
    sectors = [("AUTO", "Automobile"),
               ("BANK", "Banking"),
               ("FINSERV", "Financial Services"),
               ("FMCG", "Fast Moving Consumer Goods"),
               ("INFRA", "Infrastructure"),
               ("IT", "Information Technology"),
               ("REAL", "Real Estate and Construction"),
               ("CEM","Cement"),
               ("ENG", "Engineering"),
               ("PET", "Petroleum"),
               ("TOUR", "Tourism"),
               ("REN", "Renewable Energy"),
               ("CE", "Consumer Electronics"),
               ("ELEC", "Electrical Energy"),
               ("CHE", "Speciality Chemicals"),
               ("PHARM", "Pharmaceutical"),

               ]
    print("Creating sectors list...")
    cmd = "INSERT INTO sectors (code, full_name) VALUE (%s, %s);"
    cur = db_functions.dbc.cursor()
    for val in sectors:
        cur.execute(cmd, val)
    db_functions.dbc.commit()


def create_test_scripts():
    test_scripts = [
        ("SBIN", "State Bank of India", "BANK"),
        ("AXIS", "Axis Bank Ltd", "BANK"),
        ("ICICI", "Icici Limited", "BANK"),
        ("TECHM", "Tech Mahindra", "IT"),
        ("DABUR", "Dabur Ltd", "FMCG"),
        ("NESTLEIND", "Nestle India Ltd", "FMCG"),
        ("TATACOFFEE", "Tata Coffee Ltd", "FMCG"),
        ("HCLTECH", "Hcl Technologies Ltd", "IT"),
        ("TCS", "Tata Consultancy Services Ltd", "IT"),
        ("INFY", "Infosys Ltd", "IT"),
        ("LT", "Larsen & Toubro Ltd", "INFRA"),
        ("GMRINFRA", "Gmr Airports Infrastructure Ltd", "INFRA"),
        ("HDFC", "Housing Development Finance Corp Ltd", "FINSERV"),
        ("SFN", "Sundaram Finance Ltd", "FINSERV"),
        ("MAHLIFE", "Mahindra Lifespace Developers Ltd", "REAL"),
        ("BRIGADE", "Brigade Enterprises Ltd", "REAL"),
        ("M&M", "Mahindra & Mahindra Ltd", "AUTO"),
        ("TVSMOTOR", "Tvs Motor Company Ltd", "AUTO"),
        ("MRF", "Mrf Ltd", "AUTO"),
        ("BAJAJ", "Bajaj Electricals", "CE"),
        ("SUNPHARMA", "Sun Pharmaceutical Industries", "PHARM"),
        ("RAMCOCEM", "Ramco Cement Ltd", "CEM"),
        ("THERMAX", "Thermax Ltd", "ENG"),
        ("INDHOTEL","The Indian Hotels Co Ltd","TOUR"),

    ]
    print("Initialising scripts table...")
    cur = db_functions.dbc.cursor()
    cmd = "DELETE FROM scripts;"
    cur.execute(cmd)

    cmd = "INSERT INTO scripts (script_code, script_name, sector_code) " \
          " VALUE (%s, %s, %s)"
    for rec in test_scripts:
        cur.execute(cmd, rec)

    db_functions.dbc.commit()


def delete_tables():
    cur = db_functions.dbc.cursor()
    table_list = ["transactions", "ltp", "scripts", "sectors"]
    for table in table_list:
        cmd = "DROP TABLE IF EXISTS " + table + ";"
        print(cmd)
        cur.execute(cmd)
    db_functions.dbc.commit()


def create_test_transactions():
    trans = [['SBIN', '2020-01-05', 100, 455.0],
             ['SBIN', '2020-02-01', 250, 465.0],
             ['SBIN', '2020-03-01', 100, 455.0],
             ['SBIN', '2020-04-11', 150, 445.0],
             ['SBIN', '2020-05-01', 110, 453.0],
             ['SBIN', '2021-06-01', 110, 555.0],
             ['SBIN', '2021-07-01', 145, 552.0],
             ['SBIN', '2021-08-01', 1000, 655.0],
             ['SBIN', '2021-09-01', 200, 456.0],
             ['SBIN', '2022-01-05', 400, 454.0],
             ['SBIN', '2022-02-01', 1400, 645.0],
             ['SBIN', '2023-03-01', 1020, 655.0],

             ['AXIS', '2018-01-01', 250, 500],
             ['AXIS', '2018-02-01', 250, 510],
             ['AXIS', '2019-03-01', 250, 600],
             ['AXIS', '2020-04-01', -750, 670],
             ['AXIS', '2021-05-01', 250, 700],
             ['AXIS', '2021-06-01', -250, 745],

             ['ICICI', '2021-01-01', 250, 500],
             ['ICICI', '2021-01-01', 250, 760],
             ['ICICI', '2021-01-01', -500, 810],

             ['TECHM', '2021-03-01', 50, 1024],
             ['DABUR', '2010-04-01', 10, 810],
             ['NESTLEIND', '2012-05-01', 500, 512],
             ['TATACOFFEE', '2013-06-01', 600, 180],
             ['HCLTECH', '2014-08-01', 2500, 814],
             ['TCS', '2014-02-01', 20, 2810],
             ['LT', '2019-03-01', 1500, 1810],
             ['HDFC', '1991-09-01', 500, 81.0],
             ['MAHLIFE', '2001-10-01', 75, 710],
             ['TVSMOTOR', '2011-12-01', 150, 210],
             ['MRF', '2022-03-01', 545, 910],
             ['SUNPHARMA', '2021-01-03', 100, 733],
             ['BAJAJ', '2021-04-10', 15, 1006],

             ['RAMCOCEM', '2001-04-10', 150, 575],
             ['THERMAX', '2012-05-10', 150, 1300],
             ['INDHOTEL', '2019-05-10', 250, 325],
             ]
    cur = db_functions.dbc.cursor()
    cmd = "INSERT INTO transactions " \
          "(script_id, date_of_trans, qty, price) " \
          "VALUE (%s, %s, %s, %s);"
    for tr in trans:
        tr[0] = (scripts.db_get_script_id(script_code=tr[0]))
        cur.execute(cmd, tr)
    db_functions.dbc.commit()


def create_ltp():
    ltp_list = [
        ['SBIN', 750],
        ['AXIS', 850],
        ['ICICI', 550],
        ['TECHM', 1100],
        ['DABUR', 1022],
        ['NESTLEIND', 612],
        ['TATACOFFEE', 455],
        ['HCLTECH', 554],
        ['TCS', 3180],
        ['INFY', 4500],
        ['LT', 2100],
        ['GMRINFRA', 122],
        ['HDFC', 81],
        ['SFN', 232],
        ['MAHLIFE', 70],
        ['BRIGADE', 320],
        ['M&M', 232],
        ['TVSMOTOR', 250],
        ['MRF', 1021],
        ['SUNPHARMA', 993],
        ['BAJAJ', 1196],
        ['RAMCOCEM', 1119],
        ['THERMAX', 2454],
        ['INDHOTEL', 334]
    ]
    cur = db_functions.dbc.cursor()
    cmd = "INSERT INTO ltp (script_id, ts, ltp) " \
          " VALUE (%s, %s, %s)"
    ts = datetime.datetime.now()
    for ltp in ltp_list:
        ltp[0] = (scripts.db_get_script_id(script_code=ltp[0]))
        cur.execute(cmd, (ltp[0], ts, ltp[1]))
    db_functions.dbc.commit()


def setup():
    confirm = input("WARNING! This will delete all data! "
                    "All tables will be re-created. "
                    "Sample data will be inserted. "
                    "Enter DELETE to confirm.")
    if confirm != "DELETE":
        return

    delete_tables()
    create_tables()
    create_sector_records()
    create_test_scripts()
    create_test_transactions()
    create_ltp()
