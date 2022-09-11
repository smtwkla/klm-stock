from klm_menu import M_CMD, M_PROMPT, M_HOTKEY

main_menu = {
    "menu": "Main Menu",
    "name": "main",
    "options": [
        {M_CMD: "menu:scripts", M_PROMPT: "Manage Scripts...", M_HOTKEY: "s"},
        {M_CMD: "menu:analysis", M_PROMPT: "Analysis...", M_HOTKEY: "a"},
        {M_CMD: "menu:transactions", M_PROMPT: "Transactions...", M_HOTKEY: "t"},
        {M_CMD: "exit", M_PROMPT: "Exit App", M_HOTKEY: "x"},
    ],
    "back_option": False
}

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

analysis_menu = {
    "menu": "Analysis Menu",
    "name": "analysis",
    "options": [
        {M_CMD: "status", M_PROMPT: "Today's Status", M_HOTKEY: "t"},
        {M_CMD: "list_hold", M_PROMPT: "List Holdings", M_HOTKEY: "l"},
        {M_CMD: "ledger", M_PROMPT: "Script Ledger", M_HOTKEY: "a"},
        {M_CMD: "perf", M_PROMPT: "Script Performance", M_HOTKEY: "p"},
        {M_CMD: "chart", M_PROMPT: "Script Chart", M_HOTKEY: "c"},
    ],
    "back_option": True,
    "back_to": "main"
}

transactions_menu = {
    "menu": "Transactions Menu",
    "name": "transactions",
    "options": [
        {M_CMD: "buy", M_PROMPT: "Buy Entry", M_HOTKEY: "b"},
        {M_CMD: "sell", M_PROMPT: "Sell Entry", M_HOTKEY: "s"},
    ],
    "back_option": True,
    "back_to": "main"
}


menus = [main_menu, scripts_menu, analysis_menu, transactions_menu]
menu_system = { x["name"]: x for x in menus }
