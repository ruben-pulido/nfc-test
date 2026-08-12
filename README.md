# NFC Sound Tags — Ascending Intervals Game

Eight web pages, one per NFC tag, each a "guess the interval" mini-game:
tapping the tag opens the page, which plays two piano notes blind (Do,
followed by a second note). A second tap reveals both notes on a staff and
their solfège names. A third tap jumps to a random other tag's page, so
tapping through several tags in a row feels like a shuffled quiz.

## MLT Tonal Patterns (all 7 tonalities)

Beyond the 8 simple intervals, the site includes a practice app covering
the full Music Learning Theory tonal pattern set across **7 tonalities**:
Major (Ionian), Minor (Aeolian), Dorian, Phrygian, Lydian, Mixolydian, and
Locrian. Tonic = C for major, tonic = A for minor.

| Tonality | Tonic | Categories | Patterns |
|---|---|---|---|
| Major (Ionian) | DO (C) | Tonic, Dominant, Subdominant, Expanded, Cadential, Linear, Chromatic | 57 |
| Minor (Aeolian) | LA (A) | Tonic, Dominant, Subdominant, Expanded, Cadential, Chromatic | 57 |
| Dorian | RE | Tonic, Dominant, Subdominant, Expanded, Cadential, Linear | 53 |
| Phrygian | MI | Tonic, Dominant, Subdominant, Expanded, Cadential, Linear | 53 |
| Lydian | FA | Tonic, Dominant, Subdominant, Expanded, Cadential, Linear | 53 |
| Mixolydian | SO | Tonic, Dominant, Subdominant, Expanded, Cadential, Linear | 53 |
| Locrian | TI | Tonic, Dominant, Subdominant, Expanded, Cadential, Linear | 53 |
| **Total** | | | **379** |

Open **`patterns.html`** to use it: pick a tonality from the dropdown (or
the original Intervals), optionally narrow to one or more categories, then
Start.

### Controls

| Action | Effect |
|---|---|
| Tap anywhere / **Space** | Play blind &rarr; reveal &rarr; jump to a **random** pattern in your current selection |
| **Right arrow** / **swipe right** | Jump to the **next** pattern in the selection, in a fixed sequential order |
| **Left arrow** / **swipe left** | Jump to the **previous** pattern in the selection, sequentially |

Sequential navigation always resets the new pattern to the blind state (so
you still have to play-then-reveal each one) &mdash; it just controls *which*
pattern comes next: predictable order (arrows/swipe) vs. shuffled
(tap/space). Both can be mixed freely mid-session.

### How the Dorian/Phrygian/Lydian/Mixolydian/Locrian patterns were built

The two source documents only covered Major and Minor. For the other five
tonalities, `generator/gen_modal_patterns.py` derives analogous pattern
sets by reusing the *exact scale-degree shapes and documented directions*
from the major document's Tonic/Dominant/Subdominant/Expanded/Cadential/
Linear categories, and re-spelling them in each mode's own natural solfege
syllables (e.g. major's tonic shape 1-3-5 becomes RE-FA-LA in Dorian,
MI-SO-TI in Phrygian, and so on) &mdash; all diatonically correct
automatically (Dorian/Phrygian tonic triads come out minor, Lydian/
Mixolydian major, Locrian diminished, exactly as they should be).

**Deliberately out of scope:** the Chromatic Intermediaries category isn't
generated for these 5 modes, since it depends on each tonality's specific
half-step locations (which chromatic neighbor tones make sense differs
mode to mode) and doesn't transfer directly from the major set the way the
purely-diatonic categories do.

### How the audio/notation is generated

`generator/patterns_data.py` transcribes every pattern from the two MLT
source documents, including each transition's documented ascending/
descending direction. `generator/solfege.py` turns a syllable sequence plus
its directions into actual pitches: the first note lands in a fixed home
octave (DO=C4 for major, LA=A3 for minor), and each subsequent note is
placed in whichever octave is closest to the previous note **while still
strictly obeying the documented direction** &mdash; this is what correctly
distinguishes e.g. a "SO" that continues descending below the tonic from a
"SO" that sits above it, using the same syllable both times.

`generator/gen_staff_v3.py` renders the staff SVGs generically for any
letter/octave/accidental combination (extending the original renderer,
which only handled the plain diatonic notes needed for whole-tone
intervals) &mdash; sharps and flats are drawn as a Unicode &#9839;/&#9837;
glyph next to the notehead. `generator/gen_all_patterns.py` runs the whole
pipeline for all 114 patterns and writes `patterns.json`, the manifest
`patterns.html` reads at runtime.

