import streamlit as st
import os
from google import genai

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="PRINT FLASH | المتجر الإلكتروني المتقدم",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Gemini API Setup ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    api_working = True
except Exception:
    api_working = False

# --- 3. Ultra-Modern UI/UX Styling (2026 Dark/Neon Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Readex+Pro:wght@300;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Readex Pro', sans-serif;
    }
    
    .stApp {
        background: #090d16;
        color: #f8fafc;
    }

    /* Glassmorphic Header Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        margin-bottom: 30px;
    }
    
    .hero-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4b4b, #ff8c42, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .badge-discount {
        background: linear-gradient(90deg, #ef4444, #f59e0b);
        color: white;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        margin-top: 10px;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }

    /* Product Cards Styling */
    .product-card-2026 {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 18px;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .product-card-2026:hover {
        border-color: #ff8c42;
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(255, 140, 66, 0.15);
    }
    
    .card-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 14px;
        margin-bottom: 12px;
    }
    
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 6px;
    }
    
    .card-category {
        font-size: 0.75rem;
        color: #ff8c42;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .card-desc {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.4;
        margin-bottom: 15px;
    }
    
    .price-badge {
        font-size: 1.3rem;
        font-weight: 800;
        color: #10b981;
    }
    
    /* Summary Box */
    .summary-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    
    /* Custom Sidebar Controls */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. Products Data Base ---
PRODUCTS = [
    {
        "id": 1,
        "name": "استيكرات قص ليزر (Stickers)",
        "category": "ملصقات واستيكرات",
        "unit_price": 2.5,
        "image": "https://images.unsplash.com/photo-1572375992501-4b0892d50c69?auto=format&fit=crop&w=800&q=80",
        "desc": "استيكرات مقاومة للماء والقطع بجودة ألوان فائقة وتحديد دقيق."
    },
    {
        "id": 2,
        "name": "كروت شخصية فاخرة (Business Cards)",
        "category": "مطبوعات ورقية",
        "unit_price": 1.5,
        "image": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
        "desc": "كروت بزنس سلوفان مطفي أو لامع مع خيارات بصمة ورنيش بارز."
    },
    {
        "id": 3,
        "name": "فلايرات ودعايات (Flyers)",
        "category": "مطبوعات ورقية",
        "unit_price": 3.0,
        "image": "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=800&q=80",
        "desc": "فلايرات إعلانية تسويقية بألوان زاهية وورق كوشيه ممتاز."
    },
    {
        "id": 4,
        "name": "بنرات ويافطات (Outdoor Banners)",
        "category": "دعاية وإعلانات ضخمة",
        "unit_price": 15.0,
        "image": "https://images.unsplash.com/photo-1542744094-3a31b272c490?auto=format&fit=crop&w=800&q=80",
        "desc": "بنرات وفليكس أوت دور مقاومة للشمس وعوامل الجو المختلفة."
    },
    {
        "id": 5,
        "name": "بلوك نوت شركات (Block Note)",
        "category": "مطبوعات ورقية",
        "unit_price": 12.0,
        "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=800&q=80",
        "desc": "دفاتر ملاحظات مخصصة بالكامل بهوية شركتك وشعارك."
    },
    {
        "id": 6,
        "name": "كتالوجات ومجلات (Catalogs & Books)",
        "category": "مطبوعات ورقية",
        "unit_price": 25.0,
        "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
        "desc": "طباعة المجلات وتجليد الكتب الفاخر بأساليب التجليد الحراري والدبابيس."
    }
]

INSTAPAY_USERNAME = "abdelrahman_yassen22@instapay"

# --- 5. Main Header ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚡ PRINT FLASH</div>
    <p style="color: #94a3b8; font-size: 1.1rem; margin: 0;">منصة الطباعة المتقدمة والتصاميم الذكية</p>
    <div class="badge-discount">🔥 خصم 30% فلاش مطبق على جميع المنتجات</div>
