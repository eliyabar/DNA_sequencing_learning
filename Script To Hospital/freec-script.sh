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

    # configuration for window size 500
	outputDir=$RESULTS_PATH/$mainfolder/window500/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 500/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w500.txt

	$FREEC_PATH -conf $outputDir/config_w500.txt

    # configuration for window size 10000
	outputDir=$RESULTS_PATH/$mainfolder/window10000/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 10000/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w10000.txt

	$FREEC_PATH -conf $outputDir/config_w10000.txt

    # configuration for window size 50000
	outputDir=$RESULTS_PATH/$mainfolder/window50000/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 50000/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w50000.txt

	$FREEC_PATH -conf $outputDir/config_w50000.txt

    # configuration for window size 50
	outputDir=$RESULTS_PATH/$mainfolder/window50/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 50/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w50.txt

	$FREEC_PATH -conf $outputDir/config_w50.txt

    # configuration for window size 25
	outputDir=$RESULTS_PATH/$mainfolder/window25/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 25/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w25.txt

	$FREEC_PATH -conf $outputDir/config_w25.txt

    # configuration for window size 10
	outputDir=$RESULTS_PATH/$mainfolder/window10/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 10/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w10.txt

	$FREEC_PATH -conf $outputDir/config_w10.txt

    # configuration for window size 2
	outputDir=$RESULTS_PATH/$mainfolder/window2/

	mkdir $outputDir
	
	sed -i "s/window =.*/window = 2/" config.txt

	sed -i "s@outputDir =.*@outputDir =${outputDir}@" config.txt

	cp config.txt $outputDir/config_w2.txt

	$FREEC_PATH -conf $outputDir/config_w2.txt
	
done

# end of script
