
# some general settings for the trimming script

# define a folder for the logfiles
DIR_TO_LOGFILE = '\\logs\\'

# Define the root folder for the data source
# this script will search for wave files to trim in the "DIR_TO_SRC" folder.
# "SRC_FOLDERS" defines specific folders which should be included.
# If SRC_FOLDERS is emtpy this script will trim all wav files within DIR_TO_SRC.
# All sub-folders and all containing wave files will be trimmed
# and stored in the same directory tree under within"DIR_TO_DEST"
DIR_TO_SRC = './data/'
DIR_TO_DEST = './trimmed_data/'

# This script trims silent space at the beginning of a wav file
# it detects the starting bin of a speaking voice within a wav file
# by comparing the difference between two consecutive bins.
# DELTA defines the necessary difference between these two bins
# BUFFER defines the number of bins to the left of the detected starting bin
# and include this BUFFER to the trimmed files to avoid clipped voices
DELTA = 1000
BUFFER = 1000

# define the folders within DIR_TO_SRC which should be included in the trimming process
#SRC_FOLDERS = ['wav16_test', 'wav16_train']
SRC_FOLDERS = ['p225']
