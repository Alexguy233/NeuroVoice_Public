import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from glob import glob
import librosa
import librosa.display
import IPython.display as ipd
from itertools import cycle

# Purely a tool for use in developing and testing getSyllables and other
# audio analyzes. This isn't used by anything and only exists by itself.
# change the file audio_files is based on to make it work. Creates a graph
# so you can see the amplitude of the sounds to help tune silence threshold
# and volume of the syllables.

# Inputs:
# y: array of amplitudes
# amp_thresh: volume threshold to register a syllable
# min_silence_dur: minimum silence necessary between two syllables to count
# as a new one
# sr: sample rate of the original audio
# Returns:
# int[] of a starting and then ending index of a syllable
def findNoisyIntervals(y, amp_thresh=0.22, min_silence_dur=0.05, sr=44100):
    """
    Strict silence detection based on amplitude threshold and minimum duration.
    Returns non-silent segments where audio exceeds amplitude threshold.
    """
    # Convert minimum silence duration to samples
    min_silence_samples = int(min_silence_dur * sr)
    
    # Create silence mask (True when amplitude below threshold)
    silence_mask = np.abs(y) < amp_thresh
    
    # Find transitions between silence and non-silence
    changes = np.diff(silence_mask.astype(int))
    silence_starts = np.where(changes == 1)[0] + 1
    silence_ends = np.where(changes == -1)[0]
    
    # Handle audio that starts/ends with silence
    if silence_mask[0]:
        silence_starts = np.insert(silence_starts, 0, 0)
    if silence_mask[-1]:
        silence_ends = np.append(silence_ends, len(y)-1)
    
    # Filter silence segments by duration
    valid_silences = []
    for start, end in zip(silence_starts, silence_ends):
        if (end - start) >= min_silence_samples:
            valid_silences.append((start, end))
    
    # Extract non-silent segments between valid silences
    noisy_segments = []
    prev_end = 0
    
    for start, end in valid_silences:
        if start > prev_end:
            noisy_segments.append((prev_end, start))
        prev_end = end
    
    # Add final segment after last silence
    if prev_end < len(y) - 1:
        noisy_segments.append((prev_end, len(y)-1))
    
    return noisy_segments


# Visualization setup
sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(color_pal)

# Load audio, change the string name to look at different ones
audio_files = glob("recording4_mutazfast.wav")
y, sr = librosa.load(audio_files[0], sr=None)

# Detect noisy segments with strict thresholds
y_noises = findNoisyIntervals(y, 
                            amp_thresh=0.18,  # Strict amplitude threshold
                            min_silence_dur=0.05,  # 50ms of silence required
                            sr=sr)
print(y_noises)
#Plot with highlighted segments
plt.figure(figsize=(12, 6))
librosa.display.waveshow(y, sr=sr, alpha=0.7)
#
# Add threshold line and silent regions
plt.axhline(y=0.18, color='r', linestyle='--', alpha=0.5, label='Amplitude Threshold')
plt.axhline(y=-0.18, color='r', linestyle='--', alpha=0.5)

# Highlight noisy segments. The colors repeat
# to show pa, ta, and ka because right now it gets
# the median based on assuming the three appear 
# repeatedly one after another. 
colors = ['red', 'green', 'blue']

for i, (start, end) in enumerate(y_noises):
    plt.axvspan(start/sr, end/sr, color=colors[i % len(colors)], alpha=0.3)
    
plt.title("Chunks Displayed as Colored Sections")
plt.legend()
plt.show()
