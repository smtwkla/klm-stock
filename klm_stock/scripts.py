import pprint
import pymysql
import db_functions
from klm_menu import print_banner
import sectors

MIN_SCRIPT_NAME_LEN = 3


def list_scripts():
    cur:pymysql.cursors.Cursor = db_functions.dbc.cursor()
    sql = "SELECT id, script_code, script_name, sector_code FROM scripts;"
    cur.execute(sql)

    res = cur.fetchall()
    i = 1
    print_banner("List of Scripts")
    for rec in res:
        print(f"{i}. [{rec[0]}] {rec[1]} - {rec[2]} : ({rec[3]})")
        i += 1

def add_script():
    print("Enter script details...")
    scr_code = input_script_code()
    if scr_code is None:
        return

    scr_name = input("Script Name:")
    scr_name = scr_name.strip().title()

    sec_code = input("Sector Code:")
    if sectors.get_sector_full_name(code=sec_code) is None:
        # we use sectors.get_sector_id to look up the sector code's full name
        # if None is returned, it means the given sector code is invalid.

        print("Error. Enter valid Sector code.")
        return

    cmd = "INSERT INTO scripts (script_code, script_name, sector_code)" \
          " VALUE (%s, %s, %s)"
    cur = db_functions.dbc.cursor()
    val = (scr_code, scr_name, sec_code)
    try:
        cur.execute(cmd, val)
        db_functions.dbc.commit()
    except pymysql.Error as e:
        print("Error processing SQL command:")
        print(e)


def edit_script():
    scr_code = input_script_code(check_exiting=True, prompt="Enter Script Code to Edit")
    if scr_code is None:
        return

    scr_name = input_script_name()
    if scr_name is None:
        return

    sec_code = sectors.input_sector_code(check_exiting=True)

    if sectors.get_sector_full_name(code=sec_code) is None:
        print("Error. Enter valid Sector code.")
        return

    scr_id = db_get_script_id(script_code=scr_code)

    cmd = "UPDATE scripts SET script_code=%s, script_name=%s, sector_code=%s " \
          "WHERE id=%s"

    cur = db_functions.dbc.cursor()
    val = (scr_code, scr_name, sec_code, scr_id)
    try:
        cur.execute(cmd, val)
        db_functions.dbc.commit()
    except pymysql.Error as e:
        print("Error processing SQL command:")
        print(e)


def del_script():
    scr_code = input_script_code(prompt="Enter Script code to DELETE", check_exiting=True)
    cmd = "SELECT COUNT(transactions.id) FROM transactions " \
          " LEFT JOIN scripts on transactions.script_id = scripts.id "\
          " WHERE scripts.script_code = %s;"
    val = (scr_code,)
    cur = db_functions.dbc.cursor()
    cur.execute(cmd, val)
    rec_cnt = cur.fetchone()
    print(f"{rec_cnt[0]} records exist for script.")
    if rec_cnt[0] > 0:
        print("Can not delete. Transactions exist for the script.")
        return

    cmd = "DELETE FROM scripts WHERE script_code=%s"

    cur = db_functions.dbc.cursor()
    try:
        cur.execute(cmd, val)
        db_functions.dbc.commit()
    except pymysql.Error as e:
        print("Error processing SQL command:")
        print(e)


def db_get_script_id(*, script_code):
    cur = db_functions.dbc.cursor()
    val = (script_code,)
    cur.execute("SELECT id FROM scripts WHERE script_code = %s", val)
    res = cur.fetchone()
    return res[0] if res is not None else None


def input_script_code(*,check_exiting=False, prompt=None):
    """
    Gets script code as input from user.
    Returns script code if valid, None if invalid input given.

    If check_existing is true, the script code is checked if it already exists in table.
    If exists, the code is returned. If not exists, None is returned.
    """
    prompt_str = ("Script Code" if prompt is None else prompt) + ": "
    scr_code = input(prompt_str)
    scr_code = scr_code.strip().upper()
    if not scr_code.isalnum() or len(scr_code) <= 1:
        print("Invalid script code. It can contain only alpa-numeric charecters, " 
              " must be more than one charecter.")
        return

    if check_exiting:
        scr_id = db_get_script_id(script_code=scr_code)
        if scr_id is None:
            print('Script not found.')
            return None
    return scr_code


def input_script_name(prompt=None):
    prompt_str = ("Script Name" if prompt is None else prompt) + ": "
    scr_name = input(prompt_str)
    scr_name = scr_name.strip().title()
    if len(scr_name) < MIN_SCRIPT_NAME_LEN:
        print(f"Script name must be minimum {MIN_SCRIPT_NAME_LEN} charecters.")
        return None
    return scr_name
