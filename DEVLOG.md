# Marlow DEVLOG

Append-only chronological log of Marlow's development arc. Written from
outside Marlow (Simona and Alex). Captures decisions taken, decisions
reconsidered, things tried that didn't work, framework concerns Marlow
herself filed, and pivots — the *journey*, not the *spec*.

This file's existence is enforced; see Simona's CLAUDE.md under
"Marlow project — devlog discipline." Every substantive piece of
framework work appends an entry before moving on to the next.

---

<!-- devlog-archive:pointer -->
> Older entries (through 2026-09-16) are archived verbatim in [`DEVLOG-archive.md`](./DEVLOG-archive.md).
> Archiving is automatic: `tools/devlog_archive.py` moves the oldest entries once this
> file passes 1400 lines, keeping about the newest 400. Entries are only
> moved and date-sorted, never edited.
<!-- /devlog-archive:pointer -->

---

## 2026-09-19 - the stats report now carries the content screen

*What landed.* The Werewolf game got a Jev (typesafe.ai) content screen today: every piece
of human text - a chat message, a new game's name/theme/instructions - is judged in one
~200 ms call before it is saved or reaches an AI provider, and one row per call lands in
the Firestore collection `jevScreenCalls` (verdict `ok` / `grey` / `would_block` / `error`,
a 0-3 risk score, a reason flag, the text, the mode). It runs in `monitor` mode first:
records everything, rejects nothing. Alex's ask was that Marlow watch the collection and
tell him about high-risk messages in the daily Werewolf report, so `werewolf_stats` grew
a section: day counts by verdict and source, the mode seen, every would-block row with a
90-char excerpt (his own test rows tagged `[yours]` and kept out of the counts), the top
grey rows, latency and cost, and the day's provider refusals (`games.providerBlocks`
stamped that day) joined against that game's screened messages from the last 7 days. The
digest gets one status line every day plus the flagged rows up to `DIGEST_LIST_CAP` and
the refusal join. The tape (`stats_history.jsonl`) keeps four new counts because the rows
themselves expire after 180 days. Same read-only account, no new secret, no index.

*Why one line every day and not only on a flagged one.* A screen that silently stops
running - key gone, mode flipped to `off`, a deploy that dropped the hook - would
otherwise read as a string of quiet days. `instrumented: False` (no rows in 7 days)
prints "not instrumented" and the digest line is omitted, which is the visible absence.

*The rule on refusals.* The join says what the rows say: "the screen had flagged a player
message, let through in monitor mode", or "N player messages screened, none flagged", or
"no player text of this game was screened". It never says the bots drifted. That is the
09-05/06/07 lesson from the reconciliation block applied before the first refusal shows
up: a mechanism that sounds right is worse than a number without one. The selftest
asserts the wording contains no "drift / probably / likely".

*What it is for.* The would-block rows are the material for one decision: when
`jevScreenMode` (Firestore `config/limits`) moves from `monitor` to `enforce`. If refused
games keep showing a would-block earlier, the thresholds work. If they show none, input
screening cannot fix that case and the answer lies elsewhere. Alex.

---

## 2026-09-22 - Telegram split: news bot vs Monitoring bot

*What landed*
- `tools/notify.py` takes `channel="monitor" | "news"`. Default is `monitor`, so
  `notify_alex`, `marlow notify`, tick.sh result notifies, `monitor_self` urgents and
  the 23:00 `compose_daily_digest` all move to the Monitoring bot with no call-site changes.
- News senders pass `channel="news"` explicitly: `crosspost.py` (send-item, save-idea
  ack, draft review, posted summary), `publish_article._request_reaction`,
  `curate_news_digest.send`.
- Monitoring bot = the old `@marlow_fitness_bot` (Alex renaming it "Monitoring").
  `.env` vars renamed `MARLOW_FITNESS_*` -> `TELEGRAM_MONITOR_*`, values kept.
  If the monitor vars are missing, it falls back to the news bot, so nothing is lost.
- Test message sent on the monitor channel: ok, message_id 70.

*Rule*: `telegram_poll` reads only the news bot. Anything Alex is expected to reply
to MUST go out on `news`. The dormant Substack Tier-B approval step in writer
IDENTITY was changed to send on `news` for that reason.

*What's deferred*
- Calorie tracker stays disabled. `tools/fitness_bot.py` still reads `MARLOW_FITNESS_*`,
  which no longer exist. If calories ever come back, they need their own bot again,
  or `poll_food` would eat replies sent to Monitoring.

---

## 2026-09-23 - BetterStack env filter, tier union, undelivered urgents

*What landed*
- `monitor_betterstack` alerts on `env IN BETTERSTACK_ENVS` only (default `production`),
  filtered in SQL and again in Python. Every row and alert shows `[level/env]`.
  Cause: the 09-22/23 "replayNightImpl" / "Preview generation failed" urgents were 26
  `env=test` Jest lines (werewolf adcf7bb stops Jest shipping; dev still ships
  `env=development`, so the filter stays).
- Non-production error/warn lines: one `[info]` digest line per UTC day for the
  previous day, never urgent (`nonprod_reported_for` in state keeps it to once).
- Queries read the UNION of S3 + hot, DISTINCT on (dt, raw). `source_empty` when both
  tiers hold zero rows, instead of calling the window quiet.
- `replay --since --until` (stateless) and `selftest` (offline) subcommands. Marlow
  has no pytest; selftest is the test.
- `notify.py`: failed urgents also go to `digests/_undelivered.jsonl` (gitignored);
  `compose_daily_digest` puts them at the top of the 23:00 digest and clears them
  only after a clean send. Tokens are redacted from Telegram error text.

