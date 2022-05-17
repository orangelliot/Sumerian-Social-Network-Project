# Nicholas J Uhlhorn
# May 2022
# A shell script to automate making the database on a local machine

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

########## Check for direcories ##########

# Check if the directorys exists and create them if not
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


########## Translated Texts ##########
# Link to untranslated Ur III period https://cdli.ucla.edu/tools/cdlifiles/cdli_ur3atf.zip
# Link to the translation pipline https://github.com/cdli-gh/Sumerian-Translation-Pipeline.git
# Download, parse, and translate the data as needed

# Check if the untranslated dir has atf files
count=$(find $UNTRANSLATED -maxdepth 1 -type f -name "*.atf" -printf x | wc -c)
if [ $count -gt 0 ]
then
    echo "$UNTRANSLATED has $count atf entries"
else
    echo "$UNTRANSLATED has no atf entries"
    read -p "Do you want to fetch the tablets from the Ur III period? (y/n default: n) " responce
    if [ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ] )
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
fi

# Check if the translated directory has conll entries to use
count=$(find $TRANSLATED -maxdepth 1 -type f -name "*.conll" -printf x | wc -c)
if [ $count -gt 0 ]
then
    echo "$TRANSLATED has $count conll entries"
else
    echo "$TRANSLATED has no conll entries"
    # Ask user if they want to create entries from untranslated data
    read -p "Do you want to create tranlsated files? (y/n defuault: n) " responce
    if [ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ] )
    then
        #TODO: get translation pipeline and run the files through
        echo "Unimplelmented atm"
    else
        # We do not have anything to add to the database
        read -p "Continue with making empty database? (y/n default:n) " responce
        if [ ! -z $responce ] && ( [ ${responce:0:1} == 'y' ] || [ ${responce:0:1} == 'Y' ] )
        then
            echo "Contunuing to creating database"
        else
            exit 0
        fi
    fi
fi

echo Contunuing

# MySQL installed
# 

# TODO: Setup database

# TODO: Add entries to the database