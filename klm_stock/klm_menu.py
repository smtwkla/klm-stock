import pprint

M_CMD = "cmd"
M_PROMPT = "prompt"
M_HOTKEY = "hotkey"
M_SUBMENU = "submenu"

back_option = {M_CMD: "back", M_PROMPT: "Back...", M_HOTKEY: "b"}


def display_menu(menu_dict):
    """
     Function to display menu, as described in menu_dict dictionary.
     Ex :
        scripts_menu = {
            "menu": "Manage Scripts Menu",
            "name": "scripts",
            "options": [
                {M_CMD: "list_scripts", M_PROMPT: "List Scripts", M_HOTKEY: "l"},
                {M_CMD: "add_script", M_PROMPT: "Add Script", M_HOTKEY: "a"},
                {M_CMD: "edit_script", M_PROMPT: "Edit Script", M_HOTKEY: "e"},
                {M_CMD: "del_script", M_PROMPT: "Delete Script", M_HOTKEY: "d"},
            ],
            "back_option": True,
            "back_to": "main"
}
    """
    print_banner(menu_dict["menu"])
    index = 1
    for i in menu_dict["options"]:
        print(f"{index}. {i[M_PROMPT]} ({i[M_HOTKEY]})")
        index += 1
    if menu_dict["back_option"]:
        print(f"{index}. {back_option[M_PROMPT]} ({back_option[M_HOTKEY]})")


def get_menu_input(menu):
    valid_chars = get_valid_hotkeys(menu)
    max_num = get_valid_choice_nums(menu)
    action = None

    while True:
        inp = input(f"Enter choice (1..{max_num}) or {valid_chars}:")
        if not inp.isalnum():
            print("Invalid input.")
            continue
        if inp.isdigit():
            choice_num = int(inp)
            if 0 < choice_num <= max_num:
                action = get_menu_cmd(menu, choice_num)
                break
            else:
                print("Invalid number entered. ", end="")
        if inp.isalpha():
            inp = inp.strip()
            inp = inp.lower()
            if inp in valid_chars:
                action = get_menu_cmd(menu, inp)
                break
            else:
                print("Invalid character entered. ", end="")
    return action


def present_menu(menu_to_present, menu_system):
    menu = menu_system[menu_to_present]
    while menu is not None:
        display_menu(menu)
        act = get_menu_input(menu)
        if ":" in act:
            menu_name = act.split(":")[1]
            menu = menu_system[menu_name]
        else:
            menu_name = menu["name"]
            return act, menu_name


def print_banner(header, star="*", width=25):
    """ Prints banner with decoration at top and bottom """
    decoration = star * width
    print("\n"+decoration)
    print(header.center(width))
    print(decoration+"\n")


def get_valid_hotkeys(menu):
    hotkeys = []
    for i in menu["options"]:
        hotkeys.append(i[M_HOTKEY])
    if menu["back_option"]:
        hotkeys.append(back_option[M_HOTKEY])
    return hotkeys


def get_valid_choice_nums(menu):
    return len(menu["options"]) + (1 if menu["back_option"] else 0)


def get_menu_cmd(menu, inp):
    if type(inp) is str:
        if inp == back_option[M_HOTKEY] and menu["back_option"]:
            return "menu:" + menu["back_to"]
        for i in menu["options"]:
            if i[M_HOTKEY] == inp:
                return i[M_CMD]
    if type(inp) is int:
        options = menu["options"]
        if inp == len(options)+1 and menu["back_option"]:
            return "menu:"+menu["back_to"]
        return options[inp-1][M_CMD]


def generate_menu_system(*menus):
    """ Generates Menu system dictionary from list of menus given as arguments """
    menu_sys = {}
    for menu in menus:
        menu_name = menu["name"]
        menu_sys[menu_name] = menu
    return menu_sys
    # return {i["name"]: i for i in menus}
