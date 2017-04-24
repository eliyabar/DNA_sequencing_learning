#!/bin/bash

DIR=$(dirname $0)
FREEC_PATH=/home/rotemsd/Desktop/FinalProject/FREEC-9.7b/src/freec
OUTPUT_PATH=/home/rotemsd/Desktop

# print usage parameters
usage()
{
    echo "usage: [-f | --file <PATH TO FILE>]"
}

# check for arguments
if [ "$1" == "" ]; then
	usage
    	exit 1
fi


while [ "$1" != "" ]; do
    case $1 in
        -f | --file )           shift
                                file=$1
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [[ ("$file" == "")]]; then
	usage
    	exit 1
fi

array=() # Create array
while IFS= read -r line # Read a line
do
	array+=("$line") # Append line to the array
done < "$file"

RESULTS_PATH=$OUTPUT_PATH/outputResults/

if [ ! -d $RESULTS_PATH ]
	then mkdir $RESULTS_PATH
fi

# printf '%s\n' "${array[@]}"

# create config file
for ((i = 0; i < ${#array[@]}; ++i)); do

	path=${array[$i]}
	fileName=$(basename $path)
	fileName="${fileName%.*}"
	mainfolder="id_${i}_${fileName}"

	mkdir $RESULTS_PATH/$mainfolder

	#printf '%s\n' "${path}"
	
	sex="XY"

	sed -i "s@mateFile =.*@mateFile = ${path}@" config.txt

	sed -i "s@sex =.*@sex = ${sex}@" config.txt

    # configuration for window size 100
	outputDir=$RESULTS_PATH/$mainfolder/window100/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 100/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w100.txt

	$FREEC_PATH -conf $outputDir/config_w100.txt	
done

# end of script
