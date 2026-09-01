"""
PRINT FLASH — Streamlit web app
================================
A production-ready single-file Streamlit app for a printing business.

Features
--------
1. Warm-themed UI (coral / orange / magenta gradients, geometric accents).
2. Dynamic, real-time cost calculator for 8 printing product types,
   with a "Flash Offer" percentage discount.
3. A Gemini-powered AI design assistant chat embedded in the sidebar / tab.
4. An itemized order cart -> summary -> payment method (InstaPay / Vodafone
   Cash, both with auto-generated QR codes) -> "Send to WhatsApp" button
   that builds a pre-filled WhatsApp message with every order detail.

Run locally:
    streamlit run app.py

Deploy free & 24/7:
    See README.md for the full GitHub + Streamlit Community Cloud guide.
"""

import io
import urllib.parse
from dataclasses import dataclass, field

import streamlit as st

# QR codes for the payment section are generated on the fly (no external
# images needed) using the `qrcode` package. See requirements.txt.
import qrcode

# ---------------------------------------------------------------------------
# 0. PAGE CONFIG  (must be the first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PRINT FLASH | Premium Printing, Special Offers",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 1. BRAND CONFIG — EDIT THESE VALUES FOR YOUR BUSINESS
# ---------------------------------------------------------------------------
BRAND_NAME = "PRINT FLASH"
TAGLINE = "PRINT MORE, SAVE MORE — Premium printing with special offers for every project"

# Your WhatsApp number in local format (no spaces, no +). Country code is
# added automatically below (Egypt = 20).
WHATSAPP_LOCAL_NUMBER = "01006328846"
COUNTRY_CODE = "20"

# --- Payment details — REPLACE THESE PLACEHOLDERS WITH YOUR REAL DETAILS ---
INSTAPAY_IPA = "printflash@instapay"        # TODO: replace with your real InstaPay IPA / mobile
VODAFONE_CASH_NUMBER = "010XXXXXXXX"        # TODO: replace with your real Vodafone Cash number

# Flash discount applied storewide (set to 0 to disable)
FLASH_DISCOUNT_PERCENT = 30

# ---------------------------------------------------------------------------
# 2. THEME / CSS — warm coral, orange, magenta gradient identity
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
:root{
    --coral:#FF3E6C;
    --orange:#FF8C42;
    --amber:#FFB627;
    --charcoal:#2D2A26;
    --card-bg:#FFFFFF;
    --page-bg:#FFF7F2;
}

/* Overall page background */
.stApp{
    background: var(--page-bg);
}

/* Hide default Streamlit chrome for a cleaner storefront feel */
#MainMenu, footer {visibility: hidden;}

/* ---------- Hero banner ---------- */
.pf-hero{
    background: linear-gradient(120deg, var(--coral) 0%, var(--orange) 55%, var(--amber) 100%);
    border-radius: 22px;
    padding: 2.6rem 2.2rem;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.6rem;
    box-shadow: 0 10px 30px rgba(255,62,108,0.25);
}
.pf-hero::before{
    content:"";
    position:absolute;
    width:260px;height:260px;
    background: rgba(255,255,255,0.12);
    transform: rotate(45deg);
    top:-120px; right:-80px;
    border-radius: 24px;
}
.pf-hero::after{
    content:"";
    position:absolute;
    width:160px;height:160px;
    background: rgba(255,255,255,0.10);
    transform: rotate(20deg);
    bottom:-70px; left:-40px;
    border-radius: 20px;
}
.pf-hero h1{
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: 0.5px;
}
.pf-hero p{
    font-size: 1.05rem;
    margin-top: 0.4rem;
    opacity: 0.95;
    max-width: 620px;
}
.pf-badge{
    display:inline-block;
    background: var(--charcoal);
    color: var(--amber);
    font-weight: 800;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.85rem;
    margin-top: 0.9rem;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

/* ---------- Cards ---------- */
.pf-card{
    background: var(--card-bg);
    border-radius: 18px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 6px 18px rgba(45,42,38,0.08);
    border: 1px solid rgba(255,140,66,0.15);
    margin-bottom: 1rem;
}
.pf-card h3{
    color: var(--charcoal);
    margin-top: 0;
}
.pf-price{
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--coral);
}
.pf-price-sub{
    color: #8a8a8a;
    text-decoration: line-through;
    font-size: 1.05rem;
    margin-left: 0.5rem;
}

