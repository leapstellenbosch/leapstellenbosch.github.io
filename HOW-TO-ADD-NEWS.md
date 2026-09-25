# How to add a news item

You need a GitHub account that is a member of the `leapstellenbosch` organisation. You do not need to install anything. Everything happens in your web browser and takes about five minutes.

## Steps

1. Open <https://github.com/leapstellenbosch/leapstellenbosch.github.io>.
2. Click the `_posts` folder.
3. Click **Add file → Create new file**.
4. Name the file with today's date and a short title, all lower case, words joined by hyphens, ending in `.md`:

   ```
   2026-09-21-karl-wins-dissertation-prize.md
   ```

   The date must be in the form `YYYY-MM-DD`. The rest becomes the web address of the post.

5. Paste the template below into the big text box and fill it in.

   ```
   ---
   title: "Karl Bergemann wins the EHSSA dissertation prize"
   date: 2026-09-21
   author: Johan Fourie
   summary: One sentence that appears on the news card.
   ---
   Write the news item here. Leave a blank line between paragraphs.

   You can make text *italic* or **bold**, and add a link like this:
   [the conference programme](https://example.org/programme).
   ```

   - Keep the three dashes `---` on their own lines, above and below the top block.
   - Keep the double quotes around the title.
   - Write your name under `author` exactly as it appears on the Team page, and the post will link to your card.

6. Click **Commit changes…**, then **Commit changes** again in the box that opens.
7. Wait about a minute, then refresh <https://leapstellenbosch.org/news/>. Your post is live.

The same template is saved in `docs/news-template.md`.

## Adding a photo (optional)

1. Make the photo a JPEG no wider than 1,600 pixels, and give it a simple name with no spaces, such as `karl-prize.jpg`.
2. In the repository, open `assets` → `img` → `news`, click **Add file → Upload files**, drag the photo in and commit.
3. Add two lines to the top block of your post:

   ```
   image: /assets/img/news/karl-prize.jpg
   image_alt: Karl Bergemann receiving the prize in Durban
   ```

If the photo is a small headshot of a speaker or visitor (narrower than about 1,000 pixels), add a third line, `image_portrait: true`. The post then shows it small and in black and white, instead of stretching it across the page.

Use photos you took or have permission to use. Ask the people in a photo before you post it.

## Changing or removing a post

Open the file in `_posts`, click the pencil icon, make the change and commit. To remove a post, open the file, click the three dots at the top right and choose **Delete file**.

## If the post does not appear

Open the **Actions** tab of the repository. A green tick means the site was rebuilt; give it another minute and refresh with Ctrl+F5. A red cross means the build failed, and the live site stays as it was, so nothing is broken for visitors. Click the failed run to see the message. The usual causes:

- A missing closing quote in the title: `title: "My title` should be `title: "My title"`.
- A colon inside an unquoted line, for example `summary: LEAP lecture: a success`. Put the whole line in double quotes: `summary: "LEAP lecture: a success"`.
- A file name that does not start with a date in the form `2026-09-21-`.
- A date in the future. Posts dated ahead of today stay hidden until that day.

Fix the file, commit again, and the site rebuilds. If you are stuck, write to Johan.
