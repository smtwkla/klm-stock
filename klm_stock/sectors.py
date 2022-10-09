import pprint

import db_functions
from klm_menu import print_banner


def list_sectors():
    cur = db_functions.dbc.cursor()
    cur.execute("SELECT code, full_name FROM sectors;")
    res = cur.fetchall()
    i=1
    print_banner("List of Sectors")
    for row in res:
        print(f"{i}. {row[0]} - {row[1]}")
        i+=1


def get_sectors():
    pass


def get_sector_full_name(*, code):
    cur = db_functions.dbc.cursor()
    cmd = "SELECT full_name FROM sectors WHERE code=%s"
    val = (code,)
    cur.execute(cmd, val)
    res = cur.fetchone()
    if res is None:
        return None
    else:
        return res[0]

def add_sector(*, short_name, full_name):
    pass


def edit_sector(*, id, short_name, full_name):
    pass


def del_sector(*, id):
    pass


def input_sector_code(*, prompt=None, check_exiting=False):
    prompt_str = ("Enter Sector Code" if prompt is None else prompt) + ": "
    sec_code = input(prompt_str)
    sec_code = sec_code.strip().upper()
    if check_exiting:
        if get_sector_full_name(code=sec_code) is None:
            print("Sector Code does not exist.")
            return None
    return sec_code
