from pydub import AudioSegment
from math import ceil
import ctypes
from glob import glob
from pathlib import Path

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def cleanup(filepath, file):
    cleanedup = "songs_converted/" + filepath.replace("songs\\", "").replace(".mp3", "").replace(".flac", "").replace(".wav", "").replace(".ogg", "").replace(".", "").replace(",", "").replace("_", "").replace("'", "") + " _" + str(ceil((len(file) / 1000.0))).zfill(3) # GMOD can't open some files if they have some forbidden characters. Some workshop uploads tools don't like them too. So I've did this awfulness. Oh and I need to make it fit for SBM.
    return cleanedup
    
def edit(file):
    loadedsong = AudioSegment.from_file(file)
    fadetime = ceil(clamp((len(loadedsong)) * 0.02, 0, 7000))
    editedsong = loadedsong.fade_in(fadetime).fade_out(fadetime).set_frame_rate(44100)
    return editedsong

def main():
    print("SBM Auto Converter: convert lots of songs automatically to the type SBM accepts! Made by John aka downline.")
    convertedfilesnumber = 0
    if not Path(str(Path.cwd()) + "/songs").is_dir() or not Path(str(Path.cwd()) + "/songs_converted").is_dir():
        Path(str(Path.cwd()) + "/songs").mkdir(parents=True, exist_ok=True) 
        Path(str(Path.cwd()) + "/songs_converted").mkdir(parents=True, exist_ok=True)
        print("Created the previously missing directories for songs.")
        print("Drop your songs in there and restart the script! " + str(Path.cwd()) + "\songs")
    else:
        if len(glob('songs/*')) == 0:
            print("No songs found. Drop them into the songs folder! " + str(Path.cwd()) + "\songs")
        else:
            for i in glob("songs/*"):
                try:
                    print("Working...")
                    initializedfile = edit(i)
                    savepath = cleanup(i, initializedfile)
                    initializedfile.export(savepath + ".ogg", format="ogg")
                    print("Saved: " + savepath)
                    convertedfilesnumber += 1
                except Exception as e:
                    print("Unexpected error. ", e)
                    continue
            if convertedfilesnumber == len(glob('songs/*')):
                print("Ran out of files.")
                ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True )
    return input()
 
main()
