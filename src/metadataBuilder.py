# metadataBuilder.py
# Copyright (c) 2025 Frederik M. Dam
# This file is licensed under the MIT License.
# See the LICENSE file in the project root for full license text.

# This program is meant to take .col files and extract feature data from them.
#   This involves reading data from the file, generating laplacian and adjacency graphs, and performing the necessary calculations.
import os
import os.path
import numpy as np
import csv
import time 
import argparse

##
# Reads the specified file and extracts the feature columns.
##
def gather_features(path):
    print("Calculating features")
    feature_dict = {}

    with open(path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['feature_source']
            row.pop('feature_source')
            feature_dict[key] = row

    return feature_dict 

##
# This opens the best.csv file and treat it as the solutions from an algorithm
#   This method assumes that all solutions passed to it are valid, this is done since i want to use the github action to check the validity of solutions instead.
#       Could consider having the action delete non valid solutions.
# The method also reads from the algoritm performance file and extracts information reguarding the valid algorithms.
##
def gather_algo_results(algos, path_to_csv): 
    print("Processing Algorithm results...")

    algo_dict = {}

    with open(path_to_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate through each row in the CSV
        for row in reader:
            instance_name = row['instance_name']
            algo_dict[instance_name] = {}

            # Extract the best known performance for this instance from the 'best' column
            algo_dict[instance_name]['best_performance'] = int(row['best_performance'])

            # Iterate through each algorithm column and add the performance data
            for algo in algos:
                if algo in row:
                    algo_dict[instance_name][algo] = float(row[algo]) if row[algo] else float('nan')
                else:
                    # If the algorithm column does not exist, set it to NaN
                    algo_dict[instance_name][algo] = float('nan')

            # If the "best" algorithm is known from the CSV, copy the value from the "best" column
            if 'best' in row:
                algo_dict[instance_name]['best'] = int(row['best'])

    return algo_dict

##
# Given the list of algorithms and a target directory, this method orcestrates the primary function of this script and collects all information in a file.
##
def make_file(algos, filepath): 
    # collect the dictionaries needed for file creation
    feature_dict = gather_features('../Resources/InstanceFeatures.csv') # A static file that should be updated when a new instance is added.
    algo_dict = gather_algo_results(algos, "../Resources/algoPerf.csv")

    algo_best = algos+ ['best'] # grabs the best as to calculate the performance ratio later.

    # get the features and algorithms used to create a header for a CSV file.
    feature_names = list(next(iter(feature_dict.values())).keys()) # gets the headers dynamically.
    header = [feature for feature in feature_names]
    algorithms = ['algo_' + s for s in algo_best] 

    with open(os.path.join(filepath, "metadata.csv") , mode="w", newline="") as file:
        writer = csv.writer(file)

    # write the headers on the first row, followed by the information from the dict on the following rows.
        writer.writerow(['instances', 'source'] + header + algorithms)
        iterator = 1 
        for instance_name, features in feature_dict.items():
            row = [
                iterator,                                 # Indexing
                instance_name                             # Instance name
            ] + list(features.values()) #dynamic addition of the features.

            # Generically adds the performances of the algorithms to the row.
            best_perf = algo_dict[instance_name]['best_performance']

            for algo in algo_best:
                algo_perf = algo_dict[instance_name][algo]
                if best_perf != 0: # avoids division by zero
                    perf_ratio = (algo_perf - best_perf) / best_perf
                    #print(perf_ratio)
                else: 
                    perf_ratio = float('nan')
                row.append(perf_ratio)

            writer.writerow(row)
            iterator += 1    


    print(f"file created in path: {filepath}")
    return True
    
def test():
    timestamp = time.time()
    algos = ['DSATUR'] 
    
    make_file(algos, "../analysis/test/metadata.csv")

    end = time.time()
    print(end - timestamp)
    
    os.chdir("../analysis/test")
    os.system("isa")

if __name__ == "__main__":
    #could for the page, just remove pyhard and instead only use pyispace, and then print the plots myself as i am already somewhat doing.
    parser = argparse.ArgumentParser(description=" This script takes a directory, a list of algorithms and a name for the outputfile, generating METADATA needed to perform ISA using pyhard")
    #could default to use all or simply the 5 thats been tested.
    parser.add_argument("--a", required=True, help="A list of algorithms to be used, names must correspond with the foldernames where the solution certificates are located, where a certificate must share a name with the instance it solves.")
    parser.add_argument("--o", required=True, help="path to the output directory")
    args = parser.parse_args()
    algos = args.a.split(",")
    make_file(algos, f"{args.o}")


