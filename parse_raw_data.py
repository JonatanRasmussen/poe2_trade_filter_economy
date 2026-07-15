# parse_raw_data.py - DO NOT REMOVE THIS LINE FROM THE SCRIPT!!!

import re
import json
import html
import os
from global_configs import GlobalConsts

def clean_poe_text(raw_text):
    """Removes HTML tags and unescapes HTML entities to return clean text."""
    if not isinstance(raw_text, str):
        return raw_text

    # Replace <br> with a newline or space so sentences don't mash together
    text = re.sub(r'<br\s*/?>', '\n', raw_text)

    # Replace the specific em-dash span with a standard dash
    text = text.replace('<span class="ndash">—</span>', '-')

    # Remove all remaining HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Unescape HTML entities (e.g., &lt; to <)
    return html.unescape(text)

def parse_poe2db_script(script_content):
    # 1. Extract the JSON payload from the JavaScript wrapper
    match = re.search(r'new ModsView\((\{.*?\})\);', script_content, re.DOTALL)
    if not match:
        raise ValueError("Could not find the JSON payload in the provided text. Make sure the file contains the 'new ModsView({...});' block.")

    json_str = match.group(1)
    raw_data = json.loads(json_str)

    # 2. Extract mappings (Prefix/Suffix)
    gen_types = raw_data.get('gen', {})
    gen_types["5"] = "Corrupted Implicit"

    # 3. Define the categories we want to extract
    categories = ['normal', 'corrupted', 'desecrated', 'liquid']
    organized_data = {}

    for category in categories:
        if category not in raw_data or not raw_data[category]:
            continue

        organized_data[category] = []

        for mod in raw_data[category]:
            gen_id = str(mod.get('ModGenerationTypeID', ''))
            affix_type = gen_types.get(gen_id, f"Unknown Type ({gen_id})")

            description = clean_poe_text(mod.get('str', ''))
            name = clean_poe_text(mod.get('Name', mod.get('Code', 'Unknown')))
            tags = [clean_poe_text(tag) for tag in mod.get('mod_no', [])]

            clean_mod = {
                "Name": name,
                "Affix_Type": affix_type,
                "Level_Req": mod.get('Level'),
                "Mod_Families": mod.get('ModFamilyList', []),
                "Tags": tags,
                "Description": description
            }

            organized_data[category].append(clean_mod)

    return organized_data

# --- Execution ---
if __name__ == "__main__":
    input_file = GlobalConsts.FILE_RAW_DATA_INPUT

    # Ensure output directory exists
    output_folder = GlobalConsts.FOLDER_CLEANED_POE2DB_DATA
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f"{GlobalConsts.FILE_NAME}.json")

    if not os.path.exists(input_file):
        print(f"Error: Could not find '{input_file}'. Please create it and paste your raw data inside.")
    else:
        print(f"Reading data from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_file_content = f.read()

        try:
            cleaned_data = parse_poe2db_script(raw_file_content)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

            print(f"Success! Cleaned data has been saved to '{output_file}'.")

        except json.decoder.JSONDecodeError as e:
            print(f"JSON Parsing Error: {e}")
            print("The extracted text was not valid JSON. Please ensure your raw_data.txt contains the exact script block.")