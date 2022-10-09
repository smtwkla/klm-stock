import pprint
from klm_menu import print_banner
import pymysql

import scripts
import db_functions


def add_trasaction(*, is_buy=True):
    scr_code = scripts.input_script_code(check_exiting=True)
    scr_id = scripts.db_get_script_id(script_code=scr_code)
    tr_date = input("Enter Date:")
    qty = int(input("Enter Qty:")) * (-1 if not is_buy else 1)
    price = float(input("Enter Price:"))
    cmd = "INSERT INTO transactions (script_id, date_of_trans, qty, price) "\
          " VALUE (%s, %s, %s, %s)"
    val = (scr_id, tr_date, qty, price)
    cur = db_functions.dbc.cursor()
    try:
        cur.execute(cmd,val)
        db_functions.dbc.commit()
    except pymysql.Error as e:
        print("Error inserting transaction: ", e)


def print_script_ledger():
    LED_WIDTH = 70
    scr_code = scripts.input_script_code(check_exiting=True)
    scr_id = scripts.db_get_script_id(script_code=scr_code)
    cmd = "SELECT ts.id, ts.script_id, ts.date_of_trans, ts.qty, ts.price, scr.script_name "\
          " FROM transactions AS ts LEFT JOIN scripts AS scr ON scr.id = ts.script_id" \
          " WHERE ts.script_id=%s" \
          " ORDER BY ts.date_of_trans"
    val = (scr_id,)
    cur = db_functions.dbc.cursor()
    cur.execute(cmd,val)
    print_banner("Ledger of " + scr_code, star="-")
    buy_tot = sell_tot = amt_tot = 0
    line_count = 1
    print("-" * LED_WIDTH)
    line = f"{'#':3} | {'Date':^10} | {'Type':4} | {'Buy':6} | {'Sell':6} | {'Price':8} | {'Amount':12} |"
    print(line)
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
        line = f"{line_count:3} | {tr_date} | {tr_type:4} | {qty if buy else '':6} | {qty if sell else '':6} | {tr_price:8.2f} | {tr_amt:12.2f} |"
        print(line)
        line_count += 1
    else:
        print("-" * LED_WIDTH)
        line = f"{'':3} | {'Totals:':10} | {'    '} | {buy_tot:6} | {sell_tot:6} | {' ':8} | {amt_tot:12.2f} |"
        print(line)
        print("-" * LED_WIDTH)


def calc_total_holding_amt():

    cmd = "SELECT sum(ts.qty * ltp.ltp) as amt" \
            " FROM transactions AS ts LEFT JOIN scripts AS scr ON scr.id = ts.script_id " \
            " LEFT JOIN ltp ON scr.id = ltp.script_id"
    cur = db_functions.dbc.cursor(pymysql.cursors.DictCursor)
    cur.execute(cmd)
    rec = cur.fetchone()
    return rec["amt"]


def print_holdings():
    HOLDING_WIDTH = 99
    cmd = "SELECT ts.script_id, scr.script_code, scr.script_name, scr.sector_code, sum(ts.qty) as qty, ltp.ltp" \
            " FROM transactions AS ts LEFT JOIN scripts AS scr ON scr.id = ts.script_id " \
            " LEFT JOIN ltp ON scr.id = ltp.script_id" \
            " GROUP BY scr.script_code ORDER BY scr.script_code;"
    cur = db_functions.dbc.cursor(pymysql.cursors.DictCursor)
    cur.execute(cmd)
    i = 1
    total = calc_total_holding_amt()

    l = f'{"":3} | {"Code":10} | {"Script Name":25} | {"Sector":10} | {"Qty":6} | {"LTP":8} | {"Value@LTP":10} | ' \
        f'{"%":4} |'
    print("-" * HOLDING_WIDTH)
    print(l)
    print("-" * HOLDING_WIDTH)

    for rec in cur:
        price = rec['ltp'] or 0
        amt = price * rec['qty']
        percent = round(amt / total*100,1)
        l = f'{i:3} | {rec["script_code"]:10} | {rec["script_name"]:25} | {rec["sector_code"]:10} | {rec["qty"]:6} | ' \
            f'{price:8.2f} | {amt:10.2f} | {percent:5.1f}'
        print(l)
        i += 1
    print("-" * HOLDING_WIDTH)
    print("Total Value of Holdings @ LTP:", total)


def print_sector_holdings():
    SEC_WIDTH = 69
    cmd = "SELECT scr.sector_code, sum(ts.qty * ltp.ltp) as amt, sectors.full_name" \
            " FROM transactions AS ts LEFT JOIN scripts AS scr ON scr.id = ts.script_id " \
            " LEFT JOIN ltp ON scr.id = ltp.script_id" \
            " LEFT JOIN sectors on scr.sector_code = sectors.code" \
            " GROUP BY scr.sector_code ORDER BY scr.sector_code;"

    cur = db_functions.dbc.cursor(pymysql.cursors.DictCursor)
    cur.execute(cmd)
    i = 1
    tot_amt = calc_total_holding_amt()

    print("-" * SEC_WIDTH)
    l = f'{"":3} | {"Code":10} | {"Sector":25} | {"Amount":10} | {"Percent":6} |'
    print(l)
    print("-" * SEC_WIDTH)
    for rec in cur:
        amt = rec["amt"] if rec["amt"] else 0
        percent= round(amt / tot_amt * 100, 1)
        l = f'{i:3} | {rec["sector_code"]:10} | {rec["full_name"]:25} | {amt:10.2f} | {percent:6.2f}% |'
        print(l)
        i += 1
    print("-" * SEC_WIDTH)
    print("Total Holdings:", tot_amt)
