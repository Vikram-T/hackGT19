import os
import wave
file_name = r"C:\Users\vivek\Dropbox (GaTech)\Projects\HackGT\Interpreting line plots.wav"
wave_file = wave.open(file_name, "rb")
frame_rate = wave_file.getframerate()
print(frame_rate)