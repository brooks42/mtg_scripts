import os
import json

# need to read all of the cards from the card files directory and compile them into a single file of cards

# grab the cards from https://github.com/db-ygoresources-com/yugioh-card-history/tree/main/en and use this script to compile them into a single JSON file of all the cards

def combine_json_files(input_dir, output_file):
    combined_data = []

    # Iterate over all JSON files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    # If the file contains a list, extend; otherwise, append the object
                    if isinstance(data, list):
                        combined_data.extend(data)
                    else:
                        combined_data.append(data)
                except Exception as e:
                    # print(f"{e}")
                    pass
    
    # Write combined data to the output file
    with open(output_file, 'w') as out_f:
        json.dump(combined_data, out_f, indent=4)

    # print(f"Combined {len(combined_data)} entries into {output_file}")

if __name__ == "__main__":
    input_directory = "card_files"
    output_json = "yugioh_cards.json"
    combine_json_files(input_directory, output_json)
