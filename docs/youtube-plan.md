# YouTube plan (draft for Adder)

Goal: the lesson videos bring people to the site. YouTube is the free sample; the site is where the practice, quizzes, sample exam and teacher material live.

## What goes up

| Group | Videos | Why |
|---|---|---|
| Free trig review (Unit 0) | all 7 | The site's free front door; trig gaps are what students search for. |
| One full unit | all of Unit 1 or Unit 2 | Shows the course end to end. Unit 2 (derivatives) is searched more. |
| Highlights from every other unit | 2 or 3 per unit | The lessons people search for: chain rule, related rates, FTC, volumes, series tests. |
| Everything else | later, or members only | Decide once Stripe and the free/paid plan are set (board: site-5). |

Upload only final versions: Adder's voice, 1080p, the review notes applied (board: videos-3).

## Channel layout

- One playlist per unit, in course order, plus "AP Calculus: start here" (trig review, then 1.1).
- A "Worked examples" playlist of short clips cut at example boundaries (the beat timings already mark them). These double as Shorts when vertical crops work.
- The channel banner and the end screen say the same thing: free practice, quizzes and a full sample AP exam at the site.

## Each video's page

- Title: what the student is searching for, then the topic number: "The Chain Rule, Explained Slowly | AP Calculus 3.1". No clickbait.
- Description, first two lines (what shows before "more"): one sentence on what the lesson covers, then the link to that lesson's page on the site.
- Then: links to the topic's practice, quiz and the sample exam; chapter markers from the beats (each beat already has a start time in voicemap_<slug>.json, so these can be generated); captions uploaded from our .vtt (ours are better than auto-captions, with math written as symbols).
- Pinned comment: the practice link again.

## The funnel to the site

- Every link carries a UTM tag (`?utm_source=youtube&utm_medium=video&utm_campaign=<slug>`) so the site can tell which videos send people.
- The landing page for a video link is that lesson, readable without an account, with practice one click away. Sign-up is asked for only when saving progress or taking the exam.
- End screen (last 10 to 20 s; the outro card already gives room): next lesson + "practice this on the site".

## What I can build once videos are final

- A script that writes each video's title, description, chapters and tags from the transcript and voicemap, plus the captions file, ready to paste or to upload through the YouTube API.
- Thumbnails generated in the course style (topic number, one big formula or picture from the lesson).

## Decisions for Adder

1. Which unit is fully free on YouTube (Unit 1 or Unit 2)?
2. Is a lesson on YouTube also free on the site, or does the site page ask for an account?
3. Channel name: the course name, or "Mr Oaks Math" to match the logo in the videos?
