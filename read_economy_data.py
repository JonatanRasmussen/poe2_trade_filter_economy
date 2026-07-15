# read_economy_data.py - DO NOT REMOVE THIS LINE FROM THE SCRIPT!!!

import os
import re
from collections import defaultdict
from global_configs import GlobalConsts

def parse_and_summarize_economy():
    input_folder = GlobalConsts.FOLDER_ECONOMY_DATA
    input_file = os.path.join(input_folder, f"{GlobalConsts.FILE_NAME}.txt")

    if not os.path.exists(input_file):
        print(f"Error: Could not find economy data at '{input_file}'.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    mods_data = defaultdict(list)
    current_mod = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 1. Detect the AHK Header Block (e.g. "Jewel" followed by a line containing "#")
        if line == GlobalConsts.ITEM_CATEGORY_ON_TRADESITE:
            if i + 1 < len(lines) and '#' in lines[i+1]:
                current_mod = lines[i+1].strip()
                i += 3  # Skip the mod name and the max value line
                continue

        # 2. Detect the Asking Price
        if line == "Asking Price:" and current_mod:
            if i + 1 < len(lines):
                price_line = lines[i+1].strip()

                # FIX: Explicitly match known currencies to avoid mashed text like "divineDivine"
                match = re.search(r'([\d\.]+)\s*×\s*(divine|chaos|exalted|exalt)', price_line, re.IGNORECASE)
                if match:
                    amount = float(match.group(1))
                    currency = match.group(2).lower()
                    mods_data[current_mod].append((amount, currency))
                i += 2
                continue

        i += 1

    # 3. Summarize Data
    # 10 Exalt = 1 Chaos  => 1 Exalt = 0.1 Chaos
    # 100 Exalt = 1 Divine => 1 Divine = 10 Chaos
    conversion_to_chaos = {
        'chaos': 1.0,
        'divine': 10.0,
        'exalted': 0.1,
        'exalt': 0.1
    }

    print(f"\n{'='*50}")
    print(f" ECONOMY SUMMARY FOR: {GlobalConsts.FILE_NAME}")
    print(f"{'='*50}")

    if not mods_data:
        print("No valid price data found. Ensure the copy-paste format is correct.")
        return

    for mod, prices in mods_data.items():
        chaos_prices = []

        for amount, currency in prices:
            rate = conversion_to_chaos.get(currency, 0)
            if rate > 0:
                chaos_prices.append((amount * rate, amount, currency))

        if not chaos_prices:
            continue

        # Sort by converted Chaos value to find the lowest
        chaos_prices.sort(key=lambda x: x[0])
        lowest = chaos_prices[0]
        avg_chaos = sum(x[0] for x in chaos_prices) / len(chaos_prices)

        print(f"\nMod: {mod}")
        print(f"  Total Listings : {len(chaos_prices)}")
        print(f"  Lowest Price   : {lowest[1]:g} {lowest[2].capitalize()} ({lowest[0]:.2f} Chaos)")
        print(f"  Average Price  : {avg_chaos:.2f} Chaos")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    parse_and_summarize_economy()