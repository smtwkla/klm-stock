import db_functions


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
        ("MRF", "Mrf Ltd", "AUTO")
    ]
    print("Initialising scripts table...")
    cur = db_functions.dbc.cursor()
    cmd = "DELETE FROM scripts;"
    cur.execute(cmd)

    cmd = "INSERT INTO scripts (script_code, script_name, sector_code) "\
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
