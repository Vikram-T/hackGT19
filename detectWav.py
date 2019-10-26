import os
import wave
file_name = r"C:\Users\vivek\Dropbox (GaTech)\Projects\HackGT\Interpreting_line_plots.wav"
wave_file = wave.open(file_name, "rb")
frame_rate = wave_file.getframerate()
channels = wave_file.getnchannels()
print(frame_rate)
print(channels)

