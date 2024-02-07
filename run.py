import argparse
import os
import json
import shutil
import datetime
from pathlib import Path
import logging


date = (datetime.datetime.now().date())
logging.basicConfig(filename='Logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def info_logs(file,source,destination):
    logging.info(f" '{file}' Moved from '{source}' to '{destination}' ")



def validate_path(config_file, sourcedir, targetdir):
    file_flag = False
    sourcedir_flag = False
    targetdir_flag = False
    file = Path(config_file)
    sourcedir = Path(sourcedir)
    targetdir = Path(targetdir)
    
    #Below code will set flag true if file is in json format only otherwise flag will be false
    if file.is_file():
        if file.suffix == ".json":
            file_flag = True
            
        else:
            print("config file must be json")
            exit()
    else:
        print( file.stem +file.suffix+" Not foud and give location")
        exit()
    
    
    if sourcedir.is_dir():
        sourcedir_flag = True
        # print("source dir found")
    else:
        print(f"source dir not found with {sourcedir}")
        exit()
    
    if targetdir.is_dir():
        targetdir_flag = True
        # print("Target dir found")
    else:
        print(f"Target dir not found with {targetdir}")
        exit()

    return file_flag and sourcedir_flag  and targetdir_flag

def delete_file(file_path):
    file_to_delete = (Path(file_path))
    file_to_delete.unlink()

def file_org(config_file, source, target ):
    path_validation = False
    path_validation = validate_path(config_file, source, target)

    if path_validation:
       
        with open(config_file) as rules_file:
            config = json.load(rules_file)

            for rule in config['rules']:
                
                extension = rule['extension']
                category = rule['category']
                destinationpath = os.path.join(target , category)

                os.makedirs(destinationpath, exist_ok=True)

                for file in (os.listdir(source)):
                       
                        file = (file.lower())
                        if file.endswith(extension):
                            sourcepath = os.path.join(source,file)
                            try:
                                print(f"Moving : '{file}'")
                                # shutil.move(sourcepath,destinationpath)
                                info_logs(file,source,destinationpath)
                            except Exception as e:
                                file_path = (destinationpath+'/'+file)
                                userip = input(F"do you want to replace {file} enter Y")
                                if userip in ['y','Y']:
                                    delete_file(file_path)
                                    print(f"Moving : '{file}'")
                                    # shutil.move(sourcepath,destinationpath)
                                    info_logs(file,sourcepath,destinationpath)


                                
def main():
    print()
    parser = argparse.ArgumentParser(description="file orgnizor")
    parser.add_argument('config',type=str,help='Rules for file based on file extension')
    parser.add_argument('source_folder',type=str,help='folder from where files will be taken')
    parser.add_argument('destination_folder',type=str,help='after processing files will be stored')

    args = parser.parse_args()

    file_org(config_file=args.config, source=args.source_folder, target=args.destination_folder)
    

main()

print("\ncompleted.")