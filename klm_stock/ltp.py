import datetime
import random
import db_functions


def update_ltp(*, script_id, ltp, insert=False):
    """
    Function to edit/insert LTP of single script
    :param script_id: script ID to update
    :param ltp: last traded price
    :param insert: if true, use INSERT, else UPDATE
    :return: None
    """
    ts = datetime.datetime.now()
    if insert:
        cmd = "INSERT INTO ltp (script_id, update_ts, ltp) VALUE (%s, %s, %s)"
        val = (script_id, ts, ltp)
    else:
        cmd = "UPDATE ltp SET ltp=%s, update_ts=%s WHERE script_id=%s"
        val = (ltp, ts, script_id)
    cur = db_functions.dbc.cursor()
    cur.execute(cmd, val)
    db_functions.dbc.commit()


def update_all_ltp():
    """
    Updates price of all scripts in the scripts table
    :return: None
    """
    cmd = "SELECT scripts.id, l.ltp FROM scripts LEFT JOIN ltp l on scripts.id = l.script_id;"
    cur = db_functions.dbc.cursor()
    cur.execute(cmd)
    for i in cur:
        is_new_rec = i[1] is None
        old_ltp = i[1] or random.randint(150, 1500)
        old_ltp = float(old_ltp)
        # Testing code to generate random price changes
        new_ltp = old_ltp * (1 + random.randint(-15, +15)/100)
        update_ltp(script_id=i[0], ltp=new_ltp, insert=is_new_rec)
