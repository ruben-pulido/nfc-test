"""
Solfege -> pitch engine.

Each syllable maps to a fixed "home octave" MIDI pitch (major: DO=C4=60;
minor: LA=A3=57) plus a diatonic letter+accidental for staff spelling.
For patterns with more than one note, subsequent notes are placed in
whichever octave is *closest* to the previous note (simple nearest-pitch
voice leading) -- this is what naturally produces things like a repeated
"DO" landing an octave higher after an ascending DO-MI-SO-DO pattern,
without hand-placing every pattern's octaves.
"""

# (letter, accidental, home_midi)  accidental is None, '#', or 'b'
MAJOR_SYLLABLES = {
    "DO": ("C", None, 60),
    "RE": ("D", None, 62),
    "RI": ("D", "#",  63),
    "MI": ("E", None, 64),
    "FA": ("F", None, 65),
    "FI": ("F", "#",  66),
    "SO": ("G", None, 67),
    "SI": ("G", "#",  68),
    "LA": ("A", None, 69),
    "TA": ("B", "b",  70),
    "TI": ("B", None, 71),
}

MINOR_SYLLABLES = {
    "LA": ("A", None, 57),
    "TI": ("B", None, 59),
    "DO": ("C", None, 60),
    "DI": ("C", "#",  61),
    "RE": ("D", None, 62),
    "RI": ("D", "#",  63),
    "MI": ("E", None, 64),
    "FI": ("F", "#",  66),
    "FA": ("F", None, 65),
    "SO": ("G", None, 67),
    "SI": ("G", "#",  68),
    "TE": ("B", "b",  58),
}

LETTER_INDEX = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}


def resolve_pitches(mode, syllables, directions=None):
    """
    Returns a list of dicts: [{letter, accidental, octave, midi, syllable}, ...].

    If `directions` is given (list of 'up'/'down', length len(syllables)-1,
    taken from the source documents' arrow annotations), each subsequent
    note's octave is chosen as the closest instance that is strictly above
    (up) or strictly below (down) the previous note -- this is what
    correctly places e.g. a "SO" below the tonic when the pattern
    descends through it, rather than just picking whichever octave is
    numerically closest regardless of direction.

    If `directions` is omitted, falls back to plain nearest-pitch (only
    used for the simple two-note ascending intervals elsewhere on the site).
    """
    table = MAJOR_SYLLABLES if mode == "major" else MINOR_SYLLABLES
    notes = []
    prev_midi = None
    for i, syl in enumerate(syllables):
        letter, acc, home_midi = table[syl]
        if prev_midi is None:
            midi = home_midi
        else:
            candidates = [home_midi + 12 * k for k in range(-3, 4)]
            direction = directions[i - 1] if directions else None
            if direction == "up":
                valid = [c for c in candidates if c > prev_midi]
                midi = min(valid, key=lambda c: c - prev_midi)
            elif direction == "down":
                valid = [c for c in candidates if c < prev_midi]
                midi = min(valid, key=lambda c: prev_midi - c)
            else:
                midi = min(candidates, key=lambda c: abs(c - prev_midi))
        octave = midi // 12 - 1
        notes.append({
            "syllable": syl,
            "letter": letter,
            "accidental": acc,
            "octave": octave,
            "midi": midi,
        })
        prev_midi = midi
    return notes


def diatonic_step(letter, octave):
    """Staff step relative to the bottom treble-clef line (E4 = 0), same
    convention used by the existing interval-tag staff renderer."""
    return (LETTER_INDEX[letter] + 7 * octave) - 30
