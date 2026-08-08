# NFC Sound Tags — Demo Site

Two web pages, each a "guess the notes" mini-game: tapping the NFC tag opens
the page, which plays a piano note sequence blind (no notes shown yet). A
second tap on the page reveals the notes on a staff and their solfège names.

## What's inside

```
nfc-site/
├── index.html          # landing page listing both tags
├── tag1.html            # DO - MI - SOL (ascending)
├── tag2.html             # SOL - FA - RE - SI (descending)
├── images/
│   ├── tag1.svg            # DO-MI-SOL on a treble staff
│   └── tag2.svg             # SOL-FA-RE-SI on a treble staff
└── sounds/
    ├── tag1.mp3             # piano: C4-E4-G4 ascending (DO-MI-SOL)
    └── tag2.mp3              # piano: G4-F4-D4-B3 descending (SOL-FA-RE-SI)
```

The mp3s are rendered from real MIDI note sequences through a piano
soundfont (not synthetic beeps), so they sound like an actual piano playing
those notes. Filenames match their tag (`tag1.mp3`, `tag2.mp3`) — if you
add more tags, keep following that pattern.

## 1. Deploy to GitHub Pages

1. Create a new **public** GitHub repository (e.g. `nfc-sounds`).
2. Upload all the files in this folder to the repo root, preserving the
   `sounds/` subfolder — either via the GitHub web UI (drag and drop) or:
   ```bash
   cd nfc-site
   git init
   git add .
   git commit -m "NFC sound tag demo"
   git branch -M main
   git remote add origin https://github.com/<your-username>/nfc-sounds.git
   git push -u origin main
   ```
3. In the repo, go to **Settings → Pages**.
4. Under "Build and deployment", set **Source: Deploy from a branch**,
   **Branch: main / (root)**, then Save.
5. Wait ~1 minute. Your site will be live at:
   ```
   https://<your-username>.github.io/nfc-sounds/
   ```
   with the two tag pages at:
   ```
   https://<your-username>.github.io/nfc-sounds/tag1.html
   https://<your-username>.github.io/nfc-sounds/tag2.html
   ```

## 2. Write the URLs to your NFC tags

Using the free **NFC Tools** app (Android and iOS):

1. Open NFC Tools → **Write** tab.
2. **Add a record → URL/URI**.
3. Enter `https://<your-username>.github.io/nfc-sounds/tag1.html`
4. Tap **Write**, then hold your first NFC tag against the phone's NFC
   antenna until it confirms.
5. Repeat with `tag2.html` for your second tag.

On iPhone you can alternatively use the **Shortcuts app** to write NFC tags
directly (Automation → NFC → Scan), but writing a plain URL record via NFC
Tools is more portable since it doesn't depend on Shortcuts being installed
on whichever phone taps it later.

## 3. Test

- Enable NFC on the test phone (Settings → Connected devices → NFC, on most
  Android phones; iPhones with iOS 14+ read NFC automatically when the
  camera/background tag reader is active, no app needed).
- Tap the tag against the phone.
- On modern Android, you'll likely see a system dialog first: **"Open link
  found by NFC?"** — this is an OS-level anti-phishing prompt that no tag
  content or webpage can suppress. Tap **Abrir enlace / Open link**.
- The page opens showing only a play button — no notes revealed yet — and
  immediately tries to play the sound blind. If that's blocked by the
  browser's autoplay policy, tap the play button once to hear it.
- Tap again (the button is now an eye icon) to reveal the notes on a staff
  with their names.

## Notes

- **Why any tap at all?** Browsers require a user gesture before playing
  audio with sound, to prevent sites from blasting sound uninvited. The NFC
  tap itself doesn't always count as that gesture, so a tap on the page is
  the reliable fallback across iOS Safari, Chrome, and other browsers.
- **The two-tap game mechanic**: tap 1 plays the sound blind (or the page
  auto-plays it, in which case tap 1 becomes the reveal instead); tap 2
  reveals the staff image and note names. This is intentional — it's a
  listen-first, look-second guessing game, not a bug.
- **HTTPS is required** — GitHub Pages serves over HTTPS automatically, which
  is also a requirement for autoplay to even be considered by some browsers.
- **Swapping in real audio**: replace `sounds/tag1.mp3` and
  `sounds/tag2.mp3` with your own files (any browser-supported format works:
  mp3, m4a, ogg), keeping the same filenames, or edit the `<audio src="...">`
  line in the corresponding tag*.html.
- **Adding more tags**: duplicate `tag1.html` as `tag3.html`, change the title
  and `sounds/....mp3` reference, add a new mp3, and write a tag pointing to
  `tag3.html`.
