# SallyMusic.com — static archive

A restoration of Sally’s late-2007 paper collage website. The actual archived homepage HTML, original stylesheet, backgrounds, artwork and animated crow anchor the visual reconstruction. A small archive menu opens recovered news, biographies, discography, lyrics, media descriptions and 70 real gigography entries. Ten original Sally Radio MP3 files play using browser-native audio controls.

The intended public site is **site/**. GitHub Pages should serve that directory, using the included Actions workflow. There is no server, database, dependency installation, analytics, executable legacy PHP or Flash. No current website or domain configuration is used.

## Sources and scope

- [Archived 2007 homepage](https://web.archive.org/web/20070828100657/http://www.sallymusic.com:80/cms/)
- [Archived tour page](https://web.archive.org/web/20070929161501/http://sallymusic.com/cms/?itemid=102)
- [Later preserved gigography](https://web.archive.org/web/20110715232633/http://sallymusic.com/cms/?itemid=102)
- Original matching skin artwork from the saved SallyMusic.com website.
- Recovered writing is in `content/`, with evidence links per entry and retained revisions.

The homepage represents a coherent archived layout. Reading-room pages combine surviving older sources and revisions, using the same skin for browsing. The archive menu, mobile adjustments and archival notice are restoration additions. Approximately 74 news posts were recovered, plus two text revisions. Missing database records and unavailable media are not reconstructed. CMS publication years are unassigned because they were not printed. Source dates are capture dates.

Newsletter, contact, comments, login, purchases and Flash are inactive. Email addresses are omitted from the public copy. Outbound historical links open Internet Archive captures. No original configuration, logs, credentials, databases or private contact lists are included.

## Run / rebuild

The generated site runs directly from any static host. For a local server:

```sh
python3 -m http.server 8000 --directory site
```

To regenerate HTML after editing `content/`, install `markdown-it-py`, retain the recovered source HTML/CSS in the ignored `source-material/` directory, and run `python3 build.py`. `site/` is already built and deployment does not require this tool or the recovery sources.

## Rights

Historical writing, photographs and artwork remain the property of their original owners. This archive does not grant them a new open-source license.