To regenerate after editing the pattern data:
```bash
cd generator
python3 gen_all_patterns.py
```
(`gen_all_patterns.py` calls `gen_modal_patterns.py` internally for the 5
derived tonalities, so one command regenerates everything.)

## Original interval tags (tag1.html … tag8.html)

| Tag | Notes | Interval |
|-----|-------|----------|
| tag1 | Do &ndash; Do | Unison |
| tag2 | Do &ndash; Re | 2nd |
| tag3 | Do &ndash; Mi | 3rd |
| tag4 | Do &ndash; Fa | 4th |
| tag5 | Do &ndash; Sol | 5th |
| tag6 | Do &ndash; La | 6th |
| tag7 | Do &ndash; Si | 7th |
| tag8 | Do &ndash; Do | Octave |

All eight always start on the same Do (C4), ascending, so the only variable
between tags is how far the second note climbs.

## What's inside

```
nfc-site/
├── index.html              # dev-only landing page linking everything below
├── patterns.html            # practice app for all 114 MLT tonal patterns
├── patterns.json             # manifest patterns.html reads (id/audio/image/label)
├── tag1.html … tag8.html      # one page per simple ascending interval
├── images/
│   ├── tag1.svg … tag8.svg      # each interval on a treble staff
│   └── patterns/                 # one staff SVG per MLT pattern (114 files)
├── sounds/
│   ├── tag1.mp3 … tag8.mp3      # piano audio for each interval
│   └── patterns/                 # one mp3 per MLT pattern (114 files)
└── generator/                # scripts used to build all of the above
    └── ...                     # (not needed for deployment — safe to omit)
```

The mp3s are rendered from real MIDI note sequences through a piano
soundfont, so they sound like an actual piano playing those notes. The
staff images use a hand-embedded vector treble clef (extracted from the
open-source Noto Music font, SIL Open Font License) rather than relying on
the viewing device having a font that supports the Unicode musical clef
character — this is what fixes the "clef renders too big / gets cut off"
issue some phones had, since the glyph is now baked into the SVG as plain
path data with no font dependency at all.

## The three-tap game mechanic

1. **Tap 1 (or automatic)** — plays the two notes blind. The button shows a
   play icon before this, and switches to an eye icon afterward.
2. **Tap 2** — reveals the staff image and the note names (e.g. "DO · SOL").
   The button switches to a next icon.
3. **Tap 3** — jumps to a random *other* tag's page (never repeats the one
   you're on), so you can keep testing your ear tag after tag without
   picking up your phone again.

Every tag's button is the same size, shape, and color at every stage — no
color-coding by interval — so nothing about the button itself gives away
which interval you're about to hear.

## 1. Deploy to GitHub Pages

1. Create a new **public** GitHub repository (e.g. `nfc-test`).
2. Upload all files in this folder to the repo root, preserving the
   `images/` and `sounds/` subfolders.
   ```bash
   cd nfc-site
   git init
   git add .
   git commit -m "NFC interval ear-training game"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo>.git
   git push -u origin main
   ```
3. In the repo, go to **Settings → Pages** → Source: **Deploy from a
   branch** → Branch: **main / (root)** → Save.
4. Your site will be live at:
   ```
   https://<your-username>.github.io/<repo>/
   ```
   with each tag page at `tag1.html` through `tag8.html`.

## 2. Write the URLs to your NFC tags

Using the free **NFC Tools** app (Android and iOS):

1. Open NFC Tools → **Write** tab.
2. **Add a record → URL/URI**.
3. Enter `https://<your-username>.github.io/<repo>/tagN.html` (N = 1-8).
4. Tap **Write**, hold the tag to the phone until confirmed.
5. Repeat for all 8 tags — each pointing to its own `tagN.html`.
6. Before writing, make sure no **Android Application Record (AAR)** is
   added — the write should contain only the plain URI record, so tags
   open correctly in the browser on any phone, not just ones with a
   specific app installed.

## 3. Test

- Enable NFC on the test phone.
- Tap a tag. On modern Android you'll likely see **"Open link found by
  NFC?"** first — an OS-level anti-phishing prompt that can't be
  suppressed by the tag or the page. Tap **Open link**.
- The page tries to auto-play the sound; if blocked, tap once to hear it,
  tap again to reveal, tap a third time to jump to another tag.

## Notes

- **Why any tap at all (for playback)?** Browsers require a user gesture
  before playing audio with sound. The auto-play attempt fires on load and
  on visibility/focus changes, but if it's blocked, a tap on the page is
  the reliable fallback — and it can never accidentally skip ahead to the
  reveal or the next-tag jump, since only a genuine tap advances those
  stages.
- **Adding more intervals/tags**: add a new entry to the generator script's
  interval list, regenerate, and every page's random-jump list will
  automatically include the new tag.
