# Budget Provider Rollout

Per-provider plan for the budget-monitoring plugin set under `tools/budget/`. Each provider plugin implements:

```python
def get_balance() -> dict:
    return {
        "provider": str,        # e.g. "anthropic"
        "balance_usd": float,   # current credit / remaining budget
        "threshold": float,     # alert threshold from config
        "last_checked": str,    # ISO timestamp
        "source": str,          # "api" | "browser" | "manual"
        "raw": dict,            # provider-specific extras (per-model spend, etc.)
    }
```

Status legend: `not started` → `info gathered` → `built` → `verified` → `live`.

## Coverage

| Provider           | Method (planned) | Status        | What's needed from Alex                              |
| ------------------ | ---------------- | ------------- | ---------------------------------------------------- |
| **Anthropic**      | API (Admin key)  | not started   | Org admin API key, latest Admin API docs link        |
| **OpenAI**         | API (Admin key)  | not started   | Org admin API key, current usage endpoint docs       |
| **DeepSeek**       | API (`/user/balance`) | not started | API key                                              |
| **Google Gemini**  | API or browser   | not started   | GCP service account JSON OR AI Studio account login  |
| **Grok (x.ai)**    | TBD              | not started   | API key, x.ai billing/usage doc link                 |
| **Moonshot**       | TBD              | not started   | API key, Moonshot billing API doc link               |
| **Mistral**        | TBD              | not started   | API key, Mistral billing API doc link                |
| **z.ai**           | TBD              | not started   | API key, z.ai billing API doc link (newly added)     |

## Build order

Start with the providers we're most confident have clean APIs, then expand:

1. **DeepSeek** — `/user/balance` endpoint is well-known and dead simple. Good first build to nail the plugin shape.
2. **Anthropic** — Admin API for usage; compute remaining from configured cap.
3. **OpenAI** — Admin API for usage; same pattern as Anthropic.
4. **Google Gemini** — likely browser fallback unless GCP service account is acceptable.
5. **Grok / Moonshot / Mistral / z.ai** — verify each provider's current docs, build native if available, browser otherwise.

## Per-provider notes

### Anthropic
- Admin API key is separate from regular API keys. Created in Console → Settings → Admin Keys (org admin permission required).
- Endpoints around `/v1/organizations/usage_report/messages` for token/spend stats over a window.
- "Remaining balance" isn't a direct endpoint — compute from `monthly_cap - month_to_date_spend`.

### OpenAI
- Org admin API key required (separate from regular keys).
- Public per-key usage API was deprecated for individuals around 2024.
- Org-level endpoints under `/v1/organization/usage/...` return token + dollar usage.
- For prepaid credit balance specifically, may need to scrape the dashboard.

### DeepSeek
- `https://api.deepseek.com/user/balance` with `Authorization: Bearer <key>`.
- Returns `{"is_available": bool, "balance_infos": [{"currency": "USD", "total_balance": "...", "granted_balance": "...", "topped_up_balance": "..."}]}`.
- Cleanest of the bunch.

### Google Gemini
- Two paths: Vertex AI (GCP project, service account, Cloud Billing API) or AI Studio (Google account).
- Vertex AI billing API is doable but heavy: needs `roles/billing.viewer` on the billing account, queries via Cloud Billing API.
- Browser fallback: log into AI Studio with the persistent Chrome profile, scrape the usage page.

### Grok (x.ai), Moonshot, Mistral, z.ai
- Need to verify current docs before committing to API vs browser. Alex to provide doc links.
- Newer providers tend to have less-mature billing APIs; expect browser fallbacks.

## Plugin shape (interface only)

```python
# tools/budget/_base.py
from abc import ABC, abstractmethod

class BudgetProvider(ABC):
    name: str
    threshold_usd: float

    @abstractmethod
    def get_balance(self) -> dict:
        """Return balance dict per the schema in this doc."""
```

Each provider file under `tools/budget/<name>.py` implements one `BudgetProvider` subclass. The `check_provider_balance` handler dispatches by name.

## Update protocol

When a provider is added or its method changes, update the table above and bump the status. Alex's `.env` keeps secrets; this doc keeps the truth about what's wired.
