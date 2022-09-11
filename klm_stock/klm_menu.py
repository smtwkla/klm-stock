M_CMD = "key"
M_PROMPT = "prompt"
M_HOTKEY = "hotkey"
M_SUBMENU = "submenu"

back_option = {M_CMD: "back", M_PROMPT: "Back...", M_HOTKEY: "b"}

def display_menu(menu_dict):
    """
     Function to display menu, as described in menu_dict dictionary.
     Ex : [{"key":"menu1", "prompt":"Menu Choice 1"}]

    main_menu = {
        "menu": "Main Menu",
        "options": [
            {M_CMD: "scripts", M_PROMPT: "Manage Scripts...", M_HOTKEY: "s"},
            {M_CMD: "analysis", M_PROMPT: "Analysis...", M_HOTKEY: "a"},
            {M_CMD: "transactions", M_PROMPT: "Transactions...", M_HOTKEY: "p"},
            {M_CMD: "exit", M_PROMPT: "Exit App", M_HOTKEY: "x"},
        ],
        "back_option": False
    }
    """
    print_banner(menu_dict["menu"])
    index = 1
    for i in menu_dict["options"]:
        print(f"{index}. {i[M_PROMPT]} ({i[M_HOTKEY]})")
        index +=1
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


def present_menu(menu, menu_system):
    while menu is not None:
        display_menu(menu)
        act = get_menu_input(menu)
        if ":" in act:
            menu_name = act.split(":")[1]
            menu = menu_system[menu_name]
        else:
            return act
    print(f"you chose {act}")


def print_banner(header):
    DEC_WIDTH = 25
    decoration = "*" * DEC_WIDTH
    print("\n"+decoration)
    print(header.center(DEC_WIDTH))
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
        for i in menu["options"]:
            if i[M_HOTKEY] == inp:
                return i[M_CMD]
    if type(inp) is int:
        options = menu["options"]
        if inp == len(options)+1 and menu["back_option"]:
            return "menu:"+menu["back_to"]
        return options[inp-1][M_CMD]
