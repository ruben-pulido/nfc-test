"""
Generates Tonic/Dominant/Subdominant/Expanded/Cadential/Linear pattern
categories for the 5 remaining diatonic modal tonalities (Dorian, Phrygian,
Lydian, Mixolydian, Locrian), by reusing the exact pattern *shapes*
(scale-degree positions + documented directions) from the major (Ionian)
document and re-spelling them in each mode's own natural solfege syllables.

This is a deliberate simplification: the Chromatic Intermediaries category
is skipped for these 5 modes, since it depends on each tonality's specific
half-step locations (which chromatic neighbor tones "make sense" differs
mode to mode) and doesn't transfer directly from the major set the way the
purely-diatonic categories do.
"""
import sys
sys.path.insert(0, '.')

from patterns_data import MAJOR_PATTERNS, CATEGORY_LABELS
from solfege import resolve_pitches, MAJOR_SYLLABLES

IONIAN_CYCLE = ['DO','RE','MI','FA','SO','LA','TI']

MODE_CYCLES = {
    'dorian':     ['RE','MI','FA','SO','LA','TI','DO'],
    'phrygian':   ['MI','FA','SO','LA','TI','DO','RE'],
    'lydian':     ['FA','SO','LA','TI','DO','RE','MI'],
    'mixolydian': ['SO','LA','TI','DO','RE','MI','FA'],
    'locrian':    ['TI','DO','RE','MI','FA','SO','LA'],
}

TEMPLATE_CATEGORIES = ['tonic', 'dominant', 'subdominant', 'expanded', 'cadential', 'linear']


def build_templates():
    """Extract (category, [degree numbers], [directions]) from MAJOR_PATTERNS,
    skipping the chromatic category (which uses altered tones)."""
    templates = []
    for category, syllables, directions in MAJOR_PATTERNS:
        if category not in TEMPLATE_CATEGORIES:
            continue
        degrees = [IONIAN_CYCLE.index(s) + 1 for s in syllables]
        templates.append((category, degrees, directions))
    return templates


def degrees_to_mode_syllables(mode_cycle, degrees):
    return [mode_cycle[d - 1] for d in degrees]


def resolve_for_mode(syllables, directions):
    # All 5 new modes use only natural (unaltered) syllables, so the
    # existing MAJOR_SYLLABLES table (natural note spellings/home octaves)
    # is reused directly -- the pitch engine doesn't care which syllable is
    # conceptually "tonic", it just resolves the sequence given.
    table = MAJOR_SYLLABLES
    notes = []
    prev_midi = None
    for i, syl in enumerate(syllables):
        letter, acc, home_midi = table[syl]
        if prev_midi is None:
            midi = home_midi
        else:
            candidates = [home_midi + 12 * k for k in range(-3, 4)]
            direction = directions[i - 1]
            if direction == "up":
                valid = [c for c in candidates if c > prev_midi]
                midi = min(valid, key=lambda c: c - prev_midi)
            else:
                valid = [c for c in candidates if c < prev_midi]
                midi = min(valid, key=lambda c: prev_midi - c)
        octave = midi // 12 - 1
        notes.append({"syllable": syl, "letter": letter, "accidental": acc,
                       "octave": octave, "midi": midi})
        prev_midi = midi
    return notes


def build_modal_patterns():
    """Returns dict: mode_name -> [(category, syllables, directions), ...]"""
    templates = build_templates()
    result = {}
    for mode_name, cycle in MODE_CYCLES.items():
        patterns = []
        for category, degrees, directions in templates:
            syllables = degrees_to_mode_syllables(cycle, degrees)
            patterns.append((category, syllables, directions))
        result[mode_name] = patterns
    return result


if __name__ == "__main__":
    modal = build_modal_patterns()
    for mode, patterns in modal.items():
        print(mode, len(patterns), "patterns")
        for cat, syl, dirs in patterns[:2]:
            print("  ", cat, syl, dirs)
