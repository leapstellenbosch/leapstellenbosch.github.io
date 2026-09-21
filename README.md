# LEAP website

The website of the Laboratory for the Economics of Africa's Past (LEAP), Department of Economics, Stellenbosch University. Live at <https://leapstellenbosch.org>.

It is a static site built with [Jekyll](https://jekyllrb.com) and hosted on GitHub Pages. There is no database, no build tooling and no framework: plain HTML templates, one CSS file, one small JavaScript file, and content in Markdown and YAML.

## If you are a LEAP team member

You never need to install anything. You edit in the browser and the site rebuilds itself in about a minute.

- To add a news item: [HOW-TO-ADD-NEWS.md](HOW-TO-ADD-NEWS.md)
- To edit the team, projects, papers or datasets: [HOW-TO-EDIT-CONTENT.md](HOW-TO-EDIT-CONTENT.md)

## File map

```
_config.yml                 site-wide settings (title, URL, plugins)
index.html                  Home
news/  research/  team/  data/  contact/      one index.html per page
_posts/                     news items, one Markdown file each (YYYY-MM-DD-title.md)
_data/                      team, board, alumni, projects, publications, datasets, site copy
_layouts/                   default.html (page shell), post.html (a news item)
_includes/                  nav, footer, page head, cards, paper rows, project sections
assets/css/styles.css       the design system; colours and type are tokens in :root
assets/js/main.js           nav scroll state, mobile menu, scroll reveal
assets/fonts/               Raleway (SU corporate typeface) and Crimson Pro Italic (OFL), subset to Latin
assets/img/hero/            the twenty treated sources behind the home page letters (five per letter)
assets/img/archive/         treated archival photographs: motifs, quote band, social card letters
assets/img/projects/        treated project photographs
assets/img/team/ board/     headshots, 600px square
assets/img/news/            photos for news items
assets/img/logos/           the official SU + LEAP logo, for light and dark grounds
tools/treat-images.py       the photo pipeline (duotone, grain, crops). Run by hand, not part of the build
tools/make-motifs.py        draws the contour-map and weave motifs as SVG
tools/preview.py            rough local preview with Python only, no Ruby
_sources/headshots/         original headshots found online, with PROVENANCE.md
docs/news-template.md       copy-paste template for a news item
llms.txt                    plain-text index of the site for AI crawlers
.github/workflows/pages.yml builds and deploys the site on every push to main
CNAME                       the custom domain
```

## The design in one paragraph

Predominantly dark. Stellenbosch's Confident Maroon (`#60223b`) and Brilliant Gold (`#a78e53`) carry the colour weight, and the only logo shown is the official SU + LEAP logo. The four letters of LEAP each have a texture and an accent colour, drawn from LEAP's own archival sources: **L** a contour map in sage (Data, Contact), **E** archival paper in earth and sand (Research), **A** manuscript ink in blue (News), **P** a geometric weave in plum (Team). On the home page each letter is a window onto a treated archival source, drawn at random from five per letter on every visit (`_data/hero.yml`); pointing at a letter shows what it is. Each inner page carries its letter's motif in the header, and exactly one light "paper" band.

## Local preview

With Ruby (the real thing, identical to GitHub Pages):

```
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. On Windows install Ruby from <https://rubyinstaller.org> (Ruby+Devkit) first.

Without Ruby, a rough preview using Python with PyYAML and markdown-it-py:

```
python tools/preview.py
```

This re-implements only the subset of Liquid the templates use. It is good for checking layout and copy. The GitHub Actions build is the one that counts.

Add `?allin` to any address to switch off the scroll-reveal animation, which is useful for screenshots.

## Deployment

Every push to `main` triggers `.github/workflows/pages.yml`, which builds the site with the `github-pages` gem and publishes it. A failed build leaves the live site unchanged; the Actions tab shows what went wrong. The one-time setup of the organisation, Pages and the domain is described in [SETUP-github-and-domain.md](SETUP-github-and-domain.md).

There is no branch protection: team members commit straight to `main`. To require review later, add a branch protection rule for `main` under Settings → Branches.

## Regenerating images

The treated photographs are committed, so this is needed only when a source photograph changes. The sources are on Johan's Dropbox (`5 LEAP\Photos`); the paths and crop boxes are at the top of `tools/treat-images.py`.

```
python tools/treat-images.py            # everything
python tools/treat-images.py faces      # only headshots; also: archive, projects, card
python tools/make-motifs.py
```

## Credits

Raleway is Stellenbosch University's corporate typeface. Crimson Pro is licensed under the SIL Open Font License (see `assets/fonts/OFL-CrimsonPro.txt`). The contact map uses OpenStreetMap. Site content © Stellenbosch University.
