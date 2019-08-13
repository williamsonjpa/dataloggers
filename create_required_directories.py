#!/home/joe/miniconda3/bin/python3

import os

def create_directories(root):

	directory_list = [ '/Data/Converted' , '/Data/AddedInfo' ,'/Data/Appended' ,'/Data/Edited' ,'/Data/Vegetation' ,'/Data/Raw' , '/Data/Final' , \
	 '/Data/ProblemFiles/BatteryErrors' , '/Data/ProblemFiles/CollectionDuplicateMatchErrors' , '/Data/ProblemFiles/CollectionNoMatchErrors' , \
	 '/Data/ProblemFiles/SetupDuplicateMatchErrors' , '/Data/ProblemFiles/SetupNoMatchErrors' , '/Data/DungBeetle' ]

	for i in directory_list:
		try:
		    # Create target Directory
		    dirName = root + i
		    os.mkdir(dirName)
		    print("Directory " , dirName ,  " Created ") 

		except FileExistsError:
			pass

	print('Required directories created.')
