import re
import csv
from constants import entity_unit_map, unit_standardization, allowed_units
import pandas as pd

def parse_entity_value(text, entity_type):
    if entity_type not in entity_unit_map:
        raise ValueError(f"Entity type '{entity_type}' is not valid.")
    units = '|'.join(map(re.escape, entity_unit_map[entity_type]))
    pattern = rf'(\d+(?:\.\d+)?)\s*({units})'
    matches = re.findall(pattern, text.lower())
    if matches:
        value, unit = matches[0]
        standardized_unit = unit_standardization.get(unit, unit)
        return f"{value} {standardized_unit}"
    return ""

def parse_entities(text_data):
    parsed_data = {}
    for image_file, text in text_data.items():
        print(f"Processing image: {image_file}")
        parsed_values = {}
        
        # Check if text is a string, if not, convert to string or skip
        if not isinstance(text, str):
            if pd.isna(text):  # Check if it's a NaN value
                print(f"Warning: Skipping {image_file} due to NaN value")
                continue
            else:
                text = str(text)  # Convert to string if it's a number
        
        original_text = text.lower()  # Convert to lowercase for case-insensitive matching
        
        for entity_type in entity_unit_map.keys():
            try:
                entity_value = parse_entity_value(original_text, entity_type)
                if entity_value:
                    parsed_values[entity_type] = entity_value
                    print(f"Found {entity_type}: {entity_value}")
                else:
                    print(f"No {entity_type} found in the text.")
            except ValueError as e:
                print(f"Error processing {entity_type} for {image_file}: {e}")
        
        # Check for unrecognized units
        words = re.findall(r'\b\w+\b', original_text)
        unrecognized_units = [word for word in words if word in allowed_units and not any(word in entity_unit_map[et] for et in entity_unit_map)]
        if unrecognized_units:
            print(f"Warning: Unrecognized units found in {image_file}: {', '.join(unrecognized_units)}")
        
        parsed_data[image_file] = parsed_values
    
    return parsed_data

def read_csv(file_path):
    text_data = {}
    encodings = ['utf-8', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', newline='', encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    text_data[row['image_file']] = row['extracted_text']
            print(f"Successfully read the CSV file using {encoding} encoding.")
            return text_data
        except UnicodeDecodeError:
            print(f"Failed to read with {encoding} encoding. Trying next...")
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}")
    
    raise ValueError("Unable to read the CSV file with any of the attempted encodings.")

def write_csv(file_path, parsed_data):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['image_file'] + list(entity_unit_map.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for image_file, parsed_values in parsed_data.items():
            row = {'image_file': image_file, **parsed_values}
            writer.writerow(row)

if __name__ == "__main__":
    input_csv = "ocr_output.csv"
    output_csv = "parsed_text_data.csv"

    try:
        # Read the text data from the input CSV file
        text_data = read_csv(input_csv)

        # Parse the entities from the text data
        parsed_data = parse_entities(text_data)

        # Write the parsed data to the output CSV file
        write_csv(output_csv, parsed_data)

        print(f"Parsed data has been written to {output_csv}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        