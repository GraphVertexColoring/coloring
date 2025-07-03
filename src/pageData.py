# pageData.py
# Copyright (c) 2025 Frederik M. Dam
# This file is licensed under the MIT License.
# See the LICENSE file in the project root for full license text.

import os
import os.path
import csv
import argparse
import pandas as pd


# grabs the coordinates from a file path specified
# the coordinate index in the pyhard file matches the metadata indices.
def gatherData(path):
    coordinate_dict = {}

    # Grabs the coordinates and associates them with the index which matches the ones in the metadata.csv file
    with open(f"{path}/coordinates.csv", mode='r', newline='',encoding='utf-8') as file:
        reader = csv.DictReader(file) #reading the file in CSV format.
        for row in reader:
            key = row['Row']
            row.pop('Row')
            coordinate_dict[key] = row

    #Uses the metadata.csv to grab the source instance for each row.
    with open(f"{path}/metadata.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['instances']
            coordinate_dict[key]['instance_name'] = row['source']

    # Grabs the beta easy/hard value
    with open(f"{path}/beta_easy.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            coordinate_dict[row['Row']]['IsBetaEasy'] = row['IsBetaEasy']

    # Grabs the number of good algorithms and associate it with the intances.
    with open(f"{path}/good_algos.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            coordinate_dict[row['Row']]['NumGoodAlgos'] = row['NumGoodAlgos']

    # Grabs the processed features, meaining the normalized features
    with open(f"{path}/feature_process.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['Row']
            if key in coordinate_dict:
                for feature, value in row.items():
                    if feature != 'Row' and feature != 'source':
                        coordinate_dict[key][feature] = value
    
    with open(f"{path}/feature_raw.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['Row']
            if key in coordinate_dict:
                for feature, value in row.items():
                    if feature != 'Row' and feature != 'source':
                        coordinate_dict[key][f"{feature}_raw"] = value

    # Grabs the raw performance values of the algorithms
    with open(f"{path}/algorithm_raw.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['Row']
            if key in coordinate_dict:
                for algo, value in row.items():
                    if algo != 'Row':
                         coordinate_dict[key][f"{algo}_perf"] = value
    
    # Grabs the algorithms binary performances
    with open(f"{path}/algorithm_bin.csv", mode="r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['Row']
            if key in coordinate_dict: # only adds for the ones that actually exist in the instance list.
                for algo, value in row.items():
                    if algo != 'Row':
                        coordinate_dict[key][f"{algo}_bin"] = value

    return coordinate_dict

def makefile(filepath, path):
    dict = gatherData(path)
    
    # Ensure 'instance_name' is the first column
    feature_names = ['instance_name'] + [feature for feature in next(iter(dict.values())).keys() if feature != 'instance_name']
    
    #creates the csv file in case its usefull.
    with open(f"{filepath}/data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(feature_names)

        for key, values in dict.items():
            row = [values['instance_name']] + [values[feature] for feature in feature_names if feature != 'instance_name']
            writer.writerow(row)

    print(f"files: {filepath}/data.csv created")

    df = pd.read_csv(f"{filepath}/data.csv")
    df.head()

    data = df.to_json(orient="records", indent = 4)
    js_content = f"const jsonData = {data};"
    with open(f"{filepath}/data.js", "w") as file:
        file.write(js_content)
    print ("data.js created")

    os.remove(f"{filepath}/data.csv")


if __name__== "__main__":
    parser = argparse.ArgumentParser(description="generates inputfile for plot")
    parser.add_argument("--input", required=True, help="Path to the input directory, containing results from ISA")
    parser.add_argument("--o", required=True, help="Path to the desired output file")
    args = parser.parse_args()
    makefile(args.o,args.input)