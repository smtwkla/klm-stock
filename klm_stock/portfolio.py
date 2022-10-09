import pymysql
import db_functions


def calc_total_holding_amt():
    """
    Calculates total value of total holdings, as per last traded price.
    Used to calculate %
    :return: float
    """

    cmd = "SELECT sum(ts.qty * ltp.ltp) as amt" \
          " FROM transactions AS ts LEFT JOIN scripts AS scr ON scr.id = ts.script_id " \
          " LEFT JOIN ltp ON scr.id = ltp.script_id"
    cur = db_functions.dbc.cursor(pymysql.cursors.DictCursor)
    cur.execute(cmd)
    rec = cur.fetchone()
    return rec["amt"]


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
    pass


def chart():
    pass
