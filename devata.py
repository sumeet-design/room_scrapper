# this script will join the contents of the file
import json

combinations = {
    'CHAPTER HIGHBURY': [
        'SEP 24 - JUL 25 (44 WEEKS)',
        'SEP 24 - AUG 25 (51 WEEKS)',
    ]
}

import json

def combine_dicts(d1, d2):
    if len(d1) == len(d2):
        combined_list = []

        # Iterate through both lists simultaneously
        for dict1, dict2 in zip(d1, d2):
            combined_dict = {}

            # Merge the dictionaries at each index
            combined_dict.update(dict1)
            combined_dict.update(dict2)

            combined_list.append(combined_dict)

        return combined_list
    else:
        print("Lengths of the lists are not the same")
        return None


def write_to_json(data, output_file):
    # Write the data to the new JSON file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

    print("Data has been written to:", output_file)

def load_json(file_name):
    dictionary = {}
    with open(file_name, 'r') as file:
        dictionary = json.load(file)
    return dictionary



for chapter, periods in combinations.items():
    # get key from both the files
    for period in periods:
        key = f'{chapter}-{period}'
        quick_view_file = f'{key}.quick_view.json'
        apply_view_file = f'{key}.apply_view.json'
        quick_view_dict = load_json(quick_view_file)
        apply_view_dict = load_json(apply_view_file)
        the_dict = combine_dicts(quick_view_dict[key], apply_view_dict[key])
        write_to_json(the_dict, f'combined_data/{key}.json')





