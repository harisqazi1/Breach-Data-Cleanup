#!/usr/bin/python3
import csv
import json
import pandas as pd
import argparse

parser = argparse.ArgumentParser(
                    prog='stockx_07_2019.py',
                    description='A script to cleanup the StockX breach. It grabs the following fields: Email Address, Username, First Name, Last Name, Hashed Password')
parser.add_argument('filename', help='The name of the breach file (unzipped)') 
parser.add_argument('-o', '--output', help='The type of output you want: CSV, JSON, or Both')
args = parser.parse_args()

file = args.filename #Taking the user input file and using that

def to_csv(file_name):
    # Specify the columns to read by their column number
    columns_to_read = [4, 5, 6, 7, 8]
    #Just adding a ".csv" to the end of the file name
    output_file = file_name + str(".csv")
    #These headers will be added after the fact; Based on line 17
    added_text = ["Email Address", "Username", "First Name", "Last Name", "Hashed Password"] 
    #Added encoding to bypass unicode decode error
    with open(file_name, 'r', encoding = "ISO-8859-1") as infile:
        #Replace added here to mitigate "NUL" errors in file
        reader = csv.reader((line.replace('\0','') for line in infile))
        with open(output_file, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(added_text)
            for row in reader:
                #Only output the columns we mentioned in line 17
                writer.writerow(row[i] for i in columns_to_read)

# # #Following works with DtypeWarning: Columns (10,11,15,22,24,25,26,31,32,33,34,35,42,43) have mixed types. Specify dtype option on import or set low_memory=False. error
# Keeping here as backup, just in case
# def to_csv(file_name):
#     dataframe1 = pd.read_csv(file_name, encoding = "ISO-8859-1")
#     dataframe1.to_csv('soletrade-users.csv', index = None, mode='a')

def to_json(file_name):
    json_file = file_name + str(".json")
    #Using chunks so RAM doesn't get used up a lot
    chunk_size = 1000
    chunk_index = 0
    # Specify the columns to read by their column number
    columns_to_read = [4, 5, 6, 7, 8]
    headers = ["Email Address", "Username", "First Name", "Last Name", "Hashed Password"] 

    for chunk in pd.read_csv(file_name, usecols=columns_to_read, chunksize=chunk_size, encoding = "ISO-8859-1"):
        chunk.columns = headers
        if chunk_index == 0:
            chunk.to_json(json_file, orient='records', lines=True)
        else:
            with open(json_file, 'r+') as file:
                file.seek(0, 2)
                chunk.to_json(file, orient='records', lines=True)
        chunk_index += 1
    return json_file

if args.output == "CSV":
    print("Outputting CSV")
    to_csv(file)
elif args.output == "JSON":
    print("Outputting to JSON")
    to_json(file)
elif args.output == "Both":
    print("Outputting to CSV and JSON")
    print("Outputting CSV")
    to_csv(file)
    print("Outputting to JSON")
    to_json(file)
else:
    print("Choose `CSV`, `JSON`, or `Both`.\nExiting")
    exit()