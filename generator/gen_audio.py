from midiutil import MIDIFile
import subprocess, os

SF = "/usr/share/sounds/sf2/default-GM.sf2"

# (tag_number, [midi_pitch1, midi_pitch2])
INTERVALS = [
    (1, [60, 60]),  # do-do (unison)
    (2, [60, 62]),  # do-re
    (3, [60, 64]),  # do-mi
    (4, [60, 65]),  # do-fa
    (5, [60, 67]),  # do-sol
    (6, [60, 69]),  # do-la
    (7, [60, 71]),  # do-si
    (8, [60, 72]),  # do-do (octave)
]

for n, notes in INTERVALS:
    mf = MIDIFile(1)
    mf.addTempo(0, 0, 100)
    mf.addProgramChange(0, 0, 0, 0)  # Acoustic Grand Piano
    dur = 0.9
    for i, pitch in enumerate(notes):
        mf.addNote(0, 0, pitch, i * dur, dur, 100)
    midpath = f"/home/claude/nfc-site/sounds/tag{n}.mid"
    with open(midpath, "wb") as f:
        mf.writeFile(f)

    wavpath = f"/home/claude/nfc-site/sounds/tag{n}_raw.wav"
    subprocess.run(["fluidsynth", "-ni", SF, midpath, "-F", wavpath, "-r", "44100", "-g", "1.0"],
                    check=True, capture_output=True)

    mp3path = f"/home/claude/nfc-site/sounds/tag{n}.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", wavpath,
                     "-af", "silenceremove=start_periods=0:stop_periods=1:stop_duration=0.3:stop_threshold=-45dB",
                     "-q:a", "3", mp3path, "-loglevel", "error"], check=True)

    os.remove(midpath)
    os.remove(wavpath)
    print(f"tag{n}.mp3 done ({notes})")
