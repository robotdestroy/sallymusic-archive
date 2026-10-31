# SallyMusic.com — static archive

A modern HTML/CSS/JavaScript reconstruction of Sally’s original Flash-era collage website. It retains authentic artwork, stage coordinates, illustrated navigation, the original main entrance timeline and flying menu. The 2007 plain-HTML alternative and recovered writing remain accessible, including approximately 74 news posts and 70 real gigography entries. Ten original Sally Radio MP3 files play using browser audio.

The intended public site is **site/**. GitHub Pages should serve that directory, using the included Actions workflow. There is no server, database, dependency installation, analytics, executable legacy PHP or Flash. No current website or domain configuration is used.

## Sources and scope

- [Archived 2007 homepage](https://web.archive.org/web/20070828100657/http://www.sallymusic.com:80/cms/)
- [Archived tour page](https://web.archive.org/web/20070929161501/http://sallymusic.com/cms/?itemid=102)
- [Later preserved gigography](https://web.archive.org/web/20110715232633/http://sallymusic.com/cms/?itemid=102)
- Original matching skin artwork from the saved SallyMusic.com website.
- Recovered writing is in `content/`, with evidence links per entry and retained revisions.

The HTML fallback represents a coherent archived layout. Reading-room pages combine surviving older sources and revisions, using the same skin for browsing. The archive menu, mobile adjustments and archival notice are restoration additions. Approximately 74 news posts were recovered, plus two text revisions. Missing database records and unavailable media are not reconstructed. CMS publication years are unassigned because they were not printed. Source dates are capture dates.

Newsletter, contact, comments, login, purchases and Flash are inactive. Email addresses are omitted from the public copy. Outbound historical links open Internet Archive captures. No original configuration, logs, credentials, databases or private contact lists are included.

## Run / rebuild

The generated site runs directly from any static host. For a local server:

```sh
python3 -m http.server 8000 --directory site
```

To regenerate HTML after editing `content/`, install `markdown-it-py`, retain the recovered source HTML/CSS in the ignored `source-material/` directory, and run `python3 build.py`. `site/` is already built and deployment does not require this tool or the recovery sources.

## Rights

Historical writing, photographs and artwork remain the property of their original owners. This archive does not grant them a new open-source license.

## Flash experience reconstruction

The homepage now reconstructs Sally’s original Flash 7 collage in modern HTML/CSS/JavaScript, using extracted original artwork and source-based navigation/movement. The earlier HTML fallback remains at [`html-site.html`](site/html-site.html), and every reading-archive URL is retained.

See [`reconstruction/SOURCES.md`](reconstruction/SOURCES.md) for chronology, matching Wayback hashes, exact asset/frame provenance and limitations. `reconstruction/build_data.py` prepares recovered prose for the experience. `build.py` rebuilds the HTML archive without replacing the reconstructed homepage. The main experience sources are `site/index.html` and `site/experience/`; there is no framework build or runtime dependency.
