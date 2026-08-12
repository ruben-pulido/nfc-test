import json
import os
import subprocess
import sys
sys.path.insert(0, '.')

from patterns_data import MAJOR_PATTERNS, MINOR_PATTERNS, CATEGORY_LABELS
from solfege import resolve_pitches
from gen_staff_v3 import render_staff_svg
from gen_modal_patterns import build_modal_patterns
from midiutil import MIDIFile

SF = "/usr/share/sounds/sf2/default-GM.sf2"
IMAGES_DIR = "/home/claude/nfc-site/images/patterns"
SOUNDS_DIR = "/home/claude/nfc-site/sounds/patterns"

SOLFEGE_DISPLAY = {  # for the revealed label text
    "DO": "DO", "RE": "RE", "RI": "RI", "MI": "MI", "FA": "FA", "FI": "FI",
    "SO": "SOL", "SI": "SI", "LA": "LA", "TA": "TA", "TI": "TI",
    "DI": "DI", "TE": "TE",
}


def make_id(mode, category, index):
    return f"{mode}_{category}_{index:02d}"


def build_audio(notes, out_path):
    mf = MIDIFile(1)
    mf.addTempo(0, 0, 100)
    mf.addProgramChange(0, 0, 0, 0)  # Acoustic Grand Piano
    dur = 0.75 if len(notes) <= 3 else 0.62
    for i, n in enumerate(notes):
        mf.addNote(0, 0, n['midi'], i * dur, dur, 100)
    midpath = out_path.replace('.mp3', '.mid')
    with open(midpath, 'wb') as f:
        mf.writeFile(f)
    wavpath = out_path.replace('.mp3', '_raw.wav')
    subprocess.run(["fluidsynth", "-ni", SF, midpath, "-F", wavpath, "-r", "44100", "-g", "1.0"],
                    check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", wavpath,
                     "-af", "silenceremove=start_periods=0:stop_periods=1:stop_duration=0.3:stop_threshold=-45dB",
                     "-q:a", "3", out_path, "-loglevel", "error"], check=True)
    os.remove(midpath)
    os.remove(wavpath)


def process(mode, patterns, table_mode=None):
    """table_mode: which syllable table to use for pitch resolution
    ('major' or 'minor'). Defaults to `mode` itself (used for major/minor);
    the 5 new modal tonalities pass table_mode='major' since they only use
    natural syllables, resolved via the same table as major."""
    if table_mode is None:
        table_mode = mode
    manifest = []
    counters = {}
    for category, syllables, directions in patterns:
        counters[category] = counters.get(category, 0) + 1
        idx = counters[category]
        pid = make_id(mode, category, idx)

        notes = resolve_pitches(table_mode, syllables, directions)

        svg_path = f"{IMAGES_DIR}/{pid}.svg"
        render_staff_svg(notes, svg_path)

        mp3_path = f"{SOUNDS_DIR}/{pid}.mp3"
        build_audio(notes, mp3_path)

        label = " \u00b7 ".join(SOLFEGE_DISPLAY[s] for s in syllables)

        manifest.append({
            "id": pid,
            "mode": mode,
            "category": category,
            "categoryLabel": CATEGORY_LABELS[category],
            "syllables": syllables,
            "label": label,
            "image": f"images/patterns/{pid}.svg",
            "audio": f"sounds/patterns/{pid}.mp3",
        })
        print(pid, syllables, "->", [f"{n['letter']}{n['accidental'] or ''}{n['octave']}" for n in notes])
    return manifest


all_manifest = []
all_manifest += process("major", MAJOR_PATTERNS)
all_manifest += process("minor", MINOR_PATTERNS)

modal = build_modal_patterns()
MODE_DISPLAY_NAMES = {
    'dorian': 'Dorian', 'phrygian': 'Phrygian', 'lydian': 'Lydian',
    'mixolydian': 'Mixolydian', 'locrian': 'Locrian',
}
for mode_name, patterns in modal.items():
    all_manifest += process(mode_name, patterns, table_mode="major")

with open("/home/claude/nfc-site/patterns.json", "w") as f:
    json.dump(all_manifest, f, indent=2)

print(f"\nTotal patterns generated: {len(all_manifest)}")
