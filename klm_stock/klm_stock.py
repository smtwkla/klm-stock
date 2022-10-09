import pymysql
import klm_menu

import db_functions
import scripts
import sectors

import app_secrets
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
