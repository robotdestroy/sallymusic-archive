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
