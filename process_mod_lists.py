# process_mod_lists.py - DO NOT REMOVE THIS LINE FROM THE SCRIPT!!!

import json
import os
import re
from global_configs import GlobalConsts


def generate_ahk_format(data):
    output = []

    # Regex to find number ranges like (5-15) or (-10--5)
    # Group 1 is min, Group 2 is max
    range_pattern = r'\((-?\d+(?:\.\d+)?)-(-?\d+(?:\.\d+)?)\)'

    # Regex to find standalone numbers like:
    # 1
    # -5
    # 12.5
    number_pattern = r'-?\d+(?:\.\d+)?'

    # ONLY process the "normal" category
    normal_mods = data.get("normal", [])

    for mod in normal_mods:
        desc = mod.get('Description', '')

        # Find the max value from the first number range
        match = re.search(range_pattern, desc)

        if match:
            max_val = match.group(2)

            # Replace all number ranges in the description with '#' and also get rid of '+'
            formatted_desc = re.sub(rf'\+?{range_pattern}', '#', desc)

        else:
            # Handle fixed values like "+1% to Maximum Cold Resistance"
            number_match = re.search(number_pattern, desc)

            if number_match:
                max_val = number_match.group(0)

                # Replace only the first standalone number and also get rid of '+'
                formatted_desc = re.sub(
                    rf'\+?({number_pattern})',
                    '#',
                    desc,
                    count=1
                )
            else:
                # Fallback for modifiers with no numbers at all
                max_val = "-9999"
                formatted_desc = desc

        # Apply keyword replacements
        skip_modifier = False

        for old, new in GlobalConsts.KEYWORD_REPLACE.items():
            if old.lower() in formatted_desc.lower():
                if new == "":
                    skip_modifier = True
                    break

                # Case-insensitive replacement
                formatted_desc = re.sub(
                    re.escape(old),
                    new,
                    formatted_desc,
                    flags=re.IGNORECASE
                )

        if skip_modifier:
            continue

        # Append the 3 required lines
        output.append(GlobalConsts.ITEM_CATEGORY_ON_TRADESITE)
        output.append(formatted_desc)
        output.append(max_val)

    # Append the termination string
    output.append("END_OF_SCRIPT")

    return "\n".join(output)


# --- Execution ---
if __name__ == "__main__":
    input_folder = GlobalConsts.FOLDER_CLEANED_POE2DB_DATA
    input_file = os.path.join(input_folder, f"{GlobalConsts.FILE_NAME}.json")

    output_folder = GlobalConsts.FOLDER_AHK_INPUTS
    output_file = os.path.join(output_folder, f"{GlobalConsts.FILE_NAME}.txt")

    if not os.path.exists(input_file):
        print(
            f"Error: Could not find '{input_file}'. "
            "Ensure parse_raw_data.py was run first."
        )
    else:
        print(f"Reading data from {input_file}...")

        with open(input_file, 'r', encoding='utf-8') as f:
            cleaned_data = json.load(f)

        # Generate the AHK formatted text
        ahk_text = generate_ahk_format(cleaned_data)

        # Ensure output directory exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ahk_text)

        print(f"Success! AHK inputs have been saved to '{output_file}'.")