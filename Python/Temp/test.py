import os

def function():
    path = os.getcwd()
    path = path[:len(path) - 11]
    path = path + 'Dataset/Translated/'

    tablets = os.listdir(path)
    print(tablets[0][:7])

function()
