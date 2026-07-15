# global_configs.py - DO NOT REMOVE THIS LINE FROM THE SCRIPT!!!

class GlobalConsts:

    # Hardcode the item category to use for this code execution
    ITEM_CATEGORY_ON_TRADESITE = "Jewel"

    # Replace phrases before output. If "", the modifier is skipped entirely.
    KEYWORD_REPLACE = {
        "#% chance to Daze on Hit": "Dazes on Hit",  # This jewel modifier is weird.
        "#% chance for Attack Hits to apply Incision": "Attack Hits apply Incision",   # This jewel modifier is weird.
    }

    # Other file/folder names, modifying these should not be needed
    FILE_NAME = ITEM_CATEGORY_ON_TRADESITE
    FILE_RAW_DATA_INPUT = "raw_data_input.txt"
    FILE_RAW_DATA_OUTPUT = "raw_data_output.json"
    FOLDER_AHK_INPUTS = "ahk_inputs"
    FOLDER_CLEANED_POE2DB_DATA = "cleaned_poe2db_data"
    FOLDER_ECONOMY_DATA = "economy_data"