# Nicholas J Uhlhorn
# May 2022
# A shell script to automate making the database on a local machine

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
# Path to untranslated data
UNTRANSLATED=$"$SCRIPTPATH/Dataset/Untranslated"
# Path to translated data
TRANSLATED=$"$SCRIPTPATH/Dataset/Test" #!!!! CHANGE THIS FROM TEST

# TODO: Check for dependencies and fetch them if they are not there
# Untranslated? if so we might want to run it through the pipline
# The dataset, or a dataset

# Check if the directory exists and create it if not
if [ -d "$TRANSLATED" ]
then
    echo "$TRANSLATED exists"
else
    echo "Creating $TRANSLATED"
    mkdir -p -- "$TRANSLATED"
fi

# Check if the directory has conll entries to use
count=$(find $TRANSLATED -maxdepth 1 -type f -name "*.conll" -printf x | wc -c)
if [ $count -gt 0 ]
then
    echo "$TRANSLATED has $count conll entries"
else
    echo "$TRANSLATED has no conll entries"
    # Ask user if they want to create entries from untranslated data
    read -p "Do you wish to create tranlsated files? (y/n defuault: n) " responce
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