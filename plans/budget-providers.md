# Budget Providers

What is wired to read each provider's remaining balance, and how. This doc is
the truth about the mechanism; `.env` and the plist keep the secrets.

The `tools/budget/` plugin set this doc originally planned was never built, and
should not be: the split that actually matters is not per-provider classes but
`monitor_keys` (has a balance API) vs `scrape_stats` (does not), with reporting
unified afterwards in `driver/budget_state.py`. The directory is empty; the
handlers are the implementation.

## Coverage

All 11 live. Two mechanisms only: a real balance API (`monitor_keys`) or a
logged-in console scrape (`scrape_stats`). Tier 2 — balance derived from a cost
API minus a console baseline — is DORMANT and should stay that way unless a
provider offers neither of the other two: it fails quiet and wrong, because a
top-up is invisible to a cost API. It produced two confident false CRITICALs on
an OpenAI key that held $20 (2026-08-22, 08-24).

| Provider          | Method                        | Metric                | Status |
| ----------------- | ----------------------------- | --------------------- | ------ |
| **DeepSeek**      | API `/user/balance`           | prepaid balance       | live   |
| **Moonshot**      | API `/v1/users/me/balance`    | prepaid balance       | live   |
| **xAI / Grok**    | API (management key)          | prepaid balance       | live   |
| **OpenAI**        | console scrape                | prepaid balance       | live   |
| **Anthropic**     | console scrape                | prepaid balance       | live   |
| **Google Gemini** | console scrape (payments iframe) | prepaid balance    | live   |
| **GLM / z.ai**    | console scrape                | cash + credits        | live   |
| **Sakana Fugu**   | console scrape                | prepaid balance       | live   |
| **MiniMax**       | console scrape                | prepaid balance       | live   |
| **Mistral**       | console scrape                | spend vs. $30 cap     | live   |
| **Qwen**          | console scrape                | month spend, uncapped | live   |

Reporting is unified in `driver/budget_state.py`: `show` for a terminal, `digest`
for the one plain-text block `compose_daily_digest` appends at send time. The
monitors themselves post ISSUES ONLY — they must not write their own roll-call.
Two partial roll-calls from two tasks on different schedules is how the digest
ended up naming three balances twice, five once and two not at all (2026-08-27).

## Per-provider notes

### Anthropic
- No balance endpoint exists; `console.anthropic.com/settings/billing` is the
  only source. The number is pinned by the label that TRAILS it ("$16.08 /
  Remaining balance") because "Credit balance" is a section heading with a
  two-sentence blurb between it and the figure.
- Do NOT scan for the largest $: the page also prints the monthly spend limit,
  month-to-date spend and every historical credit grant.

### OpenAI
- `platform.openai.com/settings/organization/billing` (it redirects to
  `/overview`); "API credit balance" is the depleting prepaid total.
- The org admin key gives cost/usage, never a balance — that is why this is a
  scrape and not an API call.
- Headless Chrome's default UA gets a Cloudflare interstitial here and an EMPTY
  body, which reads downstream as `parse_failed: no credit balance found`. The
  scrape profile masks its UA to plain Chrome; see start-chrome-persistent.sh.

### DeepSeek
- `https://api.deepseek.com/user/balance` with `Authorization: Bearer <key>`.
- Returns `{"is_available": bool, "balance_infos": [{"currency": "USD", "total_balance": "...", "granted_balance": "...", "topped_up_balance": "..."}]}`.
- Cleanest of the bunch.

### Google Gemini
- Prepay since 2026-08-27; the metric is a depleting credit balance, not spend.
- The balance is on `aistudio.google.com/billing` under "Payments" but is NOT in
  that page's DOM: AI Studio embeds a `payments.google.com` widget in an iframe.
  Same SITE, different ORIGIN — so the parent document cannot read it AND it
  never appears as its own CDP target. Read via the browser CLI's `--frame`,
  which attaches an isolated world to the frame.
- Month-to-date cost still comes off the host page ("Total cost") as context.
- Not worth chasing: Cloud console's own payment page renders the same figure in
  a cross-origin `payments.google.com` iframe, and `payments.google.com` at top
  level demands an interactive identity re-verification.

### Qwen
- Two different pages, and which one leads depends on the data, not the date.
  `home.qwencloud.com/benefits` has the per-model free-token grants;
  `home.qwencloud.com/billing/overview` has month spend and amount due.
- The one-time 1M-token-per-model grant expired into pay-as-you-go around
  2026-08-25 with auto-stop off, so dollars are the headline now and
  percent-of-grant is a sub-note. The handler switches on `remaining_pct <= 0`.
- Billing figures render as label / bare "$" / number on separate lines, so the
  $ and the digits cannot be matched as one token.

### Grok (x.ai), Moonshot, Mistral, GLM/z.ai, Sakana, MiniMax
- All live; see the per-provider extractor comments in `handlers/scrape_stats.py`
  (or `monitor_keys.py` for Grok and Moonshot), which carry the current recipe
  and the history of every console redesign that broke it.

## Update protocol

When a provider changes mechanism or metric, update the table above, update the
extractor's comment block in the handler, and note the arc in `DEVLOG.md`.
