from klm_menu import M_CMD, M_PROMPT, M_HOTKEY, generate_menu_system
import pprint

main_menu = {
    "menu": "Main Menu",
    "name": "main",
    "options": [
        ["menu:scripts", "Manage Scripts...", "s"],
        ["menu:analysis", "Analysis...", "a"],
        ["menu:transactions", "Transactions...", "t"],
        ["exit","Exit App","x"],
    ],
    "back_option": False
}

scripts_menu = {
    "menu": "Manage Scripts Menu",
    "name": "scripts",
    "options": [
        ["list_scripts","List Scripts","l"],
        ["add_script","Add Script","a"],
        ["edit_script","Edit Script","e"],
        ["del_script","Delete Script","d"],
    ],
    "back_option": True,
    "back_to": "main"
}

analysis_menu = {
    "menu": "Analysis Menu",
    "name": "analysis",
    "options": [
        ["status","Today's Status","t"],
        ["list_hold","List Holdings","l"],
        ["ledger","Script Ledger","a"],
        ["perf","Script Performance","p"],
        ["chart","Script Chart","c"],
    ],
    "back_option": True,
    "back_to": "main"
}

transactions_menu = {
    "menu": "Transactions Menu",
    "name": "transactions",
    "options": [
        ["buy","Buy Entry","b"],
        ["sell","Sell Entry","s"],
    ],
    "back_option": True,
    "back_to": "main"
}


menu_system = generate_menu_system(main_menu, scripts_menu, analysis_menu, transactions_menu)
