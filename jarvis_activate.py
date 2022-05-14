import numpy as np
import time
from pydub import AudioSegment
import random
import sys
import io
import os
import matplotlib.mlab as mlab

# To generate wav file from np array.

from scipy.io.wavfile import write
from tensorflow.keras.models import load_model
print("-[Loding Activation]")
model = load_model('jarvis_trigger_very_high.h5')

def get_spectrogram(data):
    nfft = 200 # Length of each window segment
    fs = 8000 # Sampling frequencies
    noverlap = 120 # Overlap between windows
    nchannels = data.ndim
    if nchannels == 1:
        pxx, _, _ = mlab.specgram(data, nfft, fs, noverlap = noverlap)
    elif nchannels == 2:
        pxx, _, _ = mlab.specgram(data[:,0], nfft, fs, noverlap = noverlap)
    return pxx

def detect_triggerword_spectrum(x):
    global model
    x  = x.swapaxes(0,1)
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x)
    return predictions.reshape(-1)

def has_new_triggerword(predictions, chunk_duration, feed_duration, threshold=0.5):
    predictions = predictions > threshold
    chunk_predictions_samples = int(len(predictions) * chunk_duration / feed_duration)
    chunk_predictions = predictions[-chunk_predictions_samples:]
    level = chunk_predictions[0]
    for pred in chunk_predictions:
        if pred > level:
            return True
        else:
            level = pred
    return False

chunk_duration = 1.0 # Each read length in seconds from mic.
fs = 16000 # sampling rate for mic
chunk_samples = int(fs * chunk_duration) # Each read length in number of samples.
# Each model input data duration in seconds, need to be an integer numbers of chunk_duration
feed_duration = 10
feed_samples = int(fs * feed_duration)
assert feed_duration/chunk_duration == int(feed_duration/chunk_duration)

def get_audio_input_stream(callback):
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=fs,
        input=True,
        frames_per_buffer=chunk_samples,
        input_device_index=0,
        stream_callback=callback)
    return stream

import pyaudio
from queue import Queue
from threading import Thread
import sys
import time
# Queue to communiate between the audio callback and main thread
q = Queue()
run = [True]
silence_threshold = 100
# Run the demo for a timeout seconds
timeout = time.time() + 0.5*120  # 0.5 minutes from now
# Data buffer for the input wavform
data = np.zeros(feed_samples, dtype='int16')

def callback(in_data, frame_count, time_info, status):
    global run, timeout, data, silence_threshold    
    # if time.time() > timeout:
    #     run = False        
    data0 = np.frombuffer(in_data, dtype='int16')
    if np.abs(data0).mean() < silence_threshold:
        sys.stdout.write('-')
        return (in_data, pyaudio.paContinue)
    else:
        sys.stdout.write('.')
    data = np.append(data,data0)    
    if len(data) > feed_samples:
        data = data[-feed_samples:]
        # Process data async by sending a queue.
        q.put(data)
    return (in_data, pyaudio.paContinue)
stream = None
def is_activated():
    global stream,data,run
    stream = get_audio_input_stream(callback)
    print("Listening of Activation:")
    run[0]=True
    stream.start_stream()
    activated = False
    try:
        while run[0]:
            data = q.get()
            spectrum = get_spectrogram(data)
            preds = detect_triggerword_spectrum(spectrum)
            new_trigger = has_new_triggerword(preds, chunk_duration, feed_duration)
            if new_trigger:
                # sys.stdout.write('')
                print("[*]",end="")
                activated = True
                break
    except (KeyboardInterrupt, SystemExit):
        stream.stop_stream()
        stream.close()
        timeout = time.time()
        run = False
    stream.stop_stream()
    stream.close()
    return activated
    

if __name__ == "__main__":
    print(is_activated())    
