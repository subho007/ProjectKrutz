#!/bin/bash

clear

echo "The script starts now"
echo

pushd ./tools/stowaway/Stowaway-1.2.4

FILES=../../testAndroidApps/*
for f in $FILES
do
	APK="apkOutput/"
	OUTPUT="_output"
	OUTPUT_FOLDER=$APK${f#../../testAndroidApps/}$OUTPUT

	echo $f
	echo $OUTPUT_FOLDER

	bash stowaway.sh $f ../$OUTPUT_FOLDER &>output.txt
done

popd

echo "Stowaway Complete"
echo "Starting Androguard"

pushd ./tools/androguard

FILES=../testAndroidApps/*
for f in $FILES
do
	./androrisk.py -m -i $f
done

popd

echo "all done with the script!"

exit
