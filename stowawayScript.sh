#!/bin/bash

clear

echo "The script starts now"
echo

pushd ../tools/stowaway/stowaway/Stowaway-1.2.4

FILES=../apkFiles/*
for f in $FILES
do
	APK="apkOutput/"
	OUTPUT="_output"
	OUTPUT_FOLDER=$APK${f#../apkFiles/}$OUTPUT
	echo $f
	echo $OUTPUT_FOLDER

	bash stowaway.sh $f ../$OUTPUT_FOLDER &>output.txt
done

popd

echo "all done with the script!"

exit
