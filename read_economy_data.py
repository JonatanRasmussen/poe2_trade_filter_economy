# read_economy_data.py - DO NOT REMOVE THIS LINE FROM THE SCRIPT!!!

import os
import re
import math
from collections import defaultdict
from global_configs import GlobalConsts

def parse_age_to_hours(age_str):
    """
    Converts Path of Exile trade site age strings into approximate hours.
    Examples: "5 weeks ago", "last month", "15 hours ago", "a minute ago"
    """
    age_str = age_str.lower()

    # Under an hour
    if 'second' in age_str or 'minute' in age_str:
        return 0

    # Determine the time multiplier in hours
    multiplier = 1
    if 'hour' in age_str:
        multiplier = 1
    elif 'day' in age_str:
        multiplier = 24
    elif 'week' in age_str:
        multiplier = 168
    elif 'month' in age_str:
        multiplier = 720
    elif 'year' in age_str:
        multiplier = 8760
    else:
        return 0  # Fallback if time period is unrecognizable

    # Handle singular/edge cases like "an hour ago", "a day ago", "last week"
    if 'a ' in age_str or 'an ' in age_str or 'last' in age_str:
        return multiplier

    # Extract the explicit number if present (e.g., the '5' in '5 weeks')
    nums = re.findall(r'\d+', age_str)
    if nums:
        return int(nums[0]) * multiplier

    return multiplier

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

        # 2. Detect the Asking Price & Age
        if line == "Asking Price:" and current_mod:
            # Check if we have enough lines ahead for price and listing age
            if i + 2 < len(lines):
                price_line = lines[i+1].strip()
                age_line = lines[i+2].strip()

                # FIX: Explicitly match known currencies to avoid mashed text like "divineDivine"
                match = re.search(r'([\d\.]+)\s*×\s*(divine|chaos|exalted|exalt)', price_line, re.IGNORECASE)
                if match:
                    amount = float(match.group(1))
                    currency = match.group(2).lower()

                    # Extract the age string (e.g. "n0wimn0thing#5519 listed 5 weeks ago")
                    age_match = re.search(r'listed\s+(.+)', age_line, re.IGNORECASE)
                    age_str = age_match.group(1) if age_match else ""
                    age_hours = parse_age_to_hours(age_str)

                    mods_data[current_mod].append((amount, currency, age_hours))

                i += 3  # Skip the parsed lines
                continue

        i += 1

    # 3. Summarize Data
    conversion_to_exalt = {
        'chaos': 50.0,
        'divine': 400.0,
        'exalted': 1.0,
        'exalt': 1.0
    }

    # List to store processed summaries before printing
    summaries = []

    for mod, prices in mods_data.items():
        exalt_prices = []

        for amount, currency, age_hours in prices:
            rate = conversion_to_exalt.get(currency, 0)
            if rate > 0:
                exalt_prices.append((amount * rate, amount, currency, age_hours))

        if not exalt_prices:
            continue

        # Sort by converted Exalt value to easily find the lowest/cheapest
        exalt_prices.sort(key=lambda x: x[0])

        lowest = None
        age_label = ""

        # Priority 1: Lowest price that is >= 24 hours old
        for p in exalt_prices:
            if p[3] >= 24:
                lowest = p
                age_label = "[>= 24h old]"
                break

        # Priority 2: Lowest price that is > 1 hour old
        if not lowest:
            for p in exalt_prices:
                if p[3] > 1:
                    lowest = p
                    age_label = "[> 1h old]"
                    break

        # Priority 3: Absolute lowest price (regardless of age)
        if not lowest:
            lowest = exalt_prices[0]
            age_label = "[Any age]"

        # Average of the cheapest items based on sqrt(total items) rounded up
        num_items = len(exalt_prices)
        subset_count = math.ceil(math.sqrt(num_items))
        subset_count = max(1, subset_count)  # Failsafe to ensure we don't divide by 0

        cheapest_subset = exalt_prices[:subset_count]
        avg_exalt = sum(x[0] for x in cheapest_subset) / subset_count

        # Append to our summary list
        summaries.append({
            'mod': mod,
            'num_items': num_items,
            'lowest_exalt_value': lowest[0],
            'lowest_amount': lowest[1],
            'lowest_currency': lowest[2].capitalize(),
            'age_label': age_label,
            'avg_exalt': avg_exalt,
            'subset_count': subset_count
        })

    # Sort the summaries by lowest price in descending order (highest price first)
    summaries.sort(key=lambda x: x['avg_exalt'], reverse=True)

    # 4. Print Data
    print(f"\n{'='*50}")
    print(f" ECONOMY SUMMARY FOR: {GlobalConsts.FILE_NAME}")
    print(f"{'='*50}")

    if not summaries:
        print("No valid price data found. Ensure the copy-paste format is correct.")
        return

    for s in summaries:
        print(f"\nMod: {s['mod']}")
        print(f"  Total Listings : {s['num_items']}")
        print(f"  Lowest Price   : {s['lowest_amount']:g} {s['lowest_currency']} ({s['lowest_exalt_value']:.2f} Exalts) {s['age_label']}")
        print(f"  Average Price  : {s['avg_exalt']:.2f} Exalts (avg of the cheapest {s['subset_count']} item{'s' if s['subset_count'] > 1 else ''})")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    parse_and_summarize_economy()