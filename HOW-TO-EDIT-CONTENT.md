# How to edit the team, projects, papers and datasets

Everything on the site apart from news lives in eight small text files in the `_data` folder. You edit them in your web browser, the same way you add news (see `HOW-TO-ADD-NEWS.md`).

| File | What it controls |
|---|---|
| `_data/team.yml` | The team cards on the Team page |
| `_data/board.yml` | The Governing Board |
| `_data/alumni.yml` | The table of PhD graduates |
| `_data/projects.yml` | The project sections on the Research page; the first four also appear on the home page |
| `_data/publications.yml` | Working papers and published articles |
| `_data/datasets.yml` | The cards on the Data page |
| `_data/site.yml` | Mission text, slogan, address, email, social accounts, and the text about the Kris Inwood Library |
| `_data/hero.yml` | The captions of the archival sources behind the four letters on the home page |
| `_data/gallery.yml` | LEAP's own photographs in the "About LEAP" band on the home page, one drawn at random per visit, with captions |

## The general method

1. Open <https://github.com/leapstellenbosch/leapstellenbosch.github.io> and click `_data`.
2. Click the file, then the pencil icon at the top right.
3. Copy an existing entry, paste it where the new one should go, and change the details.
4. Click **Commit changes…** and confirm. The site rebuilds in about a minute.

Three rules keep the files valid:

- **Indentation matters.** Every entry starts with `- ` at the left margin, and the lines under it are indented by two spaces. Use spaces, never tabs.
- **Put text in double quotes** if it contains a colon, a quotation mark or starts with a special character. When in doubt, use quotes.
- **Leave a field empty rather than deleting it**: `url:` with nothing after it is fine.

If the build fails, the Actions tab shows a red cross and names the file and line. The live site stays as it was until you fix it.

## Worked example 1: a new working paper

Open `_data/publications.yml`. Journal articles come first in the file and working papers second, each list running from newest to oldest. Add the entry at the top of the working papers:

```yaml
- title: "Wheat, Wine and Wealth: Cape Farm Productivity, 1700–1800"
  authors: [Johan Fourie, Calumet Links]
  year: 2026
  type: working_paper
  series: Stellenbosch Economic Working Papers
  number: WP08/2026
  url: https://www.ekon.sun.ac.za/wpapers/2026/wp082026/wp082026.pdf
```

Write authors' names exactly as they appear on the Team page and the site sets them in bold and links them to their cards.

A published article has `type: article`, a `journal:` and a `doi:`, and no `series` or `number`:

```yaml
- title: "Running towards: Labour market incentives for runaway slaves in the British Cape Colony, 1830–1838"
  authors: [Karl Bergemann, Gabriel Brown, Johan Fourie]
  year: 2026
  type: article
  journal: Asia-Pacific Economic History Review
  doi: 10.1111/aehr.70034
  url: https://doi.org/10.1111/aehr.70034
```

## Worked example 2: a new dataset

Open `_data/datasets.yml` and add:

```yaml
- name: Cape Colony wheat prices
  period: "1700–1800"
  status: Released
  description: >-
    Monthly wheat prices at the Cape Town market, transcribed from the
    Company's ledgers.
  size: "1,200 monthly observations"
  licence: CC BY 4.0
  url: https://github.com/leapstellenbosch/wheat-prices
  citation: "Fourie, J. and Links, C. (2026). Wheat, Wine and Wealth."
```

`status` is either `Released` or `Forthcoming`. The `>-` after `description:` lets the text run over several indented lines.

## Worked example 3: a team photo

1. Crop the photo square with the face in the upper middle, at least 600 by 600 pixels, and save it as a JPEG.
2. Name it after the person's `key` in `_data/team.yml`, for example `noah-macdonald.jpg`.
3. In the repository open `assets` → `img` → `team`, click **Add file → Upload files**, drag the photo in and commit. A file with the same name replaces the old photo.
4. In `_data/team.yml` make sure the person's entry says `photo: true`. With `photo: false` the card shows the person's initials.

Photos always appear in black and white, whatever you upload, and a plain white background matches the rest of the team. Board photos work the same way, in `assets/img/board/`.

## Adding or removing a team member

Copy a whole entry in `_data/team.yml`, from its `- key:` line to the blank line after it. The `key` is the person's name in lower case with hyphens. The order of the file is the order on the page. To remove someone, delete their entry, and add them to `_data/alumni.yml` if they graduated with a LEAP PhD.
