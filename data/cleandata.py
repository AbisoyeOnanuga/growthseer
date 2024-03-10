import csv


input_file = 'Temperature-Change-on-Land_en_3-9-2024.csv'

output_file = 'Temperature-Change-on-Land.csv'


# List of column names to keep

keep_cols = ['Area', 'Element', 'Year', 'Unit', 'Value', 'Flag', 'Flag Description'] 


# Open input CSV file as read only

with open(input_file, 'r') as read_obj:

    # Open output CSV file for writing 

    with open(output_file, 'w', newline='') as write_obj:

        # Create a csv.DictReader object 

        csv_reader = csv.DictReader(read_obj)

        # Create a csv.DictWriter object 

        csv_writer = csv.DictWriter(write_obj, fieldnames=keep_cols)

        # Write headers

        csv_writer.writeheader()

        

        # Loop through rows and only write keep_cols to output

        for row in csv_reader:

            csv_writer.writerow({col:row[col] for col in keep_cols})