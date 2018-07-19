# Trimming wav-files v.01
This script trims silent space at the beginning of a wav file.
It detects the starting bin of a speaking voice within a wav file
by comparing the difference between two consecutive bins.

DELTA defines the necessary difference between these two bins

BUFFER defines the number of bins to the left of the detected starting bin
and include this buffer to the trimmed files to avoid clipped voices.

## Project structure:
- Trim_Main (Callable script with two classes for recursively wav-file trimming)
- Settings (small configuration file)
- Project_Logger (customized logger for console and logfile output)

## How to run
1. Clone
2. Install requirements (scipy)
3. Adjust the path to your source wav-files in the Settings.py
4. Define the path where to save the trimmed wav-files in the Settings.py
5. Run Trim_Main.py
