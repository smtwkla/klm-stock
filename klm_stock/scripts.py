import pymysql
from klm_menu import print_banner
import db_functions
import sectors

MIN_SCRIPT_NAME_LEN = 3     # Allowed min chars in a script name.
MIN_SCRIPT_CODE_LEN = 3


def list_scripts():
    """
    Prints list of all scripts in scripts table
    :return: None
    """
    cur: pymysql.cursors.Cursor = db_functions.dbc.cursor()
    sql = "SELECT id, script_code, script_name, sector_code FROM scripts ORDER BY script_code;"
    cur.execute(sql)
    res = cur.fetchall()

    i = 1
    print_banner("List of Scripts")
    for rec in res:
        print(f"{i}. [{rec[0]:3}] {rec[1]:15} - {rec[2]:50} : ({rec[3]})")
        i += 1


def add_script():
    """
    Gets input from user and inserts new script to table
    :return: None
    """
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
    """
    Get input from user and edit a script's details.
    :return: None
    """
    scr_code = input_script_code(check_exiting=True, prompt="Enter Script Code to Edit")
    if scr_code is None:
        return
    scr_new_code = input_script_code(check_exiting=False, prompt="Enter NEW Script Code")

    scr_name = input_script_name()
    if scr_name is None:
        return

    sec_code = sectors.input_sector_code(check_exiting=True)
    if sec_code is None:
        return

    scr_id = db_get_script_id(script_code=scr_code)

    cmd = "UPDATE scripts SET script_code=%s, script_name=%s, sector_code=%s " \
          "WHERE id=%s"
    val = (scr_new_code, scr_name, sec_code, scr_id)
    cur = db_functions.dbc.cursor()

    try:
        cur.execute(cmd, val)
        db_functions.dbc.commit()
    except pymysql.Error as e:
        print("Error processing SQL command:")
        print(e)


def del_script():
    """
    Get input and delete a script from table
    :return: None
    """
    scr_code = input_script_code(prompt="Enter Script code to DELETE", check_exiting=True)

    # First, check if records exists in transaction table for the script
    cmd = "SELECT COUNT(transactions.id) FROM transactions " \
          " LEFT JOIN scripts on transactions.script_id = scripts.id "\
          " WHERE scripts.script_code = %s;"
    val = (scr_code,)
    cur = db_functions.dbc.cursor()
    cur.execute(cmd, val)
    rec_cnt = cur.fetchone()

    if rec_cnt[0] > 0:
        print(f"Can not delete. {rec_cnt[0]} transactions exist for the script.")
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
    """
    Returns script_id of given script_code
    :param script_code: script_code to look up
    :return: script_id (int)
    """
    cur = db_functions.dbc.cursor()
    val = (script_code,)
    cur.execute("SELECT id FROM scripts WHERE script_code = %s", val)
    res = cur.fetchone()
    if res is None:
        return None
    else:
        return res[0]


def input_script_code(*, check_exiting=False, prompt=None):
    """
    Gets script code as input from user.
    Returns script code if valid, None if invalid input given.

    If check_existing is true, the script code is checked if it already exists in table.
    If exists, the code is returned. If not exists, None is returned.
    """
    prompt_str = ("Script Code" if prompt is None else prompt) + ": "
    scr_code = input(prompt_str)
    scr_code = scr_code.strip().upper()
    if len(scr_code) < MIN_SCRIPT_CODE_LEN:
        print(f"Invalid script code, must be {MIN_SCRIPT_CODE_LEN} characters or more.")
        return

    if check_exiting:
        scr_id = db_get_script_id(script_code=scr_code)
        if scr_id is None:
            print('Script not found.')
            return None
    return scr_code


def input_script_name(prompt=None):
    """
    Gets script name as input from user
    :param prompt: Prompt (str) to show to user
    :return: script_name entered by user
    """
    prompt_str = ("Script Name" if prompt is None else prompt) + ": "
    scr_name = input(prompt_str)
    scr_name = scr_name.strip().title()
    if len(scr_name) < MIN_SCRIPT_NAME_LEN:
        print(f"Script name must be minimum {MIN_SCRIPT_NAME_LEN} characters.")
        return None
    return scr_name
