# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 13:23:45 2015

@author: jordan
"""

#Import whatever modules will be used
import os
import sys
import pdb
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.table import Column as Column
from astropy.io import fits, ascii
from scipy import stats
from pyPol import Image

#Setup the path delimeter for this operating system
delim = os.path.sep

#==============================================================================
# *********************** CUSTOM USER CODE ************************************
# this is where the user specifies where the raw data is stored
# and some of the subdirectory structure to find the actual .FITS images
#==============================================================================
# This is the location of the raw data for the observing run
reducedPath = '/home/jordan/ThesisData/PRISM_Data/Reduced_data/'

#Loop through each night and build a list of all the files in observing run
fileList = []
for file in os.listdir(reducedPath):
    # Check that the file is not actually a directory
    filePath = os.path.join(reducedPath, file)
    if not os.path.isdir(filePath):
        fileList.extend([os.path.join(reducedPath, file)])

#Sort the fileList
fileNums = [''.join((file.split(delim).pop().split('.'))[0:2]) for file in fileList]
sortInds = np.argsort(np.array(fileNums, dtype = np.int))
fileList = [fileList[ind] for ind in sortInds]

groupIndexDir = reducedPath + delim + 'GroupIndices'
if (not os.path.isdir(groupIndexDir)):
    os.mkdir(groupIndexDir, 0o755)


#==============================================================================
# ***************************** INDEX *****************************************
# Build an index of the file type and binning, and write it to disk
#==============================================================================
# Check if a file index already exists... if it does then just read it in
indexFile = 'fileIndex.csv'
if not os.path.isfile(indexFile):
    # Loop through each night and test for image type
    print('\nCategorizing files by groups.\n')
    startTime = os.times().elapsed
    
    # Begin by initalizing some arrays to store the image classifications
    obsType  = []
    name     = []
    binType  = []
    polAng   = []
    waveBand = []
    fileCounter = 0
    percentage  = 0
    
    #Loop through each file in the fileList variable
    for file in fileList:
        # Read in the image
        tmpImg = Image(file)
        
        # Classify each file type and binning
        tmpName = tmpImg.header['OBJECT']
        if len(tmpName) < 1:
            tmpName = 'blank'
        name.append(tmpName)
        polAng.append(tmpImg.header['POLPOS'])
        waveBand.append(tmpImg.header['FILTNME3'])
        
        # Test the binning of this file
        binTest  = tmpImg.header['CRDELT*']
        if binTest[0] == binTest[1]:
            binType.append(int(binTest[0]))
    
        # Count the files completed and print update progress message
        fileCounter += 1
        percentage1  = np.floor(fileCounter/len(fileList)*100)
        if percentage1 != percentage:
            print('completed {0:3g}%'.format(percentage1), end="\r")
        percentage = percentage1
        
    endTime  = os.times().elapsed
    numFiles = len(fileList)
    print(('\n{0} File processing completed in {1:g} seconds'.
           format(numFiles, (endTime -startTime))))
    
    # Write the file index to disk
    fileIndex = Table([fileList, name, waveBand, polAng, binType],
                      names = ['Filename', 'Name', 'Waveband', 'Polaroid Angle', 'Binning'])
    fileIndex.add_column(Column(name='Use',
                                data=np.ones((numFiles)),
                                dtype=np.int),
                                index = 0)
    
    # Group by "Name"
    groupFileIndex = fileIndex.group_by('Name')
    
    # Grab the file-number orderd indices for the groupFileIndex
    fileIndices = np.argsort(groupFileIndex['Filename'])
    
    # Loop through each "Name" and assign it a "Target" value
    targetList = []
    
    for group in groupFileIndex.groups:
        # Select this groups properties
        thisName = np.unique(group['Name'])
        
        # Test if the group name truely is unique
        if len(thisName) == 1:
            thisName = thisName[0]
        else:
            print('There is more than one name in this group!')
        
        # Count the number of elements in this group
        groupLen = len(group)
        
        # Add the "Target" column to the fileIndex
        thisTarget = input('\nEnter the target for group "{0}": '.format(thisName))
        thisTarget = [thisTarget]*groupLen
        
        # Add these elements to the target list
        targetList.extend(thisTarget)
    
    pdb.set_trace()
    groupFileIndex.add_column(Column(name='Target',
                                data=np.array(targetList)),
                                index = 2)
    # Re-sort by file-number
    fileSortInds = np.argsort(groupFileIndex['Filename'])
    fileIndex1   = groupFileIndex[fileSortInds]
    
    # Write file to disk
    fileIndex1.write(indexFile, format='csv')
else:
    # Read the fileIndex back in as an astropy Table
    print('\nDelete the old index before re-creating a new one.')
    fileIndex = ascii.read(indexFile)#, guess=False, delimiter=' ')