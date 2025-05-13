import os
import json # for creating the options.json file 
import metadataBuilder as builder
import pageData as coordinate
from ruamel.yaml import YAML # replaced pyyaml to guarantee that the .qmd files are read correctly.
from datetime import datetime

def create_subdirs(dir_name, author):
    os.makedirs(f"../Quarto/Analysis/{dir_name}")
    print("Page directory created")

    os.makedirs(f"../temp/{dir_name}")
    print("Temp folder for analysis created")
    
    # Read the original file
    with open(f"../Quarto/Analysis/Example/Example.qmd", 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extract YAML front matter (between ---)
    if lines[0].strip() == "---":
        yaml_end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        yaml_lines = lines[1:yaml_end]
        content_lines = lines[yaml_end+1:]
    else:
        raise ValueError("No YAML front matter found")

    yaml = YAML()
    yaml_data = yaml.load("".join(yaml_lines))

    # Update values
    yaml_data['title'] = dir_name
    yaml_data['author'] = author
    yaml_data['date'] = datetime.now().strftime("%B %d, %Y")

    # Write new file
    with open(f"../Quarto/Analysis/{dir_name}/page.qmd", 'w', encoding='utf-8') as file:
        file.write("---\n")
        yaml.dump(yaml_data, file)
        file.write("---\n")
        file.writelines(content_lines)

    print(f"page.qmd copied to: ../Quarto/Analysis/{dir_name}")
    return 0

def read_config():
    with open('../config.yaml', 'r') as file:
        yaml = YAML()
        config = yaml.load(file) # reads the file 

    algorithms = config.get('algos', []) # saving algos parsing to the databuilder

    
    config.pop('algos', None) # removing algos as its the only field not pertaining to the options file
    
    dir_name = config.get('dir')
    config.pop('dir', None )

    author = config.get('author')
    config.pop('author', None )

    create_subdirs(dir_name, author)

    with open(f'../temp/{dir_name}/options.json', mode = 'w') as json_file:
        json.dump(config, json_file, indent=4)


    print("Options File created saved")
    return algorithms, dir_name

def main():
    algos, dir_name = read_config()
    output_dir = os.path.abspath(f"../temp/{dir_name}")
    success = builder.make_file(algos, output_dir)
    if success:
        os.system(f"isa -r ../temp/{dir_name}")
        coordinate.makefile(f"../Quarto/Analysis/{dir_name}", f"../temp/{dir_name}")

if __name__ == "__main__":
    main()
