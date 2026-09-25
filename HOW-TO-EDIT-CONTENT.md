# How to edit the team, projects, papers and datasets

Everything on the site apart from news lives in eight small text files in the `_data` folder. You edit them in your web browser, the same way you add news (see `HOW-TO-ADD-NEWS.md`).

| File | What it controls |
|---|---|
| `_data/team.yml` | The team cards on the Team page |
| `_data/affiliates.yml` | The extraordinary professors and research affiliates, listed by name (with a link) on the Team page |
| `_data/board.yml` | The Governing Board |
| `_data/alumni.yml` | The table of PhD graduates |
| `_data/projects.yml` | The project sections on the Research page; the first four also appear on the home page |
| `_data/publications.yml` | Working papers and published articles |
| `_data/datasets.yml` | The data index (the table) on the Data page |
| `_data/site.yml` | Mission text, slogan, address, email, social accounts, and the text about the Kris Inwood Library |
| `_data/hero.yml` | The captions of the archival sources behind the four letters on the home page |
| `_data/lectures.yml` | The LEAP Lectures page: every lecture since 2016, with its film. Mark the coming lecture `upcoming: true`; after it has happened, remove that line and add the video id |
| `_data/quotes.yml` | The quotations on the home page, one drawn at random per visit, each over an archival photograph |
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

The Data page is an index: one row per paper whose data are public on GitHub. Put the data on GitHub first (the Data page lists the steps), then open `_data/datasets.yml` and add:

```yaml
- paper: "Wheat, Wine and Wealth"
  authors:
    - "Fourie, Johan"
    - "Links, Calumet"
  outlet: Economic History of Developing Regions
  data: Monthly wheat prices at the Cape Town market, transcribed from the Company's ledgers
  period: "1700–1800"
  released: 2026-10-01
  url: https://github.com/leapstellenbosch/wheat-wine-wealth
  doi: 10.5281/zenodo.1234567
  licence: CC BY 4.0
```

- Write each author surname first, with a comma: `"Links, Calumet"`. The page shows "Calumet Links", and sorts by surname.
- `released` is the date the data went public, in the form `YYYY-MM-DD`. The table lists the newest first.
- Leave `outlet` empty for a working paper, and `doi` empty until Zenodo has issued one.
- List only data that can be downloaded now. Nothing forthcoming.

## Worked example 3: a team photo

1. Crop the photo square with the face in the upper middle, at least 600 by 600 pixels, and save it as a JPEG.
2. Name it after the person's `key` in `_data/team.yml`, for example `noah-macdonald.jpg`.
3. In the repository open `assets` → `img` → `team`, click **Add file → Upload files**, drag the photo in and commit. A file with the same name replaces the old photo.
4. In `_data/team.yml` make sure the person's entry says `photo: true`. With `photo: false` the card shows the person's initials.

Photos always appear in black and white, whatever you upload, and a plain white background matches the rest of the team. Board photos work the same way, in `assets/img/board/`.

## Adding or removing a team member

Copy a whole entry in `_data/team.yml`, from its `- key:` line to the blank line after it. The `key` is the person's name in lower case with hyphens. The order of the file is the order on the page. To remove someone, delete their entry, and add them to `_data/alumni.yml` if they graduated with a LEAP PhD.
