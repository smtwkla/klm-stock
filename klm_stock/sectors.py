from klm_menu import print_banner

import db_functions


def list_sectors():
    """
    List all sectors in sector table
    :return: None
    """
    cur = db_functions.get_cursor()
    cur.execute("SELECT code, full_name FROM sectors;")
    res = cur.fetchall()
    i = 1
    print_banner("List of Sectors")
    for row in res:
        print(f"{i}. {row[0]} - {row[1]}")
        i += 1


def get_sector_full_name(*, code):
    """
    Returns full name of sector, given a sector code
    :param code: sector code str to search for
    :return: sector full name (str)
    """
    cur = db_functions.get_cursor()
    cmd = "SELECT full_name FROM sectors WHERE code=%s"
    val = (code,)
    cur.execute(cmd, val)
    res = cur.fetchone()
    if res is None:
        return None
    else:
        return res[0]


def input_sector_code(*, prompt=None, check_exiting=False):
    """
    Gets a sector code as input from user
    :param prompt: text to display to user. Default:"Enter Sector Code:"
    :param check_exiting: if yes, checks if code exists
    :return: sector code that was input by user
    """
    prompt_str = ("Enter Sector Code" if prompt is None
                  else prompt) + ": "
    sec_code = input(prompt_str)
    sec_code = sec_code.strip().upper()
    if check_exiting:
        if get_sector_full_name(code=sec_code) is None:
            print("Sector Code does not exist.")
            return None
    return sec_code
