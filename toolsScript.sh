#!/bin/bash

clear

echo "The script starts now"
echo

if [ $(date +%u) -eq 1 ]
then
        echo "today is Monday"
        #srapy scrape
elif [ $(date +%u) -eq 2 ]
then
        echo "today is Tuesday"
elif [ $(date +%u) -eq 3 ]
then
        echo "today is Wednesday"
elif [ $(date +%u) -eq 4 ]
then
        echo "today is Thursday"
elif [ $(date +%u) -eq 5 ]
then
        echo "today is Friday"
fi

pushd ./tools/stowaway/Stowaway-1.2.4

cd ../
rm -rf apkOutput
mkdir apkOutput
cd Stowaway-1.2.4

FILES=../../testAndroidApps/*
for f in $FILES
do
        APK="../apkOutput/"
        OUTPUT="_output"
        O_F=$APK${f#../../testAndroidApps/}
              OUTPUT_FOLDER=${O_F%.apk}$OUTPUT

        echo "*************************************"
        echo $f
        echo $OUTPUT_FOLDER
        pwd
        echo "*************************************"

        mkdir $OUTPUT_FOLDER

        bash ./stowaway.sh $f $OUTPUT_FOLDER&>../../../output.txt
done

popd

echo
pushd ./scraper
echo "Inserting into the database now"
sqlite3 Evolution\ of\ Android\ Applications.sqlite  "INSERT INTO ApkInformation (Name,Version,Rating) VALUES ('ShannonsApp','1.0','5.0');"
sqlite3 Evolution\ of\ Android\ Applications.sqlite "SELECT Rating FROM ApkInformation WHERE Name = 'ShannonsApp'"
popd

echo "Starting Androguard"

pushd ./tools/androguard

FILES=../testAndroidApps/*
for f in $FILES
do
        echo "***********AndroRisk for $f******************"
        ./androrisk.py -m -i $f
        echo "***********AndroAPKInfo for $f **************"
        #./androapkinfo.py -i $f
done

popd

echo "all done with the script!"

exit
