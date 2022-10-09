import pymysql

import scripts
import db_functions
from klm_menu import print_banner


def add_transaction(*, is_buy=True):
    """
    Inputs data and inserts new transaction entry.
    param is_buy: Is buy transaction if True, else sell
    :return: None
    """
    scr_code = scripts.input_script_code(check_exiting=True)
    if scr_code is None:
        return

    scr_id = scripts.db_get_script_id(script_code=scr_code)
    tr_date = input("Enter Date:")
    qty = int(input("Enter Qty:")) * (-1 if not is_buy else 1)
    try:
        price = float(input("Enter Price:"))
    except ValueError as e:
        print(e)
        return

    cmd = "INSERT INTO transactions " \
          "(script_id, date_of_trans, qty, price) " \
          " VALUE (%s, %s, %s, %s)"
    val = (scr_id, tr_date, qty, price)
    cur = db_functions.dbc.cursor()

    try:
        cur.execute(cmd, val)
        db_functions.dbc.commit()
    except pymysql.Error as e:
        print("Error inserting transaction: ", e)


def print_script_ledger():
    """
    Prints ledger of a script. Gets script name as input from user
    :return: None
    """
    LED_WIDTH = 70

    scr_code = scripts.input_script_code(check_exiting=True)
    scr_id = scripts.db_get_script_id(script_code=scr_code)

    cmd = "SELECT ts.id, ts.script_id, ts.date_of_trans, ts.qty, " \
          " ts.price, scr.script_name " \
          " FROM transactions AS ts LEFT JOIN scripts AS scr " \
          " ON scr.id = ts.script_id" \
          " WHERE ts.script_id=%s" \
          " ORDER BY ts.date_of_trans"

    val = (scr_id,)
    cur = db_functions.dbc.cursor()
    cur.execute(cmd, val)

    line_count = 1
    buy_tot = sell_tot = amt_tot = 0
    print_banner("Ledger of " + scr_code, star="-")
    print("-" * LED_WIDTH)
    print(f"{'#':3} | {'Date':^10} | {'Type':4} | {'Buy':6} |"
          f" {'Sell':6} | {'Price':8} | {'Amount':12} |")
    print("-" * LED_WIDTH)

    for rec in cur:
        buy = True if rec[3] > 0 else False
        sell = not buy
        tr_type = "Buy" if buy else "Sell"
        qty = abs(rec[3])
        buy_tot = buy_tot + (qty if buy else 0)
        sell_tot = sell_tot + (qty if sell else 0)
        tr_date = str(rec[2])
        tr_price = rec[4]
        tr_amt = tr_price * qty * (-1 if buy else 1)
        amt_tot += tr_amt
        print(f"{line_count:3} | {tr_date} | {tr_type:4} |"
              f" {qty if buy else '':6} | {qty if sell else '':6} | " 
              f"{tr_price:8.2f} | {tr_amt:12.2f} |")
        line_count += 1
    else:
        print("-" * LED_WIDTH)
        line = f"{'':3} | {'Totals:':10} | {'    '} | {buy_tot:6} |" \
               f" {sell_tot:6} | {' ':8} | {amt_tot:12.2f} |"
        print(line)
        print("-" * LED_WIDTH)



