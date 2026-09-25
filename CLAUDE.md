# CLAUDE.md: LEAP website

The public website of LEAP (Laboratory for the Economics of Africa's Past), Stellenbosch University. Repository `leapstellenbosch/leapstellenbosch.github.io`, live at https://leapstellenbosch.org. Read `README.md` for the file map.

## Ground rules

- **`main` is production.** Every push deploys within a minute. Preview before you push (`bundle exec jekyll serve`, or `python tools/preview.py` where there is no Ruby).
- **No build tools.** Jekyll 3 via the `github-pages` gem, whitelisted plugins only (`jekyll-seo-tag`, `jekyll-sitemap`, `jekyll-feed`). No Node, no bundlers, no CSS frameworks, no JavaScript libraries. Plain CSS and a little vanilla JS.
- **Content lives in `_data/` and `_posts/`**, never hard-coded in templates. Non-technical colleagues edit those files in the GitHub web editor, so keep the YAML shapes simple and keep the comment headers in each file accurate. If you change a shape, update `HOW-TO-EDIT-CONTENT.md` in the same commit.
- **Design tokens live in `:root`** in `assets/css/styles.css`. Do not introduce colours outside the tokens.
- **Never commit personal data**: no private email addresses, phone numbers, ID numbers, student records or internal reports. The only contact address on the site is leap@sun.ac.za.
- If you use a Liquid tag or filter that `tools/preview.py` does not know, add it there too.

## Design rules

- Maroon `#60223b` and gold `#a78e53` (Stellenbosch brand) carry at least 80% of the colour weight. The four letter accents (sage, earth, blue, plum) appear only as a page's header motif, its card rule and its eyebrow label.
- The only logo shown is the official SU + LEAP co-branded logo (`assets/img/logos/`). Never display, redraw or imitate the unofficial four-letter LEAP icon. Never recreate or alter the Stellenbosch logo.
- Headshots are black and white on a plain white background, and stay black and white on hover.
- The home page cover (letters, headline, text, buttons) must fit one screen without scrolling; its sizes scale with the viewport height (`svh`). Each letter's archival source appears as a caption on hover or tap. The sources rotate: an inline script in `index.html` draws one of five per letter from `_data/hero.yml` on every page load (L maps and places, E photographs, A handwriting, P printed documents). Add sources through the `HERO` list in `tools/treat-images.py`; use only LEAP's own archival material.
- Imagery is archival photographs, treated by `tools/treat-images.py`. The one exception is the "About LEAP" band on the home page, which shows one of LEAP's own photographs (`_data/gallery.yml`), black and white, drawn at random per visit. The quotation band on the home page rotates through `_data/quotes.yml`, each quotation over its own Elliott Collection photograph (Western Cape Archives, credited in the caption). No other event or launch photographs in the design itself. News posts may carry their own photos.
- Raleway for everything, ligatures off. Crimson Pro Italic only for quotations, dates and numerals.
- Dark pages, with exactly one light "paper" band per page.
- All motion respects `prefers-reduced-motion`.
- Accessibility: body text contrast at least 7:1 on the dark ground, labels at least 4.5:1, every image has alt text, the page works without JavaScript.

## Writing

Follow `/leapstyle`. Clear, precise English, active voice, no marketing adjectives, British/South African spelling. Run `/deslop` on any new copy. "Le Rossignol" has two s's and one l; "MacDonald" has a capital D.

## Which papers belong

Only economic history papers by LEAP team members go in `_data/publications.yml`. Johan's papers on cricket, the economics of science and other fields stay off the site, as do team members' papers outside history. Published articles are listed above working papers, on both the Research page and the home page.

## The team is fixed by Johan

The Team page shows photo cards for exactly the people in `_data/team.yml`, and below them, by name only, the extraordinary professors and research affiliates in `_data/affiliates.yml`. Do not add or remove people, board members or projects without Johan's instruction.
