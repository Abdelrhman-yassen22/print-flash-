import streamlit as st
from google import genai

# --- Page Config ---
st.set_page_config(
    page_title="PRINT FLASH | مطبعة برنت فلاش",
    page_icon="🪞",
    layout="wide"
)

# --- GEMINI API SETUP (New Google GenAI SDK) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    api_working = True
except Exception as e:
    api_working = False

# --- CSS Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #FDFBF7;
        color: #222222;
    }
    .hero-banner {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8C42 50%, #FFC107 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .hero-banner h1 { color: white !important; font-weight: 800; }
    .hero-banner p { color: #FFF3E0 !important; font-size: 1.1rem; }
    
    label, .stMarkdown, p, span, h1, h2, h3, h4, h5, h6 {
        color: #2D3748 !important;
    }
    
    .stSelectbox div[data-baseweb="select"], .stNumberInput input, .stTextInput input {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        border: 1px solid #CBD5E0 !important;
        border-radius: 8px !important;
    }

    .price-card {
        background: #FFFFFF;
        border: 2px solid #FF6B6B;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.15);
    }
    .price-card h2 {
        color: #E53E3E !important;
        font-size: 2.5rem;
        margin: 0;
    }
    .price-card del {
        color: #A0AEC0 !important;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="hero-banner">
    <h1>🪞 PRINT FLASH</h1>
    <p>PRINT MORE, SAVE MORE — Premium printing with special offers for every project</p>
    <span style="background: rgba(0,0,0,0.2); padding: 5px 12px; border-radius: 20px; font-weight: bold;">
        🔥 30% FLASH OFFER — Applied automatically at checkout
    </span>
</div>
""", unsafe_allow_html=True)

# --- Navigation Tabs ---
tab1, tab2, tab3 = st.tabs(["💰 Price Calculator", "🤖 AI Design Assistant", "🛒 Checkout & Order"])

# --- Tab 1: Price Calculator ---
with tab1:
    st.subheader("Build Your Order")
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        product = st.selectbox("Choose a product", ["Stickers", "Business Cards", "Flyers / Leaflets", "Banners", "Block Note", "Books"])
        quantity = st.number_input("Quantity", min_value=10, value=100, step=10)
        size = st.selectbox("Size", ["Standard (A4/Business)", "Custom", "Large Format"])
        paper_weight = st.selectbox("Paper Weight (GSM)", ["150 GSM Standard", "300 GSM Heavy", "350 GSM Premium"])
        sides = st.radio("Sides", ["Single-sided", "Double-sided"])
        lamination = st.selectbox("Lamination", ["None", "Matte", "Glossy", "Soft-touch"])

    base_rates = {"Stickers": 2.5, "Business Cards": 1.5, "Flyers / Leaflets": 3.0, "Banners": 15.0, "Block Note": 12.0, "Books": 25.0}
    unit_price = base_rates.get(product, 2.0)
    
    raw_total = unit_price * quantity
    discounted_total = raw_total * 0.70
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="price-card">
            <p style="font-weight: bold; margin-bottom: 5px;">Live Price</p>
            <h2>{discounted_total:,.2f} EGP</h2>
            <del>{raw_total:,.2f} EGP</del>
            <p style="color: #38A169 !important; font-weight: bold; margin-top: 10px;">Saved 30% with Flash Discount!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ Add to Cart", use_container_width=True, type="primary"):
            st.success(f"Added {quantity} x {product} to cart!")

# --- Tab 2: AI Design Assistant ---
with tab2:
    st.subheader("🤖 AI Design Consultant")
    st.write("Need help deciding paper types, sizes, or design tips? Ask our AI assistant!")
    
    user_prompt = st.text_input("Ask a question about your print job:")
    if st.button("Ask AI Assistant"):
        if user_prompt:
            if api_working:
                with st.spinner("جاري التفكير والإجابة..."):
                    try:
                        system_instruction = "أنت مساعد ذكي ومتخصص في مجالات الطباعة والتصميم لمطبعة PRINT FLASH. أجب باللغة العربية بأسلوب احترافي ومختصر."
                        response = client.models.generate_content(
                            model='gemini-3.6-flash',
                            contents=f"{system_instruction}\n\nالسؤال: {user_prompt}"
                        )
                        st.markdown("### الإجابة:")
                        st.write(response.text)
                    except Exception as err:
                        st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {err}")
            else:
                st.error("لم يتم العثور على مفتاح API بشكل صحيح في Secrets.")
        else:
            st.warning("Please enter a question first.")

# --- Tab 3: Checkout ---
with tab3:
    st.subheader("🛒 Finalize Order via WhatsApp")
    st.write("Confirm your order details and send directly to our team on WhatsApp.")
    
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    payment_method = st.selectbox("Preferred Payment Method", ["InstaPay", "Vodafone Cash", "Cash on Delivery"])
    
    if st.button("📲 Send Order via WhatsApp", type="primary"):
        if name and phone:
            msg = f"New Order from {name} (%2B2{phone}): {quantity} {product} via {payment_method}"
            whatsapp_url = f"https://wa.me/201000000000?text={msg}"
            st.markdown(f'[Click here to complete order on WhatsApp]({whatsapp_url})')
        else:
            st.error("Please fill in your name and phone number.")
