# LEAP website

The website of the Laboratory for the Economics of Africa's Past (LEAP), Department of Economics, Stellenbosch University.

- **Review address (live now):** <https://leapstellenbosch.github.io>
- **Final address (not connected yet):** <https://leapstellenbosch.org>
- **Repository:** <https://github.com/leapstellenbosch/leapstellenbosch.github.io>

It is a static site built with [Jekyll](https://jekyllrb.com) and hosted on GitHub Pages. There is no database, no build tooling and no framework: plain HTML templates, one CSS file, one small JavaScript file, and content in Markdown and YAML.

## Status (21 September 2026)

The site is built, pushed and deployed, and is out for feedback at the review address. The custom domain has deliberately not been connected: Johan will set up `leapstellenbosch.org` on Porkbun once he is happy with the look.

Open items, none of which blocks anything:

1. **Feedback round.** Collect comments on the review site, then apply them.
2. **Connect the domain** when ready: Stage 3 of [SETUP-github-and-domain.md](SETUP-github-and-domain.md) (Porkbun DNS records, then Settings → Pages → Custom domain `leapstellenbosch.org`, then Enforce HTTPS). After changing the domain setting, run the "Build and deploy" workflow once more: the old redirect stays cached until a fresh deploy.
3. **Give colleagues access:** Stage 4 of the same guide.
4. **Content for Johan to check or supply**
   - The six project blurbs in `_data/projects.yml`, and his own research-focus line in `_data/team.yml`.
   - The three news posts in `_posts/`, each marked DRAFT in its front matter. The date of the Project 1834 conference (30 January 2026) is a guess.
   - Heinrich Nel's dissertation title and current position in `_data/alumni.yml` (graduated 2020).
   - Published articles by team members other than Johan: `_data/publications.yml` so far lists only his 2025–26 history articles.
   - Dataset periods in `_data/datasets.yml` ("1700s–1800s" for the Cape Panel and "After 1902" for the Constabulary records are placeholders), and whether "Uprooted" and "Path dependence" belong on a history-only Data page.
   - The captions of the letter sources in `_data/hero.yml`: the year of the first opgaafrol, the year of the Bantu World page, and the Rijksmuseum attribution of the Brandes watercolour.
   - The Kris Inwood Library text in `_data/site.yml` (his title, and "early in 2020" for the books' arrival), and the catalogue address when it exists.
   - Larger originals of the Karl Bergemann, Kate Ekama and Jan-Hendrik Pretorius portraits, which are only 300–400 px.
5. **Later:** move the data packages from `johanfourieza/research/2026/*` into repositories under `leapstellenbosch/`, and redirect the old `leapstellenbosch.org.za` site.

## If you are a LEAP team member

You never need to install anything. You edit in the browser and the site rebuilds itself in about a minute.

- To add a news item: [HOW-TO-ADD-NEWS.md](HOW-TO-ADD-NEWS.md)
- To edit the team, projects, papers, datasets or site text: [HOW-TO-EDIT-CONTENT.md](HOW-TO-EDIT-CONTENT.md)

## The pages

| Page | What is on it |
|---|---|
| Home | The cover (the four letters, the slogan, two buttons), mission and three facts, latest news, four projects, latest publications and working papers, the data band, the Maya Angelou quotation, the Stellenbosch band |
| News | Every post in `_posts/`, newest first, grouped by year. RSS at `/feed.xml` |
| Research | Current projects, published articles, working papers, the Kris Inwood Library (`#library`) |
| Team | The ten team members, the Governing Board, PhD graduates (newest first) |
| Data | Dataset cards, how to cite, the standard package layout for deposits |
| Contact | Email, addresses, links to the Department and the University, the X account, a map |

## File map

```
_config.yml                 site-wide settings (title, URL, plugins)
index.html                  Home
news/  research/  team/  data/  contact/      one index.html per page
_posts/                     news items, one Markdown file each (YYYY-MM-DD-title.md)
_data/site.yml              slogan, mission, addresses, links, social accounts, the library text
_data/team.yml  board.yml  alumni.yml         people
_data/projects.yml          project sections; the first four also appear on Home
_data/publications.yml      journal articles first, then working papers; history papers only
_data/datasets.yml          the cards on the Data page
_data/hero.yml              the 25 archival sources behind the letters on Home, with captions
_layouts/                   default.html (page shell), post.html (a news item)
_includes/                  nav, footer, page head, cards, paper rows, project sections, picture
assets/css/styles.css       the design system; colours and type are tokens in :root
assets/js/main.js           nav scroll state, mobile menu, scroll reveal, tap-to-caption on the letters
assets/fonts/               Raleway (SU corporate typeface) and Crimson Pro Italic (OFL), subset to Latin
assets/img/hero/            the treated sources behind the Home letters, 900px WebP
assets/img/archive/         treated archival photographs: page motifs, quote band, social card letters
assets/img/projects/        treated project photographs
assets/img/team/ board/     headshots, 600px square
assets/img/news/            photos for news items
assets/img/logos/           the official SU + LEAP logo, for light and dark grounds
tools/treat-images.py       the photo pipeline (duotone, grain, crops). Run by hand, not part of the build
tools/make-motifs.py        draws the contour-map and weave motifs as SVG
tools/preview.py            rough local preview with Python only, no Ruby
_sources/headshots/         original headshots, with PROVENANCE.md (where each came from)
_sources/hero/              SOURCES.md (origin and permission of every letter source) and one rendered census page
docs/news-template.md       copy-paste template for a news item
llms.txt                    plain-text index of the site for AI crawlers
.github/workflows/pages.yml builds and deploys the site on every push to main
CNAME                       the custom domain (ignored by the Actions build; the Pages setting decides)
CLAUDE.md                   conventions and guardrails for Claude Code sessions in this repository
LEAP-website-plan.md        the original build plan (kept locally, not in the repository)
```

## The design in one paragraph

Predominantly dark. Stellenbosch's Confident Maroon (`#60223b`) and Brilliant Gold (`#a78e53`) carry the colour weight, and the only logo shown is the official SU + LEAP logo. The four letters of LEAP each have a texture and an accent colour, drawn from LEAP's own archival sources: **L** maps in sage (Data, Contact), **E** photographs and pictures in earth and sand (Research), **A** handwriting in blue (News), **P** printed records in plum (Team). Each inner page carries its letter's motif in the header and exactly one light "paper" band. Headshots are black and white on a white ground.

## The home page cover

- The cover (letters, slogan, text, buttons) always fits one screen: its sizes scale with the height of the window (`svh` units in the `.hero` rules).
- Each letter is a window onto a treated archival source. On every page load an inline script in `index.html` draws one source per letter at random from `_data/hero.yml`: 5 maps, 7 photographs and pictures, 6 manuscripts and 7 printed records at present. Only the four chosen images download. Without JavaScript the first entry of each letter shows.
- Pointing at a letter, or tapping it on a phone, shows what the source is.
- To add a source: add a line to the `HERO` list in `tools/treat-images.py` (source file, crop box, rotation), run `python tools/treat-images.py hero`, add the image name and caption to `_data/hero.yml`, and note its origin in `_sources/hero/SOURCES.md`. Use only LEAP's own archival material or public-domain works, and prefer variety of source types.
- The slogan is `headline` in `_data/site.yml`: "Recovering the past to root the future."

## Local preview

With Ruby (the real thing, identical to GitHub Pages):

```
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. On Windows install Ruby from <https://rubyinstaller.org> (Ruby+Devkit) first. Johan's machine does not have Ruby.

Without Ruby, a rough preview using Python with PyYAML and markdown-it-py:

```
python tools/preview.py
```

This re-implements only the subset of Liquid the templates use, and builds into the system temp folder (not into Dropbox). It is good for checking layout and copy. The GitHub Actions build is the one that counts. To inspect a true build without Ruby, download its artifact: `gh run download <run-id> -R leapstellenbosch/leapstellenbosch.github.io`, then untar `artifact.tar`.

Add `?allin` to any address to switch off the scroll-reveal animation, which is useful for screenshots.

## Deployment

Every push to `main` triggers `.github/workflows/pages.yml`, which builds the site with the `github-pages` gem and publishes it, usually within a minute. A failed build leaves the live site unchanged; the Actions tab shows what went wrong. Pages is set to build from GitHub Actions (Settings → Pages → Source), not from a branch. The one-time setup of the organisation, Pages and the domain is described in [SETUP-github-and-domain.md](SETUP-github-and-domain.md).

There is no branch protection: team members commit straight to `main`. To require review later, add a branch protection rule for `main` under Settings → Branches.

## Regenerating images

The treated images are committed, so this is needed only when a source changes or one is added. The sources stay on Johan's Dropbox and are read from there: `5 LEAP\Photos`, `3 Data` (archive photographs, maps, gazettes, voters' rolls and more), `3 Cape Panel` and `Censuses`. The paths and crop boxes are at the top of `tools/treat-images.py`.

```
python tools/treat-images.py            # everything
python tools/treat-images.py hero       # only the Home letters; also: archive, projects, faces, card
python tools/make-motifs.py
```

Requires Python 3 with Pillow (and numpy with contourpy for the motifs).

## Credits and permissions

Raleway is Stellenbosch University's corporate typeface. Crimson Pro is licensed under the SIL Open Font License (see `assets/fonts/OFL-CrimsonPro.txt`). The contact map uses OpenStreetMap. Photographs from the AG and Elliott collections are used with the permission of the Western Cape Archives and Records Service, obtained in 2015, and are credited in their captions. The origin of every headshot and letter source is recorded under `_sources/`. Site content © Stellenbosch University.
