# NFC Sound Tags — Demo Site

A minimal working example: two web pages, each auto-playing (or one-tap-playing)
a different test sound. Point your NFC tags at these pages and tapping the tag
with a phone opens the page and plays the sound.

## What's inside

```
nfc-site/
├── index.html       # landing page listing both demo tags
├── tag1.html         # "Doorbell" test tone
├── tag2.html         # "Alarm" test tone
└── sounds/
    ├── doorbell.mp3   # ~1s two-tone chime (generated test sound)
    └── alarm.mp3      # ~1s triple-beep (generated test sound)
```

These are synthetic test tones (generated, not copyrighted music) — swap them
out for your own mp3 files once the pipeline is confirmed working. Just keep
the filenames the same, or update the `src="sounds/....mp3"` line in each
tag*.html file.

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
- The browser should open the page. If sound doesn't start immediately
  (autoplay can be blocked, especially on iOS Safari), tap the on-screen
  **▶ Tap to Play** button once — it's a large button by design so a single
  tap works reliably.

## Notes

- **Why a button at all?** Browsers require a user gesture before playing
  audio with sound, to prevent sites from blasting sound uninvited. The NFC
  tap itself doesn't always count, so the button is the reliable fallback
  across iOS Safari, Chrome, and other browsers.
- **HTTPS is required** — GitHub Pages serves over HTTPS automatically, which
  is also a requirement for autoplay to even be considered by some browsers.
- **Swapping in real audio**: replace `sounds/doorbell.mp3` and
  `sounds/alarm.mp3` with your own files (any browser-supported format works:
  mp3, m4a, ogg), keeping the same filenames, or edit the `<audio src="...">`
  line in the corresponding tag*.html.
- **Adding more tags**: duplicate `tag1.html` as `tag3.html`, change the title
  and `sounds/....mp3` reference, add a new mp3, and write a tag pointing to
  `tag3.html`.
