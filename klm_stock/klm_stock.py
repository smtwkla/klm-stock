import klm_menu

import scripts
import sectors
import transactions
import portfolio
import ltp
import db_setup

import menu_def


menu_name = "main"

while menu_name:
    cmd, menu_name = klm_menu.present_menu(menu_name, menu_def.menu_system)
    if cmd == "exit":
        menu_name = None
        continue

    # execute cmd
    print("your command:"+cmd)
    if cmd == "list_scripts":
        scripts.list_scripts()
    elif cmd == "add_script":
        scripts.add_script()
    elif cmd == "edit_script":
        scripts.edit_script()
    elif cmd == "del_script":
        scripts.del_script()
    elif cmd == "list_sectors":
        sectors.list_sectors()
    elif cmd == "buy":
        transactions.add_transaction(is_buy=True)
    elif cmd == "sell":
        transactions.add_transaction(is_buy=False)
    elif cmd == "ledger":
        transactions.print_script_ledger()
    elif cmd == "list_hold":
        portfolio.print_holdings()
    elif cmd == "sector":
        portfolio.print_sector_holdings()
    elif cmd == "ltp":
        ltp.update_all_ltp()
        print("Updated.")
    elif cmd == "perf":
        portfolio.perf()
    elif cmd == "details":
        portfolio.chart()
    elif cmd == "setup":
        db_setup.setup()