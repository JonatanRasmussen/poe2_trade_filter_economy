# process_mod_lists.py

import json
import os
from collections import defaultdict

def generate_unmerged_text_report(data):
    # Dictionary to group by: Category -> Affix_Type -> List of lines
    grouped_data = defaultdict(lambda: defaultdict(list))

    for category, mods in data.items():
        for mod in mods:
            affix = mod.get('Affix_Type', 'Unknown')

            # Replace newlines with a separator for clean single-line reading
            desc = mod.get('Description', '').replace('\n', ' | ')

            tags = mod.get('Tags', [])
            level = mod.get('Level_Req', '0')

            # Format the tags string (e.g., "[Elemental, Cold, Resistance]")
            tags_str = f"  [{', '.join(tags)}]" if tags else ""

            # Construct the final line
            line = f"{desc}{tags_str}  (iLvl: {level})"

            grouped_data[category][affix].append(line)

    # Reconstruct the text report
    output = []
    for category, affixes in grouped_data.items():
        output.append(f"=== {category.upper()} MODIFIERS ===")
        for affix, lines in affixes.items():
            output.append(f"\n[{affix}]")
            for line in lines:
                output.append(line)
        output.append("\n" + "="*40 + "\n")

    return "\n".join(output)

# --- Execution ---
if __name__ == "__main__":
    input_file = "cleaned_data.json"
    output_file = "unmerged_modifiers.txt"

    if not os.path.exists(input_file):
        print(f"Error: Could not find '{input_file}'. Please ensure the JSON file exists.")
    else:
        print(f"Reading data from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            cleaned_data = json.load(f)

        # Generate the text report
        text_report = generate_unmerged_text_report(cleaned_data)

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_report)

        print(f"Success! Unmerged modifiers have been saved to '{output_file}'.")