/* Section headers */
.pf-section-title{
    color: var(--charcoal);
    font-weight: 800;
    font-size: 1.4rem;
    margin: 1.6rem 0 0.6rem 0;
    border-left: 6px solid var(--coral);
    padding-left: 0.6rem;
}

/* Buttons */
.stButton>button{
    background: linear-gradient(90deg, var(--coral), var(--orange));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.1rem;
    font-weight: 700;
    box-shadow: 0 4px 14px rgba(255,62,108,0.3);
}
.stButton>button:hover{
    filter: brightness(1.05);
    color: white;
}

/* WhatsApp button styled distinctly (green, since it's brand-recognized) */
.pf-whatsapp-btn a{
    display:inline-block;
    background:#25D366;
    color:white !important;
    font-weight:800;
    text-decoration:none;
    padding:0.75rem 1.4rem;
    border-radius:12px;
    box-shadow: 0 4px 14px rgba(37,211,102,0.35);
}

/* Chat bubbles for AI assistant */
.pf-chat-user{
    background: var(--amber);
    color: var(--charcoal);
    padding: 0.6rem 0.9rem;
    border-radius: 14px 14px 2px 14px;
    margin: 0.3rem 0;
    max-width: 85%;
    margin-left: auto;
}
.pf-chat-ai{
    background: #FFF0E8;
    color: var(--charcoal);
    padding: 0.6rem 0.9rem;
    border-radius: 14px 14px 14px 2px;
    margin: 0.3rem 0;
    max-width: 85%;
    border: 1px solid rgba(255,140,66,0.25);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 3. PRODUCT / PRICING CONFIG
# ---------------------------------------------------------------------------
# All prices are in EGP and are DEMO / STARTING-POINT values only.
# Replace `base_price` and the multipliers with your real cost structure.

SIZE_MULTIPLIER = {"A6": 0.6, "A5": 0.8, "A4": 1.0, "A3": 1.6, "Custom": 1.3}
GSM_MULTIPLIER = {80: 0.9, 100: 1.0, 120: 1.1, 150: 1.25, 200: 1.45, 250: 1.65, 300: 1.9, 350: 2.1}
LAMINATION_ADDON = {"None": 0.0, "Matte": 0.35, "Glossy": 0.35, "Soft-touch": 0.5}
FOLDING_ADDON = {"None": 0.0, "Half-fold": 0.2, "Tri-fold": 0.35, "Z-fold": 0.35, "Gate-fold": 0.5}
COVER_ADDON = {"Soft Cover": 0.0, "Hard Cover": 3.5}  # per unit, notebooks
BINDING_ADDON = {"Staple": 0.0, "Spiral": 1.5, "Perfect Bound": 2.5}

# Quantity-based bulk discount tiers (applied BEFORE the flash offer)
QUANTITY_TIERS = [
    (1, 49, 0.0),
    (50, 99, 0.05),
    (100, 249, 0.10),
    (250, 499, 0.15),
    (500, 999, 0.20),
    (1000, float("inf"), 0.25),
]


def quantity_discount(qty: int) -> float:
    for low, high, disc in QUANTITY_TIERS:
        if low <= qty <= high:
            return disc
    return 0.0


@dataclass
class LineItem:
    product: str
    specs: dict
    unit_price: float
    quantity: int
    subtotal_before_discount: float
    bulk_discount_pct: float
    flash_discount_pct: float
    total: float

    def spec_string(self) -> str:
        return ", ".join(f"{k}: {v}" for k, v in self.specs.items())


def price_standard_item(
    base_price: float,
    quantity: int,
    size: str = "A4",
    gsm: int = 150,
    sides: str = "Single-sided",
    lamination: str = "None",
    folding: str = "None",
) -> LineItem:
    """Generic pricing engine for Cards / Flyers / Brochures / Posters /
    Envelopes / Stickers (anything priced per-unit with size + paper specs)."""
    unit_price = base_price
    unit_price *= SIZE_MULTIPLIER.get(size, 1.0)
    unit_price *= GSM_MULTIPLIER.get(gsm, 1.0)
    if sides == "Double-sided":
        unit_price *= 1.35
    unit_price += LAMINATION_ADDON.get(lamination, 0.0)
    unit_price += FOLDING_ADDON.get(folding, 0.0)

    subtotal = unit_price * quantity
    bulk_disc = quantity_discount(quantity)
    flash_disc = FLASH_DISCOUNT_PERCENT / 100.0
    total = subtotal * (1 - bulk_disc) * (1 - flash_disc)

    specs = {
        "Size": size, "Paper (GSM)": gsm, "Sides": sides,
        "Lamination": lamination, "Folding": folding,
    }
    return LineItem("", specs, unit_price, quantity, subtotal, bulk_disc, flash_disc, total)


def price_notebook(
    quantity: int,
    size: str,
    page_count: int,
    cover: str,
    binding: str,
) -> LineItem:
    base_per_page = 0.35  # EGP per printed page (demo value)
    unit_price = base_per_page * page_count
    unit_price *= SIZE_MULTIPLIER.get(size, 1.0)
    unit_price += COVER_ADDON.get(cover, 0.0)
    unit_price += BINDING_ADDON.get(binding, 0.0)

    subtotal = unit_price * quantity
    bulk_disc = quantity_discount(quantity)
    flash_disc = FLASH_DISCOUNT_PERCENT / 100.0
    total = subtotal * (1 - bulk_disc) * (1 - flash_disc)

    specs = {"Size": size, "Pages": page_count, "Cover": cover, "Binding": binding}
    return LineItem("", specs, unit_price, quantity, subtotal, bulk_disc, flash_disc, total)


def price_menu(
    quantity: int,
    pages: int,
    material: str,
    laminated: bool,
) -> LineItem:
    base_per_page = 2.5  # menus use heavier stock, priced higher per page
    material_mult = {"Standard Card": 1.0, "Premium Card": 1.3, "PVC / Plastic": 1.9}
    unit_price = base_per_page * pages * material_mult.get(material, 1.0)
    if laminated:
        unit_price += 1.2

    subtotal = unit_price * quantity
    bulk_disc = quantity_discount(quantity)
    flash_disc = FLASH_DISCOUNT_PERCENT / 100.0
    total = subtotal * (1 - bulk_disc) * (1 - flash_disc)

    specs = {"Pages": pages, "Material": material, "Laminated": "Yes" if laminated else "No"}
    return LineItem("", specs, unit_price, quantity, subtotal, bulk_disc, flash_disc, total)


BASE_PRICES = {
    "Business Cards": 0.9,
    "Flyers": 1.1,
    "Brochures": 2.2,
    "Posters": 6.5,
    "Envelopes": 1.4,
    "Stickers": 1.6,
}

# ---------------------------------------------------------------------------
# 4. SESSION STATE INIT
# ---------------------------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart: list[LineItem] = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of (role, text)

# ---------------------------------------------------------------------------
# 5. HERO SECTION
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="pf-hero">
        <h1>🖨️ {BRAND_NAME}</h1>
        <p>{TAGLINE}</p>
        <span class="pf-badge">🔥 {FLASH_DISCOUNT_PERCENT}% FLASH OFFER — Applied automatically at checkout</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 6. NAVIGATION TABS
# ---------------------------------------------------------------------------
tab_calc, tab_ai, tab_cart, tab_checkout = st.tabs(
    ["💰 Price Calculator", "🤖 AI Design Assistant", "🛒 Cart", "✅ Checkout"]
)

# ===========================================================================
# TAB 1 — PRICE CALCULATOR
# ===========================================================================
with tab_calc:
    st.markdown('<div class="pf-section-title">Build Your Order</div>', unsafe_allow_html=True)

    product_type = st.selectbox(
        "Choose a product",
        ["Business Cards", "Flyers", "Brochures", "Posters", "Envelopes",
         "Stickers", "Notebooks / Blocknotes", "Menus", "Custom Order"],
    )

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown('<div class="pf-card">', unsafe_allow_html=True)

        if product_type in BASE_PRICES:
            # --- generic per-unit product form ---
            qty = st.number_input("Quantity", min_value=1, max_value=100000, value=100, step=10)
            size = st.selectbox("Size", list(SIZE_MULTIPLIER.keys()))
            gsm = st.selectbox("Paper Weight (GSM)", list(GSM_MULTIPLIER.keys()), index=3)
            sides = st.radio("Sides", ["Single-sided", "Double-sided"], horizontal=True)
            lamination = st.selectbox("Lamination", list(LAMINATION_ADDON.keys()))
            folding = "None"
            if product_type in ("Brochures", "Flyers"):
                folding = st.selectbox("Folding", list(FOLDING_ADDON.keys()))

            line = price_standard_item(
                BASE_PRICES[product_type], int(qty), size, int(gsm), sides, lamination, folding
            )
            line.product = product_type

        elif product_type == "Notebooks / Blocknotes":
            qty = st.number_input("Quantity", min_value=1, max_value=100000, value=50, step=5)
            size = st.selectbox("Size", ["A5", "A4"])
            page_count = st.slider("Page Count", 20, 300, 80, step=10)
            cover = st.radio("Cover Type", list(COVER_ADDON.keys()), horizontal=True)
            binding = st.selectbox("Binding", list(BINDING_ADDON.keys()))

            line = price_notebook(int(qty), size, int(page_count), cover, binding)
            line.product = product_type

        elif product_type == "Menus":
            qty = st.number_input("Quantity", min_value=1, max_value=100000, value=30, step=5)
            pages = st.slider("Pages", 1, 20, 4)
            material = st.selectbox("Material", ["Standard Card", "Premium Card", "PVC / Plastic"])
            laminated = st.checkbox("Laminated", value=True)

            line = price_menu(int(qty), int(pages), material, laminated)
            line.product = product_type

        else:  # Custom Order
            st.info(
                "Custom books, special packaging, or bespoke branding? "
                "Describe it here and/or chat with the AI Design Assistant tab "
                "to refine the idea before you request a quote."
            )
            qty = st.number_input("Approximate Quantity", min_value=1, value=1)
            description = st.text_area(
                "Describe your custom order",
                placeholder="e.g. 20 hardcover A5 personalized photo books, "
                            "80 pages each, gold foil name on cover...",
            )
            est_unit_price = st.number_input(
                "Estimated unit price (EGP) — you can leave as 0 and confirm via chat",
                min_value=0.0, value=0.0, step=1.0,
            )
            subtotal = est_unit_price * qty
            bulk_disc = quantity_discount(int(qty))
            flash_disc = FLASH_DISCOUNT_PERCENT / 100.0
            total = subtotal * (1 - bulk_disc) * (1 - flash_disc)
            line = LineItem(
                "Custom Order", {"Description": description or "See chat / notes"},
                est_unit_price, int(qty), subtotal, bulk_disc, flash_disc, total,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="pf-card">', unsafe_allow_html=True)
        st.markdown("### Live Price")
        st.markdown(
            f'<span class="pf-price">{line.total:,.2f} EGP</span> '
            f'<span class="pf-price-sub">{line.subtotal_before_discount:,.2f} EGP</span>',
            unsafe_allow_html=True,
        )
        st.write(f"**Unit price:** {line.unit_price:,.2f} EGP")
        st.write(f"**Bulk discount:** {line.bulk_discount_pct*100:.0f}%")
        st.write(f"**Flash offer:** {line.flash_discount_pct*100:.0f}%")
        st.caption(line.spec_string())

        if st.button("➕ Add to Cart", use_container_width=True):
            st.session_state.cart.append(line)
            st.success(f"Added {line.product} to cart!")

        st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================================
# TAB 2 — AI DESIGN ASSISTANT (Gemini)
# ===========================================================================
with tab_ai:
    st.markdown('<div class="pf-section-title">Chat with the PRINT FLASH Design Assistant</div>', unsafe_allow_html=True)
    st.caption(
        "Brainstorm custom book ideas, branding concepts, or get help specifying "
        "your order. Powered by Google Gemini."
    )

    # API key: prefer Streamlit secrets (for the deployed app), fall back to
    # a manual sidebar input for local testing.
    gemini_api_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
    if not gemini_api_key:
        gemini_api_key = st.sidebar.text_input(
            "Gemini API Key (only needed if not set in Secrets)",
            type="password",
            help="Get a free key at https://aistudio.google.com/app/apikey",
        )

    if not gemini_api_key:
        st.warning(
            "No Gemini API key found. Add `GEMINI_API_KEY` in your Streamlit "
            "Community Cloud app **Secrets**, or paste one in the sidebar to test locally."
        )
    else:
        try:
            import google.generativeai as genai

            genai.configure(api_key=gemini_api_key)

            SYSTEM_PROMPT = (
                f"You are the friendly, creative AI design assistant for {BRAND_NAME}, "
                "a printing business. Help customers brainstorm custom books, branding "
                "materials, notebooks, menus, flyers, and personalized gifts. Ask clarifying "
                "questions about size, quantity, paper type, and style. Keep answers concise, "
                "practical, and enthusiastic. When the customer seems ready, summarize the "
                "recommended specs so they can enter them into the Price Calculator tab."
            )

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT,
            )

            # Render existing history
            for role, text in st.session_state.chat_history:
                css_class = "pf-chat-user" if role == "user" else "pf-chat-ai"
                st.markdown(f'<div class="{css_class}">{text}</div>', unsafe_allow_html=True)

            user_msg = st.chat_input("Ask about custom designs, ideas, or your order...")
            if user_msg:
                st.session_state.chat_history.append(("user", user_msg))
                st.markdown(f'<div class="pf-chat-user">{user_msg}</div>', unsafe_allow_html=True)

                # Build the conversation for Gemini from history
                convo = model.start_chat(history=[
                    {"role": "user" if r == "user" else "model", "parts": [t]}
                    for r, t in st.session_state.chat_history[:-1]
                ])
                with st.spinner("Thinking..."):
                    response = convo.send_message(user_msg)
                ai_text = response.text
                st.session_state.chat_history.append(("assistant", ai_text))
                st.markdown(f'<div class="pf-chat-ai">{ai_text}</div>', unsafe_allow_html=True)

        except ImportError:
            st.error("The `google-generativeai` package is not installed. Check requirements.txt.")
        except Exception as e:
            st.error(f"AI Assistant error: {e}")

# ===========================================================================
# TAB 3 — CART
# ===========================================================================
with tab_cart:
    st.markdown('<div class="pf-section-title">Your Cart</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is empty. Add items from the Price Calculator tab.")
    else:
        grand_total = 0.0
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                st.markdown('<div class="pf-card">', unsafe_allow_html=True)
                c1, c2, c3 = st.columns([3, 1.3, 0.6])
                with c1:
                    st.write(f"**{item.product}** — Qty {item.quantity}")
                    st.caption(item.spec_string())
                with c2:
                    st.write(f"**{item.total:,.2f} EGP**")
                    st.caption(
                        f"Bulk -{item.bulk_discount_pct*100:.0f}% · Flash -{item.flash_discount_pct*100:.0f}%"
                    )
                with c3:
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            grand_total += item.total

        st.markdown(f"### Grand Total: **{grand_total:,.2f} EGP**")

# ===========================================================================
# TAB 4 — CHECKOUT
# ===========================================================================
with tab_checkout:
    st.markdown('<div class="pf-section-title">Checkout</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Add items to your cart first.")
    else:
        # ---- itemized summary ----
        st.subheader("Order Summary")
        grand_total = sum(item.total for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"- **{item.product}** ({item.spec_string()}) — Qty {item.quantity} → **{item.total:,.2f} EGP**")
        st.markdown(f"#### Total Due: **{grand_total:,.2f} EGP**")

        st.divider()

        # ---- customer details ----
        st.subheader("Your Details")
        cust_name = st.text_input("Full Name")
        cust_phone = st.text_input("Phone Number")
        cust_notes = st.text_area("Additional Notes (delivery, deadline, design files, etc.)")

        st.divider()

        # ---- payment method ----
        st.subheader("Payment Method")
        payment_method = st.radio("Choose how you'll pay", ["InstaPay", "Vodafone Cash"], horizontal=True)

        def make_qr_bytes(data: str) -> bytes:
            img = qrcode.make(data)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue()

        pcol1, pcol2 = st.columns([1, 1])
        with pcol1:
            if payment_method == "InstaPay":
                st.write(f"**InstaPay address:** `{INSTAPAY_IPA}`")
                st.image(make_qr_bytes(INSTAPAY_IPA), caption="Scan to pay via InstaPay", width=180)
            else:
                st.write(f"**Vodafone Cash number:** `{VODAFONE_CASH_NUMBER}`")
                st.image(make_qr_bytes(VODAFONE_CASH_NUMBER), caption="Scan / save number", width=180)
        with pcol2:
            st.caption(
                "After paying, tap **Send Order to WhatsApp** below and attach your "
                "payment screenshot in the chat so we can confirm your order quickly."
            )

        st.divider()

        # ---- build WhatsApp message ----
        st.subheader("Send Your Order")

        lines = [f"🖨️ *New Order — {BRAND_NAME}*", ""]
        for item in st.session_state.cart:
            lines.append(f"• {item.product} — Qty {item.quantity} — {item.spec_string()} — {item.total:,.2f} EGP")
        lines += [
            "",
            f"*Total: {grand_total:,.2f} EGP*",
            f"Payment method: {payment_method}",
            "",
            f"Name: {cust_name or '-'}",
            f"Phone: {cust_phone or '-'}",
            f"Notes: {cust_notes or '-'}",
        ]
        message = "\n".join(lines)
        encoded_message = urllib.parse.quote(message)
        full_number = f"{COUNTRY_CODE}{WHATSAPP_LOCAL_NUMBER.lstrip('0')}"
        whatsapp_url = f"https://wa.me/{full_number}?text={encoded_message}"

        with st.expander("Preview message"):
            st.text(message)

        st.markdown(
            f'<div class="pf-whatsapp-btn"><a href="{whatsapp_url}" target="_blank">'
            f'📲 Send Order to WhatsApp</a></div>',
            unsafe_allow_html=True,
        )

        if st.button("Clear Cart After Sending"):
            st.session_state.cart = []
            st.rerun()

# ---------------------------------------------------------------------------
# 7. FOOTER
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <hr style="border-color: rgba(255,140,66,0.25); margin-top:2.5rem;">
    <p style="text-align:center; color:#8a8a8a; font-size:0.85rem;">
        {BRAND_NAME} · Prices shown are estimates and confirmed at checkout ·
        WhatsApp: +{COUNTRY_CODE}{WHATSAPP_LOCAL_NUMBER.lstrip('0')}
    </p>
    """,
    unsafe_allow_html=True,
)
