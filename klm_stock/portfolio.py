import scripts
import os
import pymysql
import db_functions
from klm_menu import print_banner


def calc_total_holding_amt():

    cmd = "SELECT sum(ts.qty * ltp.ltp) as amt" \
          " FROM transactions AS ts LEFT JOIN scripts AS scr ON scr.id = ts.script_id " \
          " LEFT JOIN ltp ON scr.id = ltp.script_id"
    cur = db_functions.dbc.cursor(pymysql.cursors.DictCursor)
    cur.execute(cmd)
    rec = cur.fetchone()
    return rec["amt"]


"""
Calculates total value of total holdings, as per last traded price.
Used to calculate %
:return: float
"""


def print_holdings():
    """
    Print all holdings, with valuation as per LTP
    :return: None
    """
    HOLDING_WIDTH = 99

    cmd = "SELECT ts.script_id, scr.script_code, scr.script_name, scr.sector_code, sum(ts.qty) as qty, ltp.ltp" \
          " FROM transactions AS ts LEFT JOIN scripts AS scr ON scr.id = ts.script_id " \
          " LEFT JOIN ltp ON scr.id = ltp.script_id" \
          " GROUP BY scr.script_code ORDER BY scr.script_code;"
    cur = db_functions.dbc.cursor(pymysql.cursors.DictCursor)
    cur.execute(cmd)

    i = 1
    total = calc_total_holding_amt()
    print("-" * HOLDING_WIDTH)
    print(f'{"":3} | {"Code":10} | {"Script Name":25} | {"Sector":10} | {"Qty":6} | {"LTP":8} | {"Value@LTP":10} | '
          f'{"%":4} |')
    print("-" * HOLDING_WIDTH)

    for rec in cur:
        price = rec['ltp'] or 0
        amt = price * rec['qty']
        percent = round(amt / total * 100, 1)
        print(f'{i:3} | {rec["script_code"]:10} | {rec["script_name"]:25} | {rec["sector_code"]:10} | {rec["qty"]:6} | '
              f'{price:8.2f} | {amt:10.2f} | {percent:5.1f}')
        i += 1
    print("-" * HOLDING_WIDTH)
    print("Total Value of Holdings @ LTP:", total)


def print_sector_holdings():
    """
    Print sector-wise summary of holdings.
    :return: None
    """
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
    print(f'{"":3} | {"Code":10} | {"Sector":25} | {"Amount":10} | {"Percent":6} |')
    print("-" * SEC_WIDTH)
    for rec in cur:
        amt = rec["amt"] if rec["amt"] else 0
        percent = round(amt / tot_amt * 100, 1)
        print(f'{i:3} | {rec["sector_code"]:10} | {rec["full_name"]:25} | {amt:10.2f} | {percent:6.2f}% |')
        i += 1
    print("-" * SEC_WIDTH)
    print("Total Value of Holdings @ LTP:", tot_amt)


def perf():
    """
    Inputs script code (existing) and shows performance data of the investment
    :return: None
    """
    print_banner('Investment Analysis')
    scr_code = scripts.input_script_code(check_exiting=True)
    if scr_code is None:
        return
    scr_id = scripts.db_get_script_id(script_code=scr_code)

    # find how many stock qty is at hand
    cmd = "SELECT SUM(qty) FROM transactions t WHERE t.script_id=%s"
    val = (scr_id,)
    cur = db_functions.dbc.cursor()
    cur.execute(cmd, val)
    res = cur.fetchone()
    qty = res[0]

    print(f'Total of {qty or 0} numbers of script {scr_code} is available.')
    if not qty or qty < 0:
        return

    # find LTP for the script
    cmd = "SELECT ltp FROM ltp WHERE ltp.script_id=%s"
    val = (scr_id,)
    cur = db_functions.dbc.cursor()
    cur.execute(cmd, val)
    res = cur.fetchone()
    ltp = res[0]

    # find purchase history of the share, to calculate average purchase price
    bal_qty = qty
    price_list = []
    cmd = "SELECT t.script_id, t.date_of_trans, t.qty, t.price FROM transactions t " \
          " WHERE t.script_id=%s AND t.qty > 0 ORDER BY t.date_of_trans DESC"
    val = (scr_id,)
    cur.execute(cmd, val)
    for rec in cur:
        cur_qty = rec[2]
        cur_price = rec[3]
        if bal_qty > cur_qty:
            bal_qty = bal_qty - cur_qty
            price_list.append([cur_qty, cur_price])
        else:
            price_list.append([bal_qty, cur_price])
            bal_qty = 0
            break

    amt = 0
    for pr in price_list:
        amt = amt + pr[0] * pr[1]

    avg = amt / qty
    val_ltp = qty * ltp
    net_gl = val_ltp - amt
    per_gl = net_gl / amt * 100

    print(f"Average purchase price     : {avg:12.2f}")
    print(f"Purchase investment        : {amt:12.2f}")
    print(f"Value at LTP               : {val_ltp:12.2f}")
    print(f"Net Gain / Loss            : {net_gl:12.2f}")
    print(f"% Gain / Loss              : {per_gl:11.2f}%")


def chart():
    """
    Inputs script code (even non-existing in table) and opens NSE website page with details
    about the script
    :return: None
    """
    scr_code = scripts.input_script_code(check_exiting=False)
    if scr_code is None:
        return
    os.system("start \"\" https://www.nseindia.com/get-quotes/equity?symbol="+scr_code)
