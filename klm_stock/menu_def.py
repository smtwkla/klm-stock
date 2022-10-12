from klm_menu import M_CMD, M_PROMPT, M_HOTKEY, generate_menu_system


main_menu = {
    "menu": "Main Menu",
    "name": "main",
    "options": [
        ["menu:scripts", "Manage Scripts...", "s"],
        ["menu:analysis", "Analysis...", "a"],
        ["menu:transactions", "Transactions...", "t"],
        ["ltp", "Fetch Last Traded Price", "l"],
        ["exit", "Exit App", "x"],
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
        {M_CMD: "list_sectors", M_PROMPT: "List Sectors", M_HOTKEY: "s"},
        {M_CMD: "setup", M_PROMPT: "Initialise Database", M_HOTKEY: "i"}
    ],
    "back_option": True,
    "back_to": "main"
}

analysis_menu = {
    "menu": "Analysis Menu",
    "name": "analysis",
    "options": [
        {M_CMD: "sector", M_PROMPT: "Sector-wise Holdings", M_HOTKEY: "s"},
        {M_CMD: "list_hold", M_PROMPT: "List All Holdings", M_HOTKEY: "l"},
        {M_CMD: "ledger", M_PROMPT: "Script Ledger", M_HOTKEY: "a"},
        {M_CMD: "perf", M_PROMPT: "Script Performance", M_HOTKEY: "p"},
        {M_CMD: "details", M_PROMPT: "Script Details on NSE", M_HOTKEY: "d"},
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


menu_system = {
                "main": main_menu,
                "scripts": scripts_menu,
                "analysis": analysis_menu,
                "transactions": transactions_menu
               }

