# Nicholas J Uhlhorn
# Sumerian Social Network Research Project
# September 2022

# import the library
from appJar import gui
import pandas as pd
import os
from PIL import Image, ImageTk


# import custom 

##### GUI Methods #####
def appendAutoText(btn):
    text = app.getEntry("autoNames") + "\n"
    app.setTextArea("textArea", text, callFunction = False)
    app.clearEntry("autoNames")

def setImgScale(sldr):
    zoom = app.getScale(sldr)
    app.zoomImage("graphImage", zoom)

def imageCreated():
    app.reloadImage('graphImage')

def generateImage():

    pass

##### GUI STRUCTURE #####
# create a GUI variable called app
app = gui("Sumerian DB for the Layman", "800x600")
app.setFont(12)

# Create widgets 
# Image FRAME START
app.startFrame("ImageFrame", row = 0, column = 0, colspan=2)
app.startScrollPane("ImagePane")
app.addImage("graphImage", "../../GraphicRepresentations/output/img/careers.png")
app.addLabel("Graph")
app.stopScrollPane()
app.addScale("Scale")
app.setScale("Scale", 1)
app.setScaleRange("Scale", -3, 3, 1)
app.setScaleChangeFunction("Scale", setImgScale)
app.stopFrame()
# Image FRAME END

# Entry FRAME START
app.startFrame("Entry", row = 1,  column = 1, sticky='NES')
# AutoEntry FRAME START
app.startFrame("AutoEntry", row = 0, column = 0, sticky='NE')
# Autofill name entry
df = pd.read_csv(f"Dataset/rawnameslist.csv")
app.addAutoEntry("autoNames", list(df['name']), column = 0, row = 0)
app.setAutoEntryNumRows("autoNames", 5)
# Add Button
app.addButton("Add", appendAutoText, row = 0, column = 1)
# END OF AutoEntry FRAME
app.stopFrame()
# Text area
app.addScrolledTextArea("textArea", rowspan = 1)
app.addButton("Generate", None)
# END OF Entry FRAME
app.stopFrame()

# start the GUI
app.go()