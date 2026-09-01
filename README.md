# PRINT FLASH — Streamlit Web App

A warm, coral/orange/magenta-themed storefront for a printing business:
a live cost calculator, a Gemini-powered AI design assistant, a cart, and
a checkout flow that sends the finished order straight to your WhatsApp.

This guide assumes **zero local setup** — no VS Code, no terminal on your
own computer. Everything happens in the browser via GitHub and Streamlit
Community Cloud (both free).

---

## 1. What's in this project

```
printflash/
├── app.py                          # the whole app (UI + pricing logic + AI + checkout)
├── requirements.txt                # Python packages Streamlit Cloud will install
└── .streamlit/
    └── secrets.toml.example        # template showing what secret to add (not a real key)
```

---

## 2. Before you deploy — fill in your real details

Open `app.py` in GitHub's web editor (steps below show you how) and update
these lines near the top (search for `BRAND_NAME`):

| Variable | What to put |
|---|---|
| `WHATSAPP_LOCAL_NUMBER` | Already set to `01006328846` — change if needed |
| `INSTAPAY_IPA` | Your real InstaPay ID / mobile number (currently a placeholder) |
| `VODAFONE_CASH_NUMBER` | Your real Vodafone Cash number (currently a placeholder) |
| `FLASH_DISCOUNT_PERCENT` | Change or set to `0` to turn off the flash offer |
| `BASE_PRICES` / multipliers | Replace the demo EGP prices with your real cost sheet |

You can also do this editing **after** deployment directly on GitHub — every
save automatically redeploys the live app within ~1 minute.

---

## 3. Get a free Gemini API key (for the AI Assistant tab)

1. Go to <https://aistudio.google.com/app/apikey>.
2. Sign in with a Google account.
3. Click **Create API key** → copy it. It's free for moderate usage.
4. Keep this tab open — you'll paste the key into Streamlit's Secrets in Step 6.

---

## 4. Put the project on GitHub (no local Git needed)

1. Go to <https://github.com> and sign in (or create a free account).
2. Click the **+** icon (top right) → **New repository**.
3. Name it `printflash`, set it to **Public** (required for the free
   Streamlit Community Cloud tier), then click **Create repository**.
4. On the new repo page, click **Add file → Upload files**.
5. Drag in `app.py` and `requirements.txt` from this delivery.
6. For the secrets template: click **Add file → Create new file**, name it
   `.streamlit/secrets.toml.example`, paste in the example content, and commit.
   (Typing `.streamlit/secrets.toml.example` as the filename automatically
   creates the `.streamlit` folder.)
7. Click **Commit changes** at the bottom of the page.

Your code is now live on GitHub — entirely from the browser.

---

## 5. Deploy on Streamlit Community Cloud (free, 24/7)

1. Go to <https://share.streamlit.io> and sign in with your **GitHub** account.
2. Click **Create app** → **From an existing repo**.
3. Choose:
   - **Repository:** `your-username/printflash`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**. Streamlit installs `requirements.txt` and starts the app —
   this takes 1–3 minutes the first time.

Your app is now running at a public URL like:
`https://your-username-printflash.streamlit.app`

It stays online 24/7 on Streamlit's free tier (it may briefly "sleep" after
long inactivity and wake up automatically on the next visit — normal for the
free tier).

---

## 6. Add your Gemini API key as a Secret

1. On your app's page in Streamlit Community Cloud, click the **⋮ menu** →
   **Settings** → **Secrets**.
2. Paste in:
   ```toml
   GEMINI_API_KEY = "your-real-key-from-step-3"
   ```
3. Click **Save**. The app restarts automatically and the AI Assistant tab
   goes live — no key ever needs to be visible in your code or GitHub repo.

---

## 7. Making future changes (still no IDE needed)

- Edit any file directly on GitHub (open the file → pencil icon → edit → commit).
- Streamlit Community Cloud watches your `main` branch and **redeploys
  automatically** within about a minute of every commit.
- To check logs or force a reboot, use the **Manage app** panel at the
  bottom-right of your running app.

---

## 8. Customizing pricing later

All pricing logic lives in clearly commented sections of `app.py`:

- `BASE_PRICES` — starting price per unit for Cards, Flyers, Brochures, etc.
- `SIZE_MULTIPLIER`, `GSM_MULTIPLIER`, `LAMINATION_ADDON`, `FOLDING_ADDON` —
  multipliers/add-ons applied to the base price.
- `COVER_ADDON`, `BINDING_ADDON` — notebook-specific pricing.
- `QUANTITY_TIERS` — bulk-quantity discount brackets.
- `FLASH_DISCOUNT_PERCENT` — the storewide promo percentage.

Change the numbers, commit, and the live app updates automatically.

---

## 9. Notes & limitations to be aware of

- **Cart persistence:** the cart lives in each visitor's browser session only
  (Streamlit `session_state`). It resets if they refresh in a new tab or the
  app restarts — fine for a quote/order tool, not a full e-commerce database.
- **Payments:** this app does not process payments — it displays your
  InstaPay/Vodafone Cash details and QR codes, and the customer pays manually
  then sends proof over WhatsApp, matching how you described your workflow.
- **AI Assistant:** uses your own Gemini API key and Google's free tier; very
  high traffic could hit Google's rate limits, at which point you'd upgrade
  your Gemini plan.
- **Pricing numbers in the code are placeholders** — please replace them with
  your real, validated cost sheet before taking real orders.
