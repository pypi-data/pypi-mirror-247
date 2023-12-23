import pkgutil
import os
import shutil

def get_iris():
    data = pkgutil.get_data(__name__, "datasets/iris.csv")
    return data
def get_bostonhousing():
    data = pkgutil.get_data(__name__, "datasets/BostonHousing.csv")
    return data
def get_heartdisease():
    data = pkgutil.get_data(__name__, "datasets/heartdisease.csv")
    return data
def get_penguins():
    data = pkgutil.get_data(__name__, "datasets/penguins.csv")
    return data
def get_titanic():
    data = pkgutil.get_data(__name__, "datasets/titanic.csv")
    return data

def get_datasets_dirpath():
    fullpath = os.path.join(os.path.dirname(__file__),'datasets')
    return fullpath

def get_datasets_filepath(filename):
    filepath = os.path.join(os.path.dirname(__file__),'datasets')
    filepath = os.path.join(filepath,filename)
    if os.path.exists(filepath):
        return filepath
    else:
        return "There is no file ("+filepath+")"

def save_datasets_file(filename,savepath):
    filepath = os.path.join(os.path.dirname(__file__), 'datasets')
    filepath = os.path.join(filepath, filename)
    try:
        shutil.copyfile(filepath,savepath)
        return True
    except Exception as e:
        print(e)
        return False