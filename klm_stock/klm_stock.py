import klm_menu
import secrets
import menu_def
import scripts

menu = menu_def.main_menu

while menu:
    cmd, menu_name = klm_menu.present_menu(menu, menu_def.menu_system)
    menu = menu_def.menu_system[menu_name]
    if cmd == "exit":
        menu = None
        continue
    # execute cmd
    if cmd == "list_scripts":
        scripts.list_scripts()
    elif cmd == "add_script":
        scripts.add_script()
    elif cmd == "edit_script":
        scripts.edit_script()
    elif cmd == "del_script":
        scripts.del_script()
