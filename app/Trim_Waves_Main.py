from scipy.io import wavfile
import numpy as np
import os
from time import time
import logging
from app.Project_Logger import Console_and_file_logger
import app.Settings as Settings

################ Static params ################
PATH = os.getcwd()
FILE = os.path.basename(__file__)
FILES_CHANGED = 0
###############################################


class Wavefile:

    def __load_file__(self, filename):
        return wavfile.read(filename)

    def __init__(self, dir_name='./data/p225', filename='p225_003.wav'):
        """
        Opens a wav file from the given directory
        :param dir_name:
        :param filename:
        """
        logging.info('Trying to open {0}'.format(os.path.join(dir_name, filename)))
        self.dir = dir_name
        self.filename = filename
        self.fs, self.data = self.__load_file__(os.path.join(dir_name, filename))

    def update(self, dir):
        """
        Update the directory where this wav files should be saved to
        :param dir:
        :return:
        """
        self.dir = dir

    def __ensure_dir__(self, file_path):
        """
        Make sure a directory exists or create it
        :param file_path:
        :return:
        """
        logging.info('Trying to save to {0}'.format(file_path))
        if not os.path.exists(file_path):
            logging.info('Creating directory {}'.format(file_path))
            os.makedirs(file_path)

    def save(self):
        """
        Saves the wav file
        :return:
        """
        self.__ensure_dir__(self.dir)
        wavfile.write(os.path.join(self.dir, self.filename), self.fs, self.data)

    def trim(self, dir='./trimmed'):
        """
        Trim the current wav file
        save it afterwards to dir
        :param dir:
        :return:
        """
        self.data = self.__trim_file__(self.data)
        logging.info('File trimmed')
        self.dir = dir
        self.save()

    def __trim_file__(self, untrimmed_file):
        """
        Internal trimming function
        :param untrimmed_file:
        :return trimmed_file:
        """
        start_index = self.__get_start_index__(untrimmed_file)
        logging.info('Start index = {0}'.format(start_index))
        logging.info(untrimmed_file[start_index - 1:start_index + 1])
        return np.asarray(untrimmed_file[start_index:], dtype=np.int16)

    def __get_start_index__(self, arr):
        """
        Returns the beginning of a speaking voice within a wav-file
        :param wave file data as arr:
        :return:
        """
        # initialize with the first bucket
        last_bucket = arr[0]

        # inner function which compares to bins within a wav file
        def is_significant_change(elem1, elem2):
            return (abs(elem1) - abs(elem2)) > Settings.DELTA

        # go through all bins in this wav file and compare t and t-1
        for idx, bucket in enumerate(arr):
            if is_significant_change(bucket, last_bucket):
                # avoid returning an index smaller than 0
                if idx - Settings.BUFFER < 0:
                    return 0
                else:
                    return idx - Settings.BUFFER
            else:
                last_bucket = bucket
        # if no significant change is noticeable, avoid returning None, keep wav file as it is
        return 0


class WaveTrimmer:
    def __init__(self):
        self.start_trimming()

    def trim_all_files_in_dir(self, current_src_dir, current_dest_dir):
        """
        search and trim wav files
        recursively search for sub-folders
        :param current_src_dir:
        :param current_dest_dir:
        :return:
        """

        t1 = time()
        logging.info('Current src directory: {0}'.format(current_src_dir))
        logging.info('Current dest directory: {0}'.format(current_dest_dir))

        # for every file in this sub-folder
        for filename in os.listdir(current_src_dir):
            # trim only wav files
            if filename.endswith(".wav"):
                # load the wav file
                wavfile = Wavefile(current_src_dir, filename)
                # trim the silent beginning within the wav file
                # save the new wave file to the destination folder defined in settings.DIR_TO_DEST
                wavfile.trim(dir=current_dest_dir)

            # further sub-directories found, recursively start trimming for this folder
            elif os.path.isdir(os.path.join(current_src_dir, filename)):
                self.trim_all_files_in_dir(os.path.join(current_src_dir, filename),
                                           os.path.join(current_dest_dir, filename))

            # ignore all other files
            else:
                logging.info('Skip file {} '.format(os.path.join(current_src_dir, filename)))

        logging.info('Trimming sub-directory {} done in {:0.3f}s'.format(current_src_dir, time() - t1))

    def start_trimming(self):
        """
        Start trimming all files within Settings.SRC_FOLDERS
        :return:
        """

        # Get all defined folders
        base = Settings.SRC_FOLDERS

        # if there are no defined folders named trim all wav files within DIR_TO_SRC
        if not base:
            logging.info(
                'No specific folders named, take all sub-folders in {} for trimming'.format(Settings.DIR_TO_SRC))
            base = [d for d in os.listdir(Settings.DIR_TO_SRC) if os.path.isdir(os.path.join(Settings.DIR_TO_SRC, d))]

        # call the recursively trimmer for each sub-folder
        for dir_n in base:
            t0 = time()
            # concat base source folder and included sub-folders
            dir_base_src = Settings.DIR_TO_SRC + dir_n
            dir_base_dest = Settings.DIR_TO_DEST + dir_n
            logging.info('Opening directory: {0}'.format(dir_base_src))
            # trim all wav files, find recursively sub-folder containing wav files
            self.trim_all_files_in_dir(dir_base_src, dir_base_dest)
            logging.info('Trimming directory {} done in {:0.3f}s'.format(dir_base_src, time() - t0))
        logging.info('finish')


def main():
    WaveTrimmer()


if __name__ == "__main__":
    # execute only if run as a script
    logger = Console_and_file_logger(os.path.basename(__file__))
    t0 = time()
    main()
    logging.info('Trimming done in {:0.3f}s'.format(time() - t0))
