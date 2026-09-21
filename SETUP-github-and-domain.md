# One-time setup: GitHub organisation, Pages and the domain

This is done once, by Johan. It takes about half an hour, most of it waiting for DNS. The website is already built and sits in `C:\Users\johanf\Dropbox\0Claude0\5LEAP\Website\`, committed to a local git repository on the `main` branch.

## Stage 1: the organisation and the repository

1. Sign in to <https://github.com> as `johanfourieza`.
2. Avatar (top right) → **Your organizations** → **New organization** → **Free**. Name it `leapstellenbosch`. Contact email: leap@sun.ac.za. It belongs to "My personal account".
3. Inside the organisation, click **New repository**.
   - Owner: `leapstellenbosch`
   - Name: exactly `leapstellenbosch.github.io`
   - Public
   - Do not add a README, .gitignore or licence. The folder already has them.
4. Push the site. In a terminal in the Website folder:

   ```
   git remote add origin https://github.com/leapstellenbosch/leapstellenbosch.github.io.git
   git push -u origin main
   ```

   Or ask Claude Code to do it: "push the LEAP website to the new repository".

## Stage 2: GitHub Pages

1. In the repository: **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**. Do not pick a suggested workflow: the repository already contains `.github/workflows/pages.yml`.
3. Open the **Actions** tab. The "Build and deploy" run should be in progress or finished. If it has not started, click the workflow, then **Run workflow**.
4. When it shows a green tick, the site is live at <https://leapstellenbosch.github.io>. Check every page before going further. This is the first real Jekyll build, so read the log if anything looks wrong.

## Stage 3: the domain leapstellenbosch.org (Porkbun)

1. Sign in to Porkbun → **Domain Management** → `leapstellenbosch.org` → **DNS**.
2. Delete Porkbun's default parked records (the ALIAS and CNAME records that point to `pixie.porkbun.com`).
3. Add these five records:

   | Type | Host | Answer |
   |---|---|---|
   | A | (blank) | 185.199.108.153 |
   | A | (blank) | 185.199.109.153 |
   | A | (blank) | 185.199.110.153 |
   | A | (blank) | 185.199.111.153 |
   | CNAME | www | leapstellenbosch.github.io |

4. Back on GitHub: **Settings → Pages → Custom domain**. Enter `leapstellenbosch.org` and save. GitHub runs a DNS check, which can take from a few minutes to an hour.
5. When the check passes, tick **Enforce HTTPS**. If the box is greyed out, wait; the certificate takes up to an hour. `www.leapstellenbosch.org` redirects to the main address automatically.
6. Recommended: in the organisation's **Settings → Pages**, add `leapstellenbosch.org` as a **verified domain**, so that nobody else can claim it.

The `CNAME` file in the repository already contains `leapstellenbosch.org`. Leave it there.

## Stage 4: give colleagues access

1. Organisation → **People → Invite member**. Enter each colleague's GitHub username or email, role **Member**.
2. Organisation → **Teams → New team**, called `LEAP team`. Add the members.
3. Repository → **Settings → Collaborators and teams → Add teams** → `LEAP team` → role **Write**.
4. Send each colleague the links to `HOW-TO-ADD-NEWS.md` and `HOW-TO-EDIT-CONTENT.md`.

Members edit the live site directly. There is no approval step, by design. If that changes, turn on branch protection: repository **Settings → Branches → Add rule** for `main`, and require a pull request before merging.

## Later

- Redirect the old `leapstellenbosch.org.za` site to the new domain once you are happy with it.
- Move the LEAP data packages from `johanfourieza/research` into repositories under `leapstellenbosch/`, then update the links in `_data/datasets.yml`. GitHub keeps redirects when a repository is transferred, but these are folders inside one repository, so they need new repositories.
