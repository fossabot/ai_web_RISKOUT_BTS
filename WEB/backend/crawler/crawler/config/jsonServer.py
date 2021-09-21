import os

def get_navernews():
    path= os.path.dirname(os.path.realpath(__file__))
    return path + "/navernews.json"

def get_naverlist():
    path= os.path.dirname(os.path.realpath(__file__))
    return path + "/naverlist.json"