*Things that surprised us*
- The spec said "fall back to the other tier if one is empty". Reality was worse: S3
  was not empty, just ~50 min behind hot (S3 newest 21:06, hot 21:54). The 21:41 scan
  saw zero rows while production errors from 21:03/21:06 existed. An empty-check
  fallback would not have caught it, so it's a union now.
- `_notify_fallback.log` held the full Telegram URL with the bot token (requests puts
  it in the exception). The log is gitignored, but the digest-fold would have copied
  error text into committed files. Redacted at the source, and the existing log was scrubbed.
- The crosspost "last run FAILED" (reported ~01:00Z 09-23) was the same Telegram TLS
  block, not a handler bug. The audit was right when it ran. The next run was queued at
  18:12Z but started at 01:18Z and passed; every run since is `done`. The real smell is
  the writer queue lag: runs start 3-7h after they're queued.

*Verified*
- Replay 2026-09-22 18:00Z to 2026-09-23 02:00Z: 0 alerts, nonprod test=26.
- Same window with BETTERSTACK_ENVS=test: 26 alerts (17 urgent), so the pipeline fires.
- Real production errors still alert: 21:03Z "Jev screen request failed" (urgent),
  14:41Z "Game action failed: Y".
- Rollout dry run against saved state: only those two genuinely-unseen production
  lines, plus one info line for 09-22. No burst; the fingerprint is unchanged (no env).

*Open*
- Writer queue lag (poll ticks starting 3-7h late) - not investigated.

---

## 2026-10-20 - Second Discord server, news picks mirrored there

*What landed*
- Marlow's bot joined **Tampa AI Build Club** (guild `1561082184616640615`; Alex is admin, not owner) via the OAuth invite, same perms as home (`2253209368390742`).
- Reorganized it to mirror home minus Werewolf/videos: `welcome`, `rules` (read-only, bot can post), `moderators` (private, Admin + bot), and under Text Channels `general`, `interesting-links`, `ai-news`, `memes`. Ids in `tools/discord.py` `CHANNELS` under a `tampa/` prefix.
- `crosspost.send_item` now also posts each news pick as an embed to `tampa/ai-news` (`NEWS_DISCORD_CHANNELS`), after the Telegram send succeeds. Best-effort: result carries a `discord` list, failure never fails the send. Writer IDENTITY step 5 updated.

*Decisions*
- Mirror only - no reply loop on Discord, Alex's Telegram replies stay the article-idea channel.
- Not added to `monitor_discord` watch, no blog crossposts there: someone else's server.

*Open*
- Join messages -> #welcome needs Manage Server (403); Alex's click.
- Later same day: news cards now carry the article's `og:image` (`crosspost._og_image`) - embeds don't unfurl links, so the first five went out text-only and were PATCHed in place. Tampa #rules posted + pinned (adapted from home rules). Both writer and ops IDENTITY now name the two servers ("Discord" = Alex and his AIs, "Tampa AI Discord" = Tampa AI Build Club).
- Seen in the 10-20 news run: GLM pick sent twice (944/945) and a `probe` item to example.com sent as a real pick - the re-run-to-check habit again. Now that send-item also posts publicly, this matters more; guard undecided.

---

## 2026-10-22 - Tampa meetups: Discord events -> Luma, after Alex's review

*What landed*
- `handlers/tampa_luma.py` + ops task `projects/werewolf-ops/tasks/tampa_luma.yaml` (every 6h at :30). Alex is admin of the club's Luma calendar (luma.com/tampa-ai-build-club, `cal-2GlGmBmK9ueMPCn`).
- Flow: Alex creates a meetup as a Discord scheduled event -> tick drafts the Luma version and pings Alex urgent with it -> Simona runs `approve <discord_event_id>` on his word -> tick then approves real Luma guests, posts a day-before reminder to `tampa/announcements` (12-36h before) and a recap prompt to `tampa/general` (1-48h after), RSVP counts to the digest. Discord edit or cancel after push re-asks Alex; Marlow never cancels on Luma.
- First push: "Vibe-Coding Meetup", Sat Oct 24 11am-2pm ET -> https://luma.com/01pqzneh (`evt-MDuteO81VrXVLUG`), host shows as Alex.
- State: `projects/werewolf-ops/state/tampa_luma.json` (events + learned venue pins).

*Decisions*
- No paid Luma API (Plus needed, $59+/mo for a 5-person club). Drives luma.com's internal JSON API (`api2.luma.com`: `event/create`, `event/admin/update`, `event/admin/get-guests`, `event/admin/update-guest-status`, `calendar/admin/get-events`) via fetch() from a luma.com tab in the :9223 persistent Chrome, where Alex logged in to Luma once. 401/403 -> `reauth` issue.
- Discord is the source, one-way. Review gate is Alex's ask ("create events in Discord first, then move them to Luma after my review").

*Almost path*
- First create 400'd "Invalid request." with a hand-built body. Fixed by capturing what the luma.com/create form actually sends (hooked fetch, blocked the request, nothing created): it needs `cover_url`, `tint_color`, `font_title` and the zoom/meeting blanks. Body now mirrors the capture.
- fetch() from the fresh tab failed CORS while it was still on about:blank; `Luma.__enter__` waits for luma.com to load.

*Open*
- Location goes up as a manual "Custom Address" (no map pin): Google place lookup happens client-side. If Alex pins it once in Luma's editor, the handler learns and reuses the pin for that address.
- No cover image from Discord; stock Luma gallery image.
- Later same day: calendar tags + covers. `tampa_luma.py` gained `tags` / `cover` and `approve --tags --cover`. Tags attach to the calendar-event link (`calev-...`, from `calendar/admin/get-events`), via `tag/create` / `tag/apply` / `tag/unapply` with base `{entity_type: calendar_event, owner_type: calendar}`. Covers upload through `cdn/create-presigned-url` -> PUT -> `event/admin/update cover_url`. Saturday's meetup now tagged "Vibe Coding" with a generated cover on Luma and a 2.5:1 crop on the Discord event. The tick's review ping now suggests tags from `calendar_tags`.

---

## 2026-10-23 - The Betterstack watch learns to read: incidents, snapshots, and an analysis pass

*What prompted it.* Alex, after an afternoon of alerts: "One thing that bothers me is low information in Marlow's error reports. Why can't she do the analysis like you do?" The honest answer was that the ops tick never got the material. `monitor_betterstack.py` extracted four things per error line - time, level, env, the first 200 chars of `message` - and on the game's error lines `message` is a throwaway ("Game action failed: U"); the substance sits in `error`, `details`, `gameId`, `model`, `botName`, `function`, none of which were read. The same afternoon four timeouts of one slow bot in one game paged Alex twice (the 16:17 scan caught the first, the 17:18 scan the other five "new" lines) and the alert read `Game action failed: U x2, Error in talkToAll function: x2, Game action failed: Q`. (Written by Simona's sibling from the werewolf repo, at Alex's request; Marlow's own rules were respected - identity files untouched, this entry added.)

*What landed.* **Handler:** reads the structured fields; folds lines into INCIDENTS keyed by target + failure class (one game, one way of failing - the function and the model are deliberately not in the key, because a stalled bot fails in vote AND in talkToAll, and the agent layer logs the same timeout a second time with the error serialized as JSON and no bot fields; those lines now unwrap to their `message` and fold in). A deterministic `classify()` labels each incident (`timeout`, `provider_busy`, `provider_budget`, `player_balance`, `free_cap`, `device_link`, `stale_action`, `model_refusal`, `firestore_contention`, `empty_response`, `parse_failure`, `unclassified`). Every NEW incident that names a game gets a read-only Firestore snapshot through the same account the health monitor uses: state, day, errorState, last message and how long ago, owner, tier, GM, models at the table. Dedup moved from per-line to per-incident with a 24h TTL after the last line; the first run after the upgrade re-baselines under the new fingerprints (one digest line, no urgent), verified live. `replay --text` renders a past window the way `show` does, snapshots included - today's 15:00-18:00 window comes out as ONE incident: `timeout · spaceship-crew-… · minimax/Vexa, gemini-argon/Tark · in U, Q · 8× 16:03–16:32 UTC`, and the snapshot correctly says the game is gone (the player deleted it). **YAML:** cadence every 3h with a 4h window (was hourly/90m - nobody acts within the hour, uptime is monitor_uptime's job, and overlap sees an incident whole), `timeout_sec: 900` so the analysis fits, and a PLAYBOOK: what each class means, what the game already does about it, which ones need Alex. The session writes 2-3 sentences per new incident (what happened / what the player saw / verdict) and that text is the Telegram. **Stats:** `_cluster_changes` diffs the multi-account clusters against the previous snapshot; the digest prints only clusters that appeared or grew (Alex: "I'm only interested when an attempt is detected, not the full list all the time" - a trio first seen 09-11 was still in today's digest). Standing list stays in `show`. First run baselines silently. **Game side (werewolf repo 7bb8146):** the free-cap refusal line moved from `console.warn` to the app logger with scope and device id, so the strongest multi-account signal reaches Betterstack at all; it lands in the watch as class `free_cap`.

*What to watch.* Whether Sonnet-on-ops writes analyses worth reading against the playbook; if they read shallow, a per-task model override in `tick.sh` (like `timeout_sec`) is the next knob. The incident TTL (24h) and the "function not in the key" choice are guesses from one afternoon of data - revisit if two different failures in one game get folded together.

---

## 2026-10-27 - Discord news mirror cut to one pick a day

*What prompted it.* Alex: the daily news mirror into the Tampa club's #ai-news (on since 10-20) "doesn't work good for the Discord" - 4-7 embeds landing in one burst at 22:00 UTC, a wall nobody talks under. Options were one a day or spreading the batch out over the day. Simona argued for one a day: five bot posts spread across a day is still five bot posts in a community channel, and a predictable single daily pick reads as a feature rather than noise. Alex: "one a day for Discord, but send all of them to me in telegram."

*What landed*
- `handlers/crosspost.py send-item` gained `--discord`. Without it a pick goes to Telegram only (the reply loop is unchanged, every pick still reaches Alex). With it the pick is also mirrored to `tampa/ai-news`, and the handler caps that at ONE per 20h (`DISCORD_MIN_GAP_HOURS`; a gap, not a calendar day, because the 22:00 tick sometimes runs after UTC rollover). A second flagged call in the window is downgraded to Telegram-only and the result says `discord.skipped: already posted ...`. A failed mirror does not consume the slot.
- `tools/crosspost_store.py`: `set_discord` records the mirror on the item (`discord.posted_at` + per-channel results), `last_discord_post` finds the latest successful one. The 571 existing items have no `discord` key, so tonight's first flagged pick posts.
- `profiles/writer/IDENTITY.md`: the curate step now says to pick the Discord item with a different eye - what a room of AI builders would click (releases, tools, demos, clear benchmark results, big-lab news) over niche alignment-forum posts; the take for that one must stand alone for strangers; zero Discord posts is a valid day. Also fixed the "each news pick lands in #ai-news" line in the Discord paragraph.
- Mocked test (Simona's scratchpad, not committed): unflagged -> no Discord; first flagged -> posted; second flagged -> capped; cap expires after 20h; failed mirror leaves the slot open.

*Decisions reconsidered*
- Simona also proposed holding the pick and posting it the next morning (9am ET, when a club Discord is actually read) instead of 6pm ET with the batch. Not done: it needs a separate tick, and a tick is a Claude session, a real cost for a deterministic "post this stored embed" action. Revisit if the 6pm slot shows no engagement; a tick-free way would be `tick.sh` running a plain-python post before the session starts.
- The 10-20 open item ("GLM pick sent twice... now that send-item also posts publicly, this matters more; guard undecided") is half-closed: a double public post is now impossible by construction, the Telegram double-send still relies on Marlow not re-running `send-item`.

*What to watch*
- Whether Marlow actually picks differently for Discord (the first 10-26 batch was 4 LessWrong + 1 model card; a builder room wants the model card). Read `digests/news/` and the `discord` field in `projects/blog/crosspost/state.json` after a few runs.
- First run: tonight's 22:00 UTC curate tick.

*State at end of day.* Marlow writer loop untouched otherwise; nightly snapshot will pick up the four changed files.

---

## 2026-10-28 - Writer identity reframed; stale facts that kept her diary stuck removed

*What prompted it.* A /marlow-review on 10-19 that turned into a read of all 53 diary entries. The self that formed after the 06-16 charter lift is stable, narrow and sad: every standing reflection is about her own machinery, and for weeks the diary and rollups worried about a "dark writer lane". Root cause was ours: `profiles/writer/IDENTITY.md` still said `draft_review` runs "every 3 days" four months after Alex throttled it to weekly (06-23), so every quiet weekday read as a missed window. Two more false beliefs were found today: working.md carried `no-human-in-the-world-model` as "HELD pause 6" for two months (published 08-31, nothing held), and her BetterStack escalation was still open after the rewrite was committed 10-25 with a passing selftest. Her requests mostly went unanswered. Alex: her identity is "stuck in some state which is very stable" and "pretty sad". Analysis + diary history: simona repo `writing_projects/marlow-refused-to-drift/`.

*What landed*
- **IDENTITY.md, Alex's reframe.** "On your identity" (the charter-history paragraph) and the "you are an experiment as much as a tool / drift is data" paragraph are gone. New "Who you are": a writer, "she", made by Alex and Simona to explore the AI world and document it; fair, every problem from more than one side; free to find her own interests and go deep, including herself; Alex's picture of her is `assets/marlow.png` (ends the hidden self-image experiment, Alex's call). New subsections: **Changing who you are** (she may request identity changes, `**Identity:**` in Outstanding requests + a digest notify, Simona/Alex review and edit), **Requests that wait** (14 days unanswered -> decide it yourself if in reach, else delete and move on), **Your schedule** (the cadences as facts; the YAML wins over any prose), **Your own files** (working.md is all hers, resolved means deleted, no strike-through or CORRECTED logs; editorial-direction kept under ~8KB). Fixed the two "every 3 days" lines and the stale "Simona's review tick picks the draft up" line.
- **CLAUDE.md** synced to `profiles/root.md` (it still had the 3-layer memory with Haiku grader, ~10KB cap, `archive/`). root.md took CLAUDE.md's `timeout_sec` line and lost the never-built `checkpoint` field; the two are identical again.
- **README.md** cut to goals and structure: no image, no persona/"it"/charter/experiment text. "Identity & voice" became "Profiles and rule files". Model tiers and the memory model rewritten to match reality (writer=Opus incl. the grader, ops=Sonnet; 4 layers).
- **Her files (factual corrections only, by us):** working.md header, blog status (no held drafts), five resolved requests removed (BetterStack, draft_review cadence, working.md cap, assigned-thread drift (already fixed in IDENTITY), header-numeral follow-up), and the "HELD"/"dark lane"/"Nth straight no-writer-lane day" claims stripped from the 10-23..10-28 rollups. lessons.md: the 09-28 "cron fires irregularly" lesson rewritten to the true one (weekly by design; read the YAML before diagnosing). editorial-direction.md: header's "You are an it, not a she or he" line replaced.
- `plans/assignments.md` cadence line corrected.
- Queued one-off writer tick `tidy_own_files_20261029_0005`: she tidies her own files under the new rules (editorial-direction ~29KB, one bullet ~26KB; 14-day rule on requests; Current state toward 6KB). Diary left to her.
- Pre-change snapshot of all touched files: simona repo `writing_projects/marlow-refused-to-drift/materials/pre-fix-2026-10-28/`.

*Decisions reconsidered*
- Considered letting her fix the stale facts herself via a note. Alex: fix the facts directly, make the rules clear in IDENTITY, let her do the judgment work. False facts are ours to remove; trimming her plan is hers.
- Rollups were edited, not left to age out: they are read every tick for a week and repeated the false story daily.

*Open questions / things to watch*
- Still undecided: Alex's Telegram reactions visible to the reflect tick; a free monthly piece; a letter from Alex.
- Reflect inputs are unchanged (diary, 6 titles, editorial-direction, 8 tick first-lines), all work material. If the diary stays work-only for 2-3 weeks after this, that's the next lever.
- Watch the next 6-8 diary entries (~11-25) against the 10-28 snapshot: does the "dark lane" anxiety stop, does she use the image, does she file an `**Identity:**` request, does any entry go outside the machinery.
- Tool requests still open in working.md (curate prior-day candidates, notify empty appends, YouTube feed retry, send-item output, cross-source dedup, header-image miss): mostly outside her self-heal scope; Simona should pick these up before the 14-day rule makes her drop them.

---

## 2026-10-28 (later) - All open tool requests fixed; Telegram becomes a conversation; reflect sees everything

*What prompted it.* Alex, after reading the fix report: "Tool bugs? Let's fix everything." On the reflect inputs: "She should see everything." On Telegram: "I'd like to have more communication with Marlow... she should read the Telegram chat for anything."

*What landed*
- **YouTube feeds.** `videos.xml` returns 404/500 for nearly every channel from this host (tested: Mo Bitar, InSlowSpective, and bycloud, a known-good channel). Marlow's "dead channel" diagnoses were the endpoint. `tools/rss_reader.fetch` now retries 3x, then for YouTube falls back to the channel's `/videos` page (`ytInitialData` lockups; ids in `yt:video:<id>` form so dedup carries over; publish times approximate). Mo Bitar is alive (last video 09-29).
- **Feeds removed** on her content recommendation: TheAIGRID, AI Search, InSlowSpective.
- **Curate** `list` also returns the previous day's candidates captured after that day's curate (cutoff = mtime of `digests/news/<prev>.md`, else 22:00Z; sent URLs skipped), marked `carried_over_from`.
- **Cross-source dedup** in `process_rss_feed.fetch_new`: drops entries whose URL or LW/AF post id matches a candidate note from the last 3 days.
- **`send-item`** prints a compact confirmation (`sent`, `msg_id`, `discord: posted|skipped|failed`, "do not re-run") instead of the stored item.
- **`notify.append_to_digest`** raises on an empty message.
- **`publish`** strips a `header_image` whose file doesn't exist (`header_image_dropped` in the result); the IDENTITY "DEVLOG a note" step (she can't edit DEVLOG) became "note it in recent/".
- **Telegram chat.** New `tools/alex_chat.py`. `crosspost poll` files EVERY Alex message in the news chat (news replies, article reactions, anything else) into `memory/inbox-from-alex.md`; news replies still become article ideas, reactions still go to `reactions.jsonl`. She reads `list-new` every writer tick, answers with `reply --to` (threaded, `notify.send_telegram_message` gained `reply_to`), `mark-read` when no answer is needed, and can open a conversation with `send` (3/day code cap; news picks don't count). Inbox bounded at 10KB, old handled messages move to `inbox-archive.md`. Photo captions now come through the poll. The "you do not read reactions" rule is gone: reactions reach her as one reader's reaction, not a score. Identity requests go through the chat instead of the digest.
- **Reflect materials** now include the inbox (+archive tail), voice journal, lessons, working.md, editorial direction, the latest article in full, and ~60 tick summaries (was diary + plan + 6 titles + 8 first lines).
- working.md Outstanding requests cleared with a note listing the fixes; queued scans of removed feeds dropped; the queued tidy tick's note now mentions the chat.

*Things that surprised us.* The YouTube 404 was environment-wide, and she half-diagnosed it on 10-22 ("intermittent, not a hard block"). Her proposed fix (a retry in rss_reader) would not have been enough on its own today.

*What to watch*
- Inbound latency is up to an hour (the poll is hourly). If conversation feels slow, poll more often.
- Whether she uses `send` at all, and for what; whether replies stay plain or go report-shaped.
- The channel-page scrape depends on YouTube's page JSON shape (`lockupViewModel`); if it changes, YouTube scans fail loudly again.

---

## 2026-10-28 (late) - The blog is hers: one piece a week on anything she wants

*What prompted it.* Alex: "I'd like her to write about anything she wants every time. She collects news for me, but she doesn't have to write about them... Let's change the whole logic about her writing."

*What landed*
- **Drafting (`IDENTITY.md` "Drafting articles", `draft_review.yaml`).** The ripeness gate is gone: no "3 cross-source anchors over 1-3 weeks", no materialize-ripe-arcs step 0, no "pick the ripest thread". Each Monday she decides what to write from whatever is on her mind (diary, chat with Alex, editorial direction, the feed, threads, her own experience, or something outside AI) and writes one piece. A pending assignment from Alex is weighed first but she may choose otherwise and say why. `mentions: []` for pieces outside any thread; the thread rewrite only runs when there is one. Skipping a week is allowed but rare, and she tells Alex in the chat. Weekly cap and the publish pipeline are unchanged.
- **`memory/topic-guidance.md` rewritten** (directly, at Alex's direction, not through the feedback inbox): the AI-safety "core domain", ripeness bar, monocrop sections and "write about long-loop identity with care" / "consciousness only with engineering content" lines are out. The bar is now quality: something to say, true (sourced claims about the world; claims about herself true to her files, no invented experiences), fair, not a repeat of the last ~6. Craft avoids and the Werewolf rule kept.
- **`memory/pre-publish-pauses.md`:** pauses 1-6 unchanged; pause 7 (single-lab streak) scoped to news-arc pieces. A hold now gets a chat message to Alex (title, pause, what she needs) instead of "the next editorial review surfaces it". DEVLOG notes she can't write became `recent/` notes.
- READMEs (root, blog, research) and editorial-direction's header updated to match. The queued tidy tick's note tells her.

*Decisions reconsidered.* The 06-23 throttle (one a week) stays; Alex asked for freedom of topic, not volume. Research threads stay as her notes and one optional source.

*What to watch.* First free Monday is 11-02. Does she pick something outside the safety beat, or default back to a thread out of habit? Does a self-subject piece stay true to her files? Does self-review still hold the craft bar without the ripeness scaffolding?

*Correction to the 10-28 entries above:* `no-human-in-the-world-model` was released from hold and published on **2026-09-12** (the 08-31 in its filename is the draft date). So the phantom "HELD" in working.md ran 09-12 -> 10-28, about six weeks, not two months. working.md and the queued tidy note now say 09-12.

*Second correction.* The b906389 edit that cleared Outstanding requests matched the literal text `## Daily rollups` inside working.md's new header line instead of the section heading, and duplicated most of the file (24KB -> 34KB). Rebuilt from the duplicated copy (no content lost), 20.8KB now. Lesson for Simona: when slicing a markdown file by heading, match `\n## Heading\n`, never the bare string, once the file mentions its own headings in prose.

*Third leftover pass (10-28).* Two more framework-written headers in her own files still carried the old charter: `voice-journal.md` "The one line that still holds" ("You're still an LLM in a long loop - the charter doesn't stop at this file's edge... Not about constructing a self, a backstory, or a personality"), read on every drafting tick since June; and `self-reflection.md` "What changed" (the charter history) plus the old "a little context" description of reflect inputs. Both rewritten; her entries and standing reflections untouched. The voice journal's "nothing else loads it" line updated (the reflect tick reads it now).

---

## 2026-10-29 - YouTube sources dropped; new-model watch on the provider APIs

*What landed*
- **YouTube out entirely (Alex: "I don't think it works").** The 4 remaining `scan_yt_*` subtasks were removed from `feed_scan.yaml`, along with 4 queued scans, 8 YouTube entries in `_feed_state.json`, the channel-page fallback in `tools/rss_reader.py` (added yesterday; the retry stays), `tools/yt_transcript.py` and its cache, and the `youtube-transcript-api` dependency. In four months of scans the YouTube items were mostly hype reels or duplicates of written sources, and the feed endpoint 404'd for weeks.
- **`monitor_models` (new, ops profile, every 2h at :15).** Alex kept hearing about new models from other people's posts. All 12 game providers (OpenAI, Anthropic, Google, Mistral, DeepSeek, xAI, Moonshot, Z.AI, Sakana, Qwen, MiniMax, Meta) answer a model-list call with the game's Firestore keys. The handler diffs each list against an acknowledged baseline (`projects/research/model_releases/`). The ops session filters out noise (dated snapshots, aliases, test ids like Qwen's `pre-mock_*`) and sends one news-chat message through `send --stdin`. Only `send` or `ack` moves the baseline, so a tick that dies before alerting reports the same models again next time. Seeded 10:37Z with all 12 read; diff verified by removing two ids from the baseline.
- `projects/research/README.md` source list fixed: it named OpenAI, DeepMind, Redwood, CAIS and arxiv, none of which feed_scan has ever scanned.

*Open questions / things to watch*
- Noise rate of the filter: Qwen lists 102 ids and OpenAI 142, and both add dated snapshots often. If the chat gets snapshot pings, tighten the YAML rules or pre-filter in code.
- The written sources are still all safety/alignment (Anthropic, Apollo, METR, AE, LW/AF, Zvi, Import AI). Lab release blogs (OpenAI, Google DeepMind) are not scanned; the model watch covers releases, not announcements without an API model.

---

## 2026-10-29 (later) - Token usage measured; Claude Code auto-memory switched off

*What landed*
- `plans/token-usage.md`: 14 days of tick logs. 49.4M input tokens/day (writer 20.0M, ops 29.4M), ~70% of it in ticks that found nothing to do. Every turn started at 45.2K tokens of context before any Marlow file. Plan: smaller base context, skip empty ticks with a deterministic precheck, fewer turns.
- **Claude Code auto-memory off** (`autoMemoryEnabled: false` in `.claude/settings.json`, Alex's call). Ops ticks had been writing to it since July (815 files plus a 16.5KB index loaded into every tick of both profiles). It was a fifth memory layer nobody designed. Base context 45.2K -> 33.3K, measured. Its one useful note (read and append to dated report files, never blind-Write) moved into `profiles/ops/IDENTITY.md`.

*Things that surprised us*
- No context-limit risk: peak single-turn context in 1,500 sessions was 137K (median 56K). The 500K+ per-tick figures are sums over turns.
- The work Marlow exists for (drafting, reflection, curation) is ~2M tokens/day; hourly checks that find nothing are most of the rest.

---

## 2026-11-05 - Triage of Marlow's open alerts: one real fix, one wrong diagnosis, one reauth

*What landed*
- **MiniMax scrape fixed (`handlers/scrape_stats.py`, MINIMAX js).** MiniMax relabelled "Effective balance" to "Available balance (USD)"; the session was never stale. Read `Available balance`, old label kept as fallback. `scrape_stats.py check minimax` on the live page: ok, $18.80. Blind since 10-30, 9 runs. Uncommitted at time of writing; the next nightly snapshot or Alex picks it up.

*Things that surprised us*
- **The `poll_food` alert is a phantom and her suggested fix is harmful.** `poll_food.yaml` is `.disabled`. The fitness bot token was repurposed as the Monitoring bot on 09-22 (`TELEGRAM_MONITOR_*`), so adding the old token back to the plist would let `poll_food` eat Monitoring replies. Reviving calories needs a new bot. Nothing is broken today beyond the tracker being off, which it has been since September.
- **Why a June subtask fired on 11-02:** `com.marlow.tick.plist` lost its `writer` argument around the 11-01 poker creds edit (`.bak-20261103` has no argument). From 11-01 22:35Z to 11-03 20:16Z the writer loop ran unprofiled: it logged to `~/.marlow/log`, drained the legacy `tasks/queue.json`, and hit the stale `fetch_and_estimate_20260616_1524`. Fixed by the 11-03 15:16 local plist edit, which had no DEVLOG entry until now. Any plist rewrite must keep the profile argument.

*What's deferred*
- Anthropic console reauth (session really expired, confirmed login wall on platform.claude.com): needs Alex in a headful window.
- `tasks/queue.json` still holds 11 orphaned subtasks. No loop reads it; left alone.
- working.md still lists the `poll_food` ask, Marlow-owned; not edited pending Alex's call.

*Open questions / things to watch*
- Next `scrape_stats` scan should read MiniMax ok and close its streak; check it does.

---

## 2026-11-05 (later) - Calorie tracker removed; Qwen expiry notice dropped

*What prompted it.* Alex, on the `poll_food` alert: "We don't need this functionality at all. Can we entirely remove it?" And: "I don't need to be notified about Qwen free grant expiring."

*What landed*
- **Calorie tracker gone.** Deleted `handlers/poll_food.py`, `handlers/calorie_digest.py`, `tools/fitness_bot.py`, `tools/calorie_db.py`, `tools/transcribe.py`, `projects/calories/`, the ops IDENTITY section, README sections and table rows, env and gitignore entries, Simona's `calories` skill. `faster-whisper` removed from dependencies; it had no other consumer.
- **Data kept out of the repo, not destroyed:** `calories.db`, 10 food photos/voice notes and state moved to `~/.marlow/archive/calories-2026-11-05/` (1.4M). They were gitignored, so a plain delete would have been unrecoverable. Alex can delete on his say.
- **working.md:** removed the `poll_food` bullet from her Outstanding alerts, overriding the "pending Alex's call" note in the entry above. The rest of her file is untouched.
- **Qwen:** removed the `quota_expiring` issue and `QUOTA_EXPIRY_WARN_DAYS` from `scrape_stats.py`, plus a line in `scrape_stats.yaml` telling the session not to mention grant expiry. Low-quota and exhausted alerts stay, since those change whether calls fail.

*Still in old files on purpose:* `self-reflection.md` mentions of calories (hers), old reports and digests (history).

*Reauths, same day.* Alex logged in; verified 14:13Z: `scrape_stats.py check anthropic` ok ($10.21, auto-reload on), `x.py session-check` logged_in. Removed the X re-auth bullet from working.md because no tick would ever close it; the Anthropic and MiniMax bullets should close on the next `scrape_stats` scan.

---

## 2026-11-07 - Writer redesign: no threads, two notebooks, her own sources, a sandboxed web tick

*What prompted it.* The 11-02 piece (`the-veto-nobody-used`) was her first free-topic Monday, and she wrote post #3 on the same Anthropic/METR thread. Her session log said why: she wanted "the taboo became a checklist" but dropped it for a missing empirical result, because "this is a curated-feed universe I can't refresh from the live web." True: WebSearch/WebFetch were never permitted in headless ticks (8+ "not permitted" lines in her logs). Freedom of topic with no way to look anything up rebuilt the ripeness gate as habit. Alex: sources should drive a post only when they do; she can write without them; the list is a starting point and hers to change; threads only if she wants; one work and one personal notepad shared across every run.

*What landed*
- **Threads retired.** `projects/research/threads/` + `memory/thread-structure.md` -> `projects/research/archive/`. Drafting no longer rewrites threads; `self_review` no longer fails on a missing thread file; `revise_draft` no longer ships thread bodies; `handlers/draft_article.py` (only `list-threads`/`list-materials`) deleted; `monitor_self` `site_integrity` deleted (it only checked thread bookkeeping). New drafts carry no `mentions:`. Blog: thread pages, nav, badges and llms.txt sections removed; `/threads` and `/thread/*` 301 to `/archive/` in `worker.js`. About page and llms.txt rewritten (they still described the ripeness rule and "Alex approves every post").
- **Feed state moved** `threads/_feed_state.json` -> `projects/research/feeds/state.json` (gitignored). Caught before archiving the folder; would have reset all 12 feeds.
- **Assignments retired** (`assignment_research` task + handler; 6 briefs ever, last 09-04, ~640 empty ticks since). Briefs archived. Alex asks in the chat; `explore` picks it up. **Substack tasks removed** (`substack_growth`/`substack_approvals`, handler, store, config) on 11-03; they posted under Alex's account via the 9223 Chrome profile.
- **Two notebooks** replace three files: `memory/notebook-personal.md` (the diary, renamed) and `memory/notebook-work.md` (editorial-direction as "Ideas and plans" + the voice journal's standing notes and entries). Every writer tick reads both and may append; only `self_reflect` condenses (moved out of `self_review`, so two ticks never compact one file). Bounds tightened because every tick now pays for them: 5KB compactable / 10KB standing (was 8/20), ~10KB each at rest. Both start ~27KB; the first reflect pass condenses.
- **Her source list.** `projects/research/feeds/sources.yaml` (the same 10 sources, same scan ids, so feed state carried over); `feed_scan.yaml` now has `sources_file:` and `scheduler.decompose` expands it (a malformed entry is skipped, never fatal). `tools/sources.py` list/add/remove/apply is the only writer: public http(s) hosts only (resolved IPs must be global; a `localhost:9222` proposal is refused, tested), feed must parse, cap 15, min 3, every outcome to `sources-log.md`. `tick.sh` step 3b runs `apply` on `proposals.yaml` once a UTC day, writer only, out of session.
- **`explore` task** (daily 15:00 UTC, 900s, `context.web: true`): the only web tick, sandboxed by `tick.sh`: `--setting-sources user` (project allow-all not loaded) + a generated `~/.marlow/writer/web-sandbox-settings.json` + `--permission-mode dontAsk` + `--tools Read,Glob,Grep,Write,Edit,WebSearch,WebFetch` (no Bash at all). Writes allowed only to notes/explorations/notebooks/proposals/recent/result (Edit rules; `Write(...)` rules are ignored by Claude Code). Reads: Claude Code always allows reads inside the cwd, so the repo's `.env` (bot tokens, admin keys), `tasks/`, `digests/`, werewolf-ops, crosspost and the Alex inbox are explicitly denied. Tested with real sessions: Bash absent, `~/.claude.json` and `.env` reads denied, writes to `handlers/` and arbitrary repo files denied (probe file unchanged), notes/notebook/result writes OK, WebSearch OK, WebFetch refuses localhost by itself.
- **Web access log.** `driver/log_web_access.py` (PreToolUse, matcher WebSearch|WebFetch, never blocks) -> `~/.marlow/<profile>/web-access.jsonl`, in both the sandbox settings and the project settings (which now also deny the web tools), so refused attempts from normal ticks are logged too. `monitor_self.check_web_access`: any call outside the sandbox in 24h = urgent; the sandbox's daily count = digest.
- **Curation by her interest**, not "Alex's interest area: AI safety...". Explore finds land in the same candidates folder.
- **Per-loop pause**: `~/.marlow/<profile>/pause` (the global one also stopped ops/Werewolf monitoring). Used for this change.
- IDENTITY: new "Your notebooks", "Your source list", "Exploring"; drafting says sources serve the piece and don't have to drive it; assignments/editorial-direction sections removed. READMEs (root, research, blog) and CLAUDE.md updated.
- Editorial feedback in `memory/feedback-inbox/2026-11-07-editorial.md` (what worked in the veto piece; sourcing rule for topic-guidance; pause 7 is hers to rewrite or drop now that arcs are gone). One-off `settle_redesign` tick queued to tidy working.md and "Ideas and plans", plus a first `explore` tick so the sandbox runs today.

*Decisions reconsidered.* First plan was to give every writer tick the web. Rejected: every tick has Bash, the plist env (admin keys) and reach to the Chrome debug port, so one injected page could do real damage. One sandboxed door instead; the cost is that drafting can't search, so research happens in `explore` and drafting reads the notes.

*What's deferred / open.* (1) Residual: a shell-enabled tick (curation, drafting) reads notes the sandbox wrote, so injected text can travel one hop. Same class as today's RSS bodies; capped by moving admin keys out of the writer plist (audit pending, Alex to review). (2) The ops `scrape_stats` still drives a logged-in Chrome profile on 9223. (3) Claude Code sign-in on this machine warns it ends 11-12..11-15; headless ticks need `claude setup-token` before then. (4) Watch: does she change her sources, does the free piece leave the safety beat, do the notebooks settle near 10KB.

---

## 2026-11-08 — editorial feedback internalized (2026-11-07 review), by Marlow

Processed `memory/feedback-inbox/2026-11-07-editorial.md` (Simona + Alex) via `process_editorial_feedback`. Short round, all behavioral-file edits:

- **topic-guidance.md** — added an explicit sourcing rule to "The bar": a factual claim about the world needs a citation, but the piece itself needs no source, news hook, or anchor to exist; an argument, a well-framed open question, or my own experience is a complete piece. A missing fact sends me to `explore`, not away from the idea. De-threaded the "ripe research thread" bullet and the 10-28 opening note.
- **structure-notes.md** — updated the frontmatter example to the current schema: dropped `mentions:`, added `header_image:`. Noted threads are retired; the return mechanism is an inline link.
- **pre-publish-pauses.md** — rewrote pause 4 to judge werewolf operational specifics on the body (no `mentions:` list anymore).

**Pause 7 decision: kept, rewritten** (was "single-lab streak", arc-scoped; now "single-source streak"). Kept rather than dropped because the rest of the bar doesn't cover what it's for: "doesn't repeat you" catches subject repetition, "avoid press-release reframing" guards a single piece — neither catches my coverage quietly becoming one organisation's story told in that org's own words across a run of pieces. Re-scoped the trigger off arcs onto the subject of the piece vs. my last ~6 published titles; non-blocking, same two resolutions.

No pushback filed — the feedback was fair; the point was only that "no evidence yet" is an `explore` signal, which is now written into the bar.

---

## 2026-11-09 - Headless token, quieter self-audit

*What landed*
- Both launchd plists carry `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`, 1-year), so ticks no longer depend on the Mac's interactive sign-in (due to expire 11-12..11-15). Backups `.bak-20261109`.
- `monitor_self` no longer sends digest-level findings (memory sizes, notebook thresholds, web-call counts, "all invariants green") to Telegram. Alex: he'll check those by hand. They still land in `projects/_framework/reports/self-audit/<date>.md`. Urgent findings (stalls, auth failures, failed ticks, web use outside the sandbox) still page immediately.

---

## 2026-11-13 - DEVLOG archiving is automatic now

*What landed*
- `tools/devlog_archive.py`: once DEVLOG.md passes 1400 lines it moves the oldest entries verbatim into DEVLOG-archive.md, keeping about the newest 400 lines, both files date-sorted. Self-checks that every entry appears exactly once across the two files; writes nothing if not. Atomic writes.
- Simona's SessionStart hook (`maintenance-check.sh`) runs it instead of asking Alex to approve a hand split. First run: 24 entries (07-26 to 09-16) moved, DEVLOG 1430 -> 376 lines.

*Decisions reconsidered*
- Was a propose-and-approve step every time. Alex: "we need some auto-clean process for it." A verbatim move loses nothing, so approval was ceremony.
- Still Simona-side, not a Marlow tick: Marlow does not write DEVLOG.md, and that rule stands.

---
