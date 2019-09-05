"""
This file creates the directory structure required for this particular project
"""

import os

ROOT_DIR = os.getcwd()
NOTEBOOKS = "{}/notebooks/".format(ROOT_DIR)
MODELS = "{}/models/".format(ROOT_DIR)
DATA = "{}/data/".format(ROOT_DIR)
UTILS = "{}/utils".format(ROOT_DIR)
TRAIN = "{}/train".format(ROOT_DIR)

def create_dir():
    print("creating project directory ...")
    os.mkdir(NOTEBOOKS)
    os.mkdir(MODELS)
    os.mkdir(DATA)
    os.mkdir(UTILS)
    os.mkdir(TRAIN)
    print("project directory created")
    
if __name__ == "__main__":
    create_dir()