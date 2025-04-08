import os
import argparse
import yaml # used for the config.yaml file that will need to be updated to trigger an ISA.
import json # for creating the options.json file 
import metadataBuilder as builder
import pageData as coordinate


def create_subdirs(dir_name):
    os.makedirs(f"../analysis/{dir_name}")
    print("Analysis directory created")
    # create the option file based on a config
    os.makedirs(f"../docs/{dir_name}")
    print("Pages directory created")
    #should make .qmd files instead.
    with open(f"../docs/example/page.html", mode = 'rb') as src_file:
        with open(f"../docs/{dir_name}/page.html", mode= "wb") as dest_file:
            # TODO: SHOULD CHANGE THIS SUCH THAT THE TOP PARAMETERS ARE CHANGED.
            # reading and writing chunks at a time
            dest_file.write(src_file.read())

    print(f"Page.html copied to: ../docs/{dir_name}")
    return 0

def read_config():
    with open('../config.yaml', 'r') as file:
        config = yaml.safe_load(file) # reads the file 

    algorithms = config.get('algos', []) # saving algos parsing to the databuilder
    
    config.pop('algos', None) # removing algos as its the only field not pertaining to the options file
    
    dir_name = config.get('dir')
    config.pop('dir', None )

    create_subdirs(dir_name)

    with open(f'../analysis/{dir_name}/options.json', mode = 'w') as json_file:
        json.dump(config, json_file, indent=4)


    print("Options File created saved")
    return algorithms, dir_name

def main():
    algos, dir_name = read_config()
    output_dir = os.path.abspath(f"../analysis/{dir_name}")
    success = builder.make_file(algos, output_dir)
    if success:
        os.system(f"isa -r ../analysis/{dir_name}")
        coordinate.makefile(f"../docs/{dir_name}", f"../analysis/{dir_name}")

if __name__ == "__main__":
    main()
