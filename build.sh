# Nicholas J Uhlhorn
# May 2022
# A shell script to automate making the database on a local machine

########## CONSTANT VARIABLES ##########
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
# Path to untranslated data
UNTRANSLATED=$"$SCRIPTPATH/Dataset/TestUntranslated"
# Path to translated data
TRANSLATED=$"$SCRIPTPATH/Dataset/TestTranslated" #!!!! CHANGE THIS FROM TEST
# URL to Ur III period cdli data
CDLIDATA=$"https://cdli.ucla.edu/tools/cdlifiles/cdli_ur3atf.zip"

########## User Prompt Variables #########
grabUntranslatedData=1
translatedUntranslatedData=1
removePipeline=1
buildDatabase=1
populateDatabase=1

########## Check for directories ##########

# Check if the directories exists and create them if not
if [ -d "$UNTRANSLATED" ]
then
    echo "$UNTRANSLATED exists"
else
    echo "Creating $UNTRANSLATED"
    mkdir -p -- "$UNTRANSLATED"
fi

if [ -d "$TRANSLATED" ]
then
    echo "$TRANSLATED exists"
else
    echo "Creating $TRANSLATED"
    mkdir -p -- "$TRANSLATED"
fi

##################################
########## User Prompts ##########
##################################
# Get all prompts from the user before doing anything this way the whole 
# script can be run without extra input from the user

# Find untranslated file count
count=$(find $UNTRANSLATED -maxdepth 1 -type f -name "*.atf" -printf x | wc -c)
echo "Found $count .atf files in the untranslated directory"
if [ ! $count -gt 0 ]
then
    read -p "Do you want to download the UrIII data set? (y/n default:n) " responce
    [ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ])
    grabUntranslatedData=$?
fi

# Find translated file count
count=$(find $TRANSLATED -maxdepth 1 -type f -name "*.conll" -printf x | wc -c)
echo "Found $count .conll files in the translated directory"
if [ ! $count -gt 0 ]
then
    read -p "Do you want to translate the untranslated data set? (y/n default:n) " responce
    [ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ])
    translatedUntranslatedData=$?
fi

# Ask if pipeline should be removed after translation
if [ $translatedUntranslatedData = 0 ]
then
    read -p "Do you want to remove the pipeline after translation? (y/n default:n) " responce
    [ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ])
    removePipeline=$?
fi

# Ask if the database will be built
read -p "Do you want to build the database? (y/n default:n) " responce
[ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ])
buildDatabase=$?

# Ask if the database will be populated (if it will be created)
if [ $buildDatabase == 0 ]
then
    read -p "Do you want to populate the database? (y/n default:n) " responce
    [ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ])
    populateDatabase=$?
fi

##################################
########## Build Script ##########
##################################

########## Translated Texts ##########
# Link to untranslated Ur III period https://cdli.ucla.edu/tools/cdlifiles/cdli_ur3atf.zip
# Link to the translation pipline https://github.com/cdli-gh/Sumerian-Translation-Pipeline.git

# Download and parse the untranslated data as needed
if [ $grabUntranslatedData = 0 ]
then
    # Get the file from cdli if it does not exist
    if [ -f "$UNTRANSLATED/UrIIItablets.zip" ]
    then
        echo "Zip file already downloaded"
    else
        curl -o $UNTRANSLATED/UrIIItablets.zip $CDLIDATA
    fi

    # Unzip the file
    unzip $UNTRANSLATED/UrIIItablets.zip -d $UNTRANSLATED/

    # Split the file into files and remove the default file
    g++ -std=c++17 -o dataSplitter $SCRIPTPATH/C++/DataCollection/splitUntranslated.cpp
    ./dataSplitter "$UNTRANSLATED/ur3_20110805_public.atf" "$UNTRANSLATED/"

    # Clean up the directory
    rm -r $UNTRANSLATED/__MACOSX # $UNTRANSLATED/UrIIItablets.zip
    rm $UNTRANSLATED/ur3_20110805_public.atf dataSplitter
fi

# Translate the data as needed
if [ $translatedUntranslatedData = 0 ]
then
    # Grab the translation pipeline from github if it is not present
    if [ ! -d "$SCRIPTPATH/Sumerian-Translation-Pipeline" ]
    then
        git clone https://github.com/cdli-gh/Sumerian-Translation-Pipeline.git
    fi
    # TODO: Translate the Untranslated data
fi

# Remove pipeline if requested
if [ $removePipeline = 0 ]
then
    rm -r "$SCRIPTPATH/Sumerian-Translation-Pipeline"
fi

# TODO: Check that MySQL is installed

# TODO: Setup database

# TODO: Add entries to the database