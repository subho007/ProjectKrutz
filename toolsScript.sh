#!/bin/bash

clear

echo "The script starts now"
echo

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

#conn=sqlite3.connect('Evolution of Android Applications.sqlite')
#c=$conn.cursor()
#try:
	#add the column to the databse if it doesn't exist
#    c.execute('ALTER TABLE Evolution of Android Applications ADD COLUMN COLNew text;')
#	c.execute('INSERT INTO Permissions (perm1, perm2, perm3) VALUES(?,?,?)', ('true','false','true'))
	
#except:
#    pass # handle the error
#$c.close()

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
