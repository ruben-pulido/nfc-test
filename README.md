# NFC Sound Tags — Ascending Intervals Game

Eight web pages, one per NFC tag, each a "guess the interval" mini-game:
tapping the tag opens the page, which plays two piano notes blind (Do,
followed by a second note). A second tap reveals both notes on a staff and
their solfège names. A third tap jumps to a random other tag's page, so
tapping through several tags in a row feels like a shuffled quiz.

## The 8 intervals

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
├── index.html            # dev-only landing page listing all 8 tags
├── tag1.html … tag8.html   # one page per interval (see table above)
├── images/
│   └── tag1.svg … tag8.svg  # each interval on a treble staff
├── sounds/
│   └── tag1.mp3 … tag8.mp3    # piano audio for each interval
└── generator/               # scripts used to build the above (not needed
    └── ...                    # for deployment — safe to omit from Pages)
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