</div>
""", unsafe_allow_html=True)

# --- 6. Sidebar (Filter Controls & UI UI/UX) ---
with st.sidebar:
    st.markdown("## 🔍 تصفية وفلترة المنتجات")
    st.markdown("---")
    
    # Search input
    search_query = st.text_input("🔎 بحث باسم المنتج:", "")
    
    # Category Filter
    categories = ["الكل"] + list(set(p["category"] for p in PRODUCTS))
    selected_category = st.selectbox("📁 فئة المنتج:", categories)
    
    # Price Range Filter
    max_p = max(p["unit_price"] for p in PRODUCTS)
    min_p = min(p["unit_price"] for p in PRODUCTS)
    price_range = st.slider("💰 نطاق سعر القطعة (EGP):", float(min_p), float(max_p), (float(min_p), float(max_p)))

# Filter Logic
filtered_products = [
    p for p in PRODUCTS
    if (search_query.lower() in p["name"].lower() or search_query == "")
    and (selected_category == "الكل" or p["category"] == selected_category)
    and (price_range[0] <= p["unit_price"] <= price_range[1])
]

# --- 7. Main Tabs ---
tab1, tab2, tab3 = st.tabs(["🛍️ معرض المنتجات وتخصيص الطلب", "🤖 المساعد الذكي", "💳 الدفع وتأكيد الطلب"])

# --- TAB 1: E-COMMERCE STORE & CALCULATOR ---
with tab1:
    st.markdown(f"### 📦 المنتجات المتاحة ({len(filtered_products)})")
    
    if not filtered_products:
        st.warning("عفواً، لا توجد منتجات تطابق خيارات الفلترة الحالية.")
    else:
        # Display Grid
        cols = st.columns(3)
        for idx, prod in enumerate(filtered_products):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="product-card-2026">
                    <div>
                        <img src="{prod['image']}" class="card-img">
                        <div class="card-category">{prod['category']}</div>
                        <div class="card-title">{prod['name']}</div>
                        <div class="card-desc">{prod['desc']}</div>
                    </div>
                    <div>
                        <hr style="border-color: rgba(255,255,255,0.05); margin: 10px 0;">
                        <div style="display:flex; justify-shadow: space-between; align-items: center;">
                            <span style="font-size:0.8rem; color:#94a3b8;">السعر يبدأ من:</span>
                            <span class="price-badge">{prod['unit_price']} EGP</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ تخصيص المنتج وحساب التكلفة")
    
    calc_c1, calc_c2 = st.columns([1.2, 1])
    
    with calc_c1:
        prod_names = [p["name"] for p in PRODUCTS]
        chosen_prod_name = st.selectbox("اختر المنتج لتخصيصه:", prod_names)
        chosen_prod = next(p for p in PRODUCTS if p["name"] == chosen_prod_name)
        
        quantity = st.number_input("الكمية المطلوبة:", min_value=10, value=100, step=10)
        paper_weight = st.selectbox("نوع ووزن الورق / الخامة:", ["150 GSM قياسي", "300 GSM ثقيل (كوشيه)", "350 GSM فاخر (كرتون)"])
        lamination = st.selectbox("نوع السلوفان / التغليف:", ["بدون تغليف", "مطفي (Matte)", "لامع (Glossy)", "مخملي (Soft-touch)"])

    raw_total = chosen_prod["unit_price"] * quantity
    discounted_total = raw_total * 0.70  # 30% Flash discount

    with calc_c2:
        st.markdown(f"""
        <div class="summary-card">
            <span style="color: #94a3b8; font-size: 0.9rem;">إجمالي الطلب بعد الخصم</span>
            <div style="font-size: 2.8rem; font-weight: 800; color: #10b981; margin: 5px 0;">
                {discounted_total:,.2f} <span style="font-size: 1.2rem;">EGP</span>
            </div>
            <div style="text-decoration: line-through; color: #ef4444; font-size: 1rem; margin-bottom: 12px;">{raw_total:,.2f} EGP</div>
            <p style="color: #34d399; font-size: 0.85rem; font-weight: 600; margin: 0;">✨ ووفرت 30% في هذا العرض!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🛒 حجز وتأكيد إضافة المنتج للسلة", type="primary", use_container_width=True):
            st.session_state['cart'] = {
                'product': chosen_prod["name"],
                'quantity': quantity,
                'price': discounted_total,
                'details': f"{paper_weight} | تغليف: {lamination}"
            }
            st.success("تم حجز المنتج وإضافته للسلة بنجاح! انتقل لتبويب الدفع وتأكيد الطلب.")

