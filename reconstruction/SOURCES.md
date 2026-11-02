# Flash reconstruction evidence

The live application is ordinary HTML/CSS/JavaScript. No SWF, ActionScript, emulator, PHP or tracking code is shipped.

## Version findings

- The main experience was Flash 7 by the [17 December 2005 wrapper capture](https://web.archive.org/web/20051217002958/http://sallymusic.com:80/land_of_clowns_and_bozos/clowncollege.html). Its exact launch date is unknown.
- The original root splash page explicitly recommended Flash 7, a 1024 × 768 screen and “elbows (optional).” It linked to `/cms` as the plain HTML / low-bandwidth alternative. That alternative was the basis of the first restoration.
- Earlier recovered 2003–2004 sections are HTML. They are preserved alongside the Flash reconstruction; those earlier bodies cannot be claimed to be the missing later Flash feed.
- Nine primary SWF files survive, with six older underscore/gomera variants. Main/current movies were used coherently; the backups were not silently merged.
- The current main, intro and loader hashes match public Wayback CDX digests:
  - `00_loader.swf`: `BCQM3TXFWCH6XYS3GQI3UCZSQVFKUXUB`, capture `20060505014256`.
  - `01_intro.swf`: `GJL5CNEWP3TZ2IPDLXZIQMFJPEN4HZ4I`, capture `20110715234906`.
  - `02_main.swf`: `7HP2LYL4H73QQTGNL6F4BKR73YVVQYJI`, capture `20110715234952`.
- Header facts: Flash version 7; 31 fps; 1007 × 675 pixels. `07_merch.swf` is 1007 × 668. Main has 154 root frames; its `init` label is frame 83 and `news` label frame 89.

## Runtime/navigation findings

`00_loader.swf` chooses `02_main.swf` normally; `sub=intro` loads the optional `01_intro.swf`. The optional intro is not the normal main entrance and was not claimed as reconstructed.

Main root labels: news 89, audio 97, pictures 105, bio 112, tour 119, merch 126, links 133. They load the corresponding `03_audio.swf` through `08_links.swf`.

`createBugs` creates six `protobug` instances mapping to audio, bio, links, tour, merch and pictures. `reset`/`move` use bounds 630 × 430 and randomized speed 5–14 px per 31fps frame. The modern version ports this movement and original wing drawings; spring-to-mouse and secondary bug reactions are approximate.

The source has entrance/exit labels and programmatic object positioning. Audio’s `speakers.moveToPoint(speakers._x,120,50)` supplies the settled speaker Y coordinate; the extracted audio scene was rendered with that position. The source fades the original `birdies` sound to volume 30; the modern version uses the original sound at 0.3 volume behind an opt-in toggle.

## Asset preparation

JPEXS Free Flash Decompiler 26.4.0 exported static vectors/bitmaps, frame PNGs, text and ActionScript. A temporary Temurin 17 runtime was used in `/tmp`; no system installation or credentials were created. Ruffle 0.7.1 was used only in an ignored, local reference page with script access disabled and network access confined to the local server. Original and reconstructed compositions were compared in the browser. Neither Ruffle nor the SWF files are included in `site/`.

- `assets/landscape.png`: main frame 83 with the independently rebuilt navigation clip excluded.
- `assets/arrival.webp`: original main root frames 2–83 at 31 fps; a single entrance, followed by the settled scene.
- `assets/blue-paper-overlay.png`: original loader background shape and its color transform; loading progress/cloud excluded. `paper.jpg` is the embedded original tile.
- `assets/news-scene.png`: `newsBox` sprite 225, frame 35, cropped back to stage coordinates using the exported transform offset (31, 742.45).
- Audio/pictures/bio/tour/merch/links scene samples: root frames 36 / 93 / 40 / 45 / 35 / 39. Audio uses the source’s settled speaker position. An idle speech balloon was excluded from the biography layer because its activation was scripted.
- Original navigation bitmap and player-control bitmaps are used directly. Six original bug wing frames form the animated menu.
- Six original band photos were reviewed, exported without metadata and included. Album order is unknown. Ten previously recovered MP3s remain unchanged.

## Limits

The missing CMS database, RSS/XML feeds and gallery XML prevent reconstruction of the exact last live content/playlist/gallery ordering. Recovered news is presented with unverified publication years unassigned; earlier biography/links/merch sources are labeled. Original full ActionScript behavior, optional intro, moving gallery eyes and speech reactions are not completely ported. Some secondary sprites are static frame samples. Page/scene transitions and speaker pulse are approximations. Mobile flow, accessible controls, source notes, gallery dialog and readable playlist are modern additions.

The readable archive, inactive old services, old-domain link rewrites and privacy protections remain. Originals, Obsidian notes, DNS and other sites are untouched.

## Hidden recording restored — 2 November 2026

Original `02_main.swf`, sprite 214 frame 1, assigns `slave.onRelease` to open `../video/disconnected.html` in a 360 × 100 popup. `slave` is sprite 210: the hand/string and small blue figure beside the prone boy, inside newsBox (sprite 225). The original wrapper's title is `://sally - is this mark berlin?` and its embed points to `http://sallymusic.com/offsite/markberlin.mp3`.

The original MP3 was recovered from `/Web/sallymusic.com/offsite/markberlin.mp3` in the saved Dropbox archive, and copied byte-for-byte to `site/assets/audio/markberlin.mp3`. Size: 18,793,588 bytes. SHA-256: `d8fbd957f08482f42b2c9bd527c3fd684e1ec8d552babfb68dd10203dd280bb0`. Its computed Dropbox content hash matches the source: `db31eed8703ced60913761954704a4605016e8e1d0a76bc7ab802d87c299a491`. Browser playback reports 1174.465375 seconds (19:34). No transcription is added.

The news-scene hotspot follows the original figure and expands to a minimum 44px touch target on small screens. A native dialog and browser audio controls replace the obsolete popup/embed. Unlike the original autoplay embed, playback is opt-in. Closing, Escape or browser Back pauses the recording and returns to the news scene; `#mark-berlin` opens the dialog directly without autoplay. Starting the recording pauses Sally Radio and ambient birds. No visual timing or original asset was changed.

## Requested slower playback — 31 October 2026

The first slowdown set decorative motion to 75% of the initial reconstruction’s speed. CSS `--motion-speed: .75` controls paper transitions (480 → 640ms), speaker pulse (500 → 666.667ms per direction), and the JavaScript flying-menu/wing step (31 → 23.25 source frames per second, with fractional frame time carried forward to avoid refresh-rate quantization). The entrance WebP’s existing frame durations were multiplied by 4/3 through ANMF-header edits, preserving its compressed artwork and loop setting: 2624 → 3499ms after cumulative rounding. Its JS completion timer scales from 2700 → 3600ms. Audio and ambient playback remain at their native 1× speed; navigation, photo dialogs and other UI actions receive no delay.

## Additional slowdown — 1 November 2026

A second requested 25% slowdown sets the current visual rate to 56.25% of the initial reconstruction (0.75 × 0.75). All existing visual timing uses CSS `--motion-speed: .5625`, including the JavaScript flying-menu/wing cadence: 17.4375 source frames/s, or 57.34767ms per step. Paper transitions are 853.333ms and speaker pulse 888.889ms per direction. The entrance ANMF headers were retimed another 4/3, from 3499 to 4665ms with cumulative rounding; compressed artwork and looping remain unchanged. Its completion timer is 4800ms. Audio remains at native 1× speed, with no delays added to UI actions.
