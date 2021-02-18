# Libraries
import pandas as pd
import os
import numpy as np
# from datetime import datetime, timedelta
import datetime as dt
import random

# For reading sound file
import librosa
# For signal processing
from scipy.signal import find_peaks
from scipy.fft import irfft
from scipy.fft import rfft,rfftfreq

# Read in relevant data files
samples_df = pd.read_csv('samples_short.csv')
ground_truth = pd.read_csv('ground_truth_short.csv')
perfect = pd.read_csv('perfect.csv')

directory_of_sounds = 'sounds/samples/'
os.path.isdir(directory_of_sounds)
len(os.listdir(directory_of_sounds + '/vi95kMQ65UeU7K1wae12D1GUeXd2')) # should be 22

#########################
# TASK DESCRIPTION
#########################

### The data ############
# You've been provided with 22 thirty-second sound files, spanning 11 minutes.
# The user of the device coughed 10 times during this 11 minute period.
# The exact timestamps of these coughs are in `ground_truth`
# `samples_df` has the mapping of the 30 second files, along with the time ("timestamp") at which time the 30 second
# recording started

### The task ############
# Write a function in python which takes a sound file as an argument
# and returns a dataframe of times (number of second since file start) at which a cough occurred.
# This is an event detection task in which it is far better to OVER-detect than
# to UNDER-detect. In regards to tuning prec/recall, you should consider
# a correctly detected cough to be worth 10 "points" and a "false positive"
# (ie, a "peak" which is not a cough) to be worth -1 points.
# The simpler, the better. No need to use Tensorflow, pre-trained models, or anything like that.
# Feel free to use libraries, but know that this is not a test of your modeling skills.

def detect_coughs(file = 'sounds/samples/vi95kMQ65UeU7K1wae12D1GUeXd2/sample-1613658921823.m4a'):
    # Replace the below random code with something meaningful which
    # generates a one-column dataframe with a column named "peak_start"
    y,sr = librosa.load(file) # sr is the sampling rate
    N = y.shape[0] # N is number of samples
    
    yf = rfft(y)
    xf = rfftfreq(N,1/sr) # Going to frequency domain
    
    points_per_freq = len(xf1) / (sr / 2)
    target_idx_100 = int(points_per_freq * 100)
    target_idx_2000 = int(points_per_freq * 2000) 
    
    # Removing all frequencies except 100-2000 Hz, as this is the typical range of frequencies for a cough from an adult. 
    # Reference: https://pubmed.ncbi.nlm.nih.gov/12666872/
    yf[ : target_idx_100 + 1 ] = 0
    yf[target_idx_2000 - 1 : ] = 0
    
    new_sig = irfft(yf) # Going back to time domain with filtered signal
    
    peaks_array = find_peaks(new_sig,prominence=0.02)[0] #Finding start of peaks in filtered signal, should correspond to coughs
    peaks = peaks_array/sr # The time instant of starting of peak is arrived at by dividing by sampling rate
    out = pd.DataFrame({'peak_start': peaks})
    return(out)

# Run function on all sounds
sounds_dir = directory_of_sounds + 'vi95kMQ65UeU7K1wae12D1GUeXd2/'
all_sounds = os.listdir(sounds_dir)
out_list = []
for i in range(len(all_sounds)):
    this_file = sounds_dir + all_sounds[i]
    this_result = detect_coughs(file = this_file)
    this_result['file'] = this_file
    out_list.append(this_result)
final = pd.concat(out_list)
final.to_csv('final.csv')

# Grade the approach
true_positives = 0
# Detect if coughs were correctly corrected
for i in range(len(perfect)):
    this_cough = perfect.iloc[i]
    same_file = final[final['file'] == this_cough['file']]
    # Get time differences
    same_file['time_diff'] = this_cough['peak_start'] - same_file['peak_start']
    keep = same_file[same_file['time_diff'] <= 0.4]
    keep = keep[keep['time_diff'] >= -0.4]
    if len(keep) > 0:
        print('Correctly found the cough at ', str(round(this_cough['peak_start'], 2)) + ' in ' + this_cough['file'])
        true_positives = true_positives + 1
    else:
        print('Missed the cough at ', str(round(this_cough['peak_start'], 2)) + ' in ' + this_cough['file'])
        pass
# Now measure false positives
false_positives = len(final) - true_positives
print('Detected ' + str(false_positives) + ' false positives')
# Calculate final score
final_score = (true_positives * 10) - false_positives
print('FINAL SCORE OF: ' + str(final_score))