# --- TAB 2: AI CONSULTANT (STABLE HANDLING) ---
with tab2:
    st.markdown("### 🤖 مستشار الطباعة والتصميم الذكي")
    st.write("اطرح أي سؤال حول المقاسات، ألوان الطباعة CMYK، أو أفضل أنواع الورق لمشروعك.")
    
    user_prompt = st.text_input("اكتب سؤالك هنا:")
    if st.button("استشارة الذكاء الاصطناعي"):
        if user_prompt:
            if api_working:
                with st.spinner("جاري الاتصال بالمساعد الذكي..."):
                    try:
                        # جلب الاستجابة بأمان دون إظهار أخطاء خام
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"أنت مستشار طباعة احترافي لمطبعة PRINT FLASH. أجب باختصار باللغة العربية: {user_prompt}"
                        )
                        st.info(response.text)
                    except Exception:
                        st.warning("⚠️ الخدمة تشهد إقبالاً كبيراً حالياً. يرجى الضغط مرة أخرى خلال ثوانٍ.")
            else:
                st.error("⚠️ لم يتم ضبط مفتاح الـ API بشكل صحيح.")
        else:
            st.warning("يرجى كتابة السؤال أولاً.")

# --- TAB 3: INSTAPAY & WHATSAPP CHECKOUT ---
with tab3:
    st.markdown("### 💳 إتمام وتأكيد الطلب")
    
    pay_c1, pay_c2 = st.columns([1.1, 1])
    
    with pay_c1:
        name = st.text_input("الاسم بالكامل")
        phone = st.text_input("رقم الواتساب للتواصل")
        payment_method = st.selectbox("طريقة الدفع الفضلى:", ["InstaPay (انستا باي)", "فودافون كاش", "الدفع عند الاستلام"])
        
        if payment_method == "InstaPay (انستا باي)":
            st.markdown("""
            <div style="background: #ffffff; color: #000; padding: 20px; border-radius: 16px; text-align: center; margin-top: 15px;">
                <h4 style="color: #4c1d95; margin-bottom: 5px;">الدفع الفوري عبر InstaPay ⚡</h4>
                <p style="font-size: 0.85rem; color: #475569;">امسح رمز الـ QR أو انسخ اسم الحساب للدفع مباشرة:</p>
            </div>
            """, unsafe_allow_html=True)
            
            if os.path.exists("instapay_qr.jpg"):
                st.image("instapay_qr.jpg", use_column_width=True)
            
            st.code(INSTAPAY_USERNAME, language=None)

    with pay_c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if 'cart' in st.session_state:
            cart = st.session_state['cart']
            st.markdown(f"""
            <div class="summary-card">
                <h4 style="color: #ff8c42; margin-bottom: 12px;">ملخص طلبك الحالي:</h4>
                <p><b>المنتج:</b> {cart['product']}</p>
                <p><b>الكمية:</b> {cart['quantity']}</p>
                <p><b>التفاصيل:</b> {cart['details']}</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <div style="font-size: 1.3rem; font-weight: bold; color: #10b981;">الإجمالي المطلوب: {cart['price']:,.2f} EGP</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("لم تقم بإضافة أي منتج إلى السلة بعد. يمكنك اختيار المنتج من التبويب الأول.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📲 إرسال وتأكيد الطلب عبر الواتساب", type="primary", use_container_width=True):
            if name and phone:
                prod_title = st.session_state['cart']['product'] if 'cart' in st.session_state else "طلب جديد"
                prod_price = st.session_state['cart']['price'] if 'cart' in st.session_state else 0
                
                msg = f"طلب جديد من {name}%0Aرقم الهاتف: {phone}%0Aالمنتج: {prod_title}%0Aالإجمالي: {prod_price} EGP%0Aطريقة الدفع: {payment_method}"
                whatsapp_url = f"https://wa.me/201000000000?text={msg}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: block; text-align: center; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; padding: 14px; border-radius: 12px; font-weight: bold; text-decoration: none; box-shadow: 0 10px 20px rgba(37,211,102,0.3);">إرسال الآن عبر الواتساب 🚀</a>', unsafe_allow_html=True)
            else:
                st.error("يرجى إدخال الاسم ورقم الهاتف أولاً.")
