import streamlit as st
import os
from google import genai

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="PRINT FLASH | مطبعة برنت فلاش",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Gemini API Setup ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    api_working = True
except Exception:
    api_working = False

# --- 3. Ultra-Modern 2026 UI CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Readex+Pro:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Readex Pro', 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Dark Futuristic Canvas */
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 40%, #020617 100%);
        color: #f8fafc;
    }

    /* Glassmorphism Header Banner */
    .hero-2026 {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 35px;
    }
    .hero-title {
        font-size: 3.2rem !important;
        font-weight: 800;
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8c42 50%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        color: #94a3b8 !important;
        font-size: 1.1rem;
        font-weight: 300;
    }
    .badge-flash {
        display: inline-block;
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.2), rgba(245, 158, 11, 0.2));
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #fef08a !important;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 15px;
    }

    /* Product Cards UI */
    .product-card {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .product-card:hover {
        transform: translateY(-6px);
        border-color: rgba(255, 140, 66, 0.5);
        box-shadow: 0 20px 40px rgba(255, 75, 75, 0.15);
    }
    .product-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 14px;
        margin-bottom: 15px;
    }
    .product-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 8px;
    }
    .product-desc {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.5;
        margin-bottom: 15px;
    }

    /* Glass Summary Box */
    .summary-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    .price-large {
        font-size: 2.8rem;
        font-weight: 800;
        color: #10b981;
        margin: 10px 0;
    }
    
    /* InstaPay Modern Container */
    .instapay-card {
        background: #ffffff;
        color: #0f172a;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    /* Streamlit Input Overrides */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 10px 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8c42 100%) !important;
        color: #ffffff !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. Products Data ---
PRODUCTS = {
    "استيكرات (Stickers)": {
        "price": 2.5,
        "image": "https://images.unsplash.com/photo-1572375992501-4b0892d50c69?auto=format&fit=crop&w=800&q=80",
        "desc": "استيكرات قص ليزر مقاومة للمواصفات الصعبة والماء بجودة ألوان فائقة."
    },
    "كروت شخصية (Business Cards)": {
        "price": 1.5,
        "image": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
        "desc": "كروت بزنس فاخرة سلوفان مطفأ أو لامع مع لمسات كبس حراري ورنيش برجوازي."
    },
    "فلايرات ودعايات (Flyers)": {
        "price": 3.0,
        "image": "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=800&q=80",
        "desc": "دعايات إعلانية عالية الدقة بألوان خالية من العيوب لتسويق منتجاتك."
    },
    "بنرات ويافطات (Banners)": {
        "price": 15.0,
        "image": "https://images.unsplash.com/photo-1542744094-3a31b272c490?auto=format&fit=crop&w=800&q=80",
        "desc": "بنرات ضخمة بأجود خامات الأوت دور المقاومة للشمس والعوامل الجوية."
    },
    "بلوك نوت (Block Note)": {
        "price": 12.0,
        "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=800&q=80",
        "desc": "دفاتر الملاحظات المخصصة بالكامل بالهوية البصرية لشركتك."
    },
    "كتب وكتالوجات (Books & Catalogs)": {
        "price": 25.0,
        "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
        "desc": "طباعة المجلات وتجليد الكتب الفاخر بأساليب التجليد الحراري والدبابيس."
    }
}

INSTAPAY_USERNAME = "abdelrahman_yassen22@instapay"

# --- 5. Modern Header ---
st.markdown("""
<div class="hero-2026">
    <div class="hero-title">⚡ PRINT FLASH</div>
    <div class="hero-subtitle">الجيل الجديد من خدمات الطباعة السريعة والتصاميم الذكية</div>
    <div class="badge-flash">🔥 عرض الخصم المباشر 30% مطبق تلقائياً</div>
</div>
""", unsafe_allow_html=True)

# --- 6. Main Navigation ---
tab1, tab2, tab3 = st.tabs(["🛍️ متجر المنتجات والحاسبة", "🤖 استشارة الذكاء الاصطناعي", "💳 الدفع والدفع المباشر"])

# --- TAB 1: E-Commerce Grid & Calculator ---
with tab1:
    st.markdown("### اختر من قائمة المنتجات المتاحة:")
    
    # Grid of products
    cols = st.columns(3)
    product_keys = list(PRODUCTS.keys())
    
    for idx, p_name in enumerate(product_keys):
        p_info = PRODUCTS[p_name]
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{p_info['image']}" class="product-img">
                <div class="product-title">{p_name}</div>
                <div class="product-desc">{p_info['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ تخصيص وحساب تكلفة الطلب:")
    
    col_calc1, col_calc2 = st.columns([1.2, 1])
    
    with col_calc1:
        selected_prod = st.selectbox("المنتج المحدد:", product_keys)
        prod_data = PRODUCTS[selected_prod]
        
        quantity = st.number_input("الكمية المطلوب طباعتها:", min_value=10, value=100, step=10)
        paper_weight = st.selectbox("نوع ووزن الورق:", ["150 GSM كوشيه قياسي", "300 GSM كوشيه ثقيل", "350 GSM كرتون فاخر"])
        lamination = st.selectbox("نوع السلوفان (التغليف):", ["بدون سلوفان", "مطفي (Matte Premium)", "لامع (High Gloss)", "مخملي (Soft-touch)"])

    raw_price = prod_data["price"] * quantity
    final_price = raw_price * 0.70  # 30% Flash discount

    with col_calc2:
        st.markdown(f"""
        <div class="summary-card">
            <span style="color: #94a3b8; font-size: 0.9rem;">إجمالي التكلفة التقديرية</span>
            <div class="price-large">{final_price:,.2f} <span style="font-size: 1.2rem;">EGP</span></div>
            <div style="text-decoration: line-through; color: #ef4444; font-size: 1rem; margin-bottom: 10px;">{raw_price:,.2f} EGP</div>
            <p style="color: #34d399; font-size: 0.85rem; font-weight: 600;">✨ خصم 30% مفعّل بنجاح</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🛒 تأكيد السلة والإنتقال للدفع", use_container_width=True, type="primary"):
            st.session_state['cart'] = {
                'product': selected_prod,
                'quantity': quantity,
                'price': final_price,
                'details': f"{paper_weight} | {lamination}"
            }
            st.success("تم تسجيل المنتج بالسلة! انتقل لتبويب (الدفع والدفع المباشر) لتأكيد طلبك.")

# --- TAB 2: AI Design Assistant (Clean Error Handling) ---
with tab2:
    st.markdown("### 🤖 مساعد التوجيه الذكي للتصاميم")
    st.write("احصل على نصائح فورية بخصوص المقاسات، جودة الألوان، والخامات الأنسب لمشروعك.")
    
    user_prompt = st.text_input("اطرح سؤالك على الذكاء الاصطناعي:")
    if st.button("استشارة المساعد"):
        if user_prompt:
            if api_working:
                with st.spinner("جاري التواصل مع المحرك الذكي..."):
                    try:
                        system_instruction = "أنت مستشار احترافي وخبير في مجالات الطباعة والتصميم لمطبعة PRINT FLASH. أجب باللغة العربية بأسلوب مشجع ومختصر."
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"{system_instruction}\n\nالسؤال: {user_prompt}"
                        )
                        st.markdown("#### الإجابة:")
                        st.info(response.text)
                    except Exception:
                        # Clean UI Warning instead of showing raw technical codes
                        st.warning("⚠️ محرك الذكاء الاصطناعي مشغول حالياً لكثرة الطلبات. يرجى إعادة الضغط على الزر بعد بضع ثوانٍ.")
            else:
                st.error("⚠️ مفتاح الاتصال بالذكاء الاصطناعي غير متوفر.")
        else:
            st.warning("يرجى كتابة السؤال أولاً.")

# --- TAB 3: InstaPay QR & WhatsApp Checkout ---
with tab3:
    st.markdown("### 💳 إتمام الطلب والدفع المباشر")
    
    c1, c2 = st.columns([1.1, 1])
    
    with c1:
        name = st.text_input("الاسم الأول والأخير")
        phone = st.text_input("رقم الهاتف (المرتبط بالواتساب)")
        payment_method = st.selectbox("طريقة الدفع الفضلى:", ["InstaPay (انستا باي)", "فودافون كاش", "الدفع عند الاستلام"])
        
        if payment_method == "InstaPay (انستا باي)":
            st.markdown(f"""
            <div class="instapay-card">
                <h3 style="color: #4c1d95; margin-bottom: 5px; font-weight: 700;">InstaPay ⚡</h3>
                <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 15px;">امسح رمز الـ QR التالي عبر التطبيق للدفع السريع:</p>
            </div>
            """, unsafe_allow_html=True)
            
            if os.path.exists("instapay_qr.jpg"):
                st.image("instapay_qr.jpg", use_column_width=True)
            else:
                st.info("رمز QR الخاص بـ InstaPay مفعّل.")
                
            st.markdown(f"""
            <div style="text-align: center; font-weight: bold; color: #a855f7; margin-top: 10px; font-size: 1.1rem;">
                عنوان الحساب: <span style="background: rgba(168,85,247,0.1); padding: 4px 10px; border-radius: 8px;">{INSTAPAY_USERNAME}</span>
            </div>
            """, unsafe_allow_html=True)
            
    with c2:
        if 'cart' in st.session_state:
            cart = st.session_state['cart']
            st.markdown(f"""
            <div class="summary-card">
                <h4 style="color: #ff8c42; margin-bottom: 15px;">تفاصيل الطلب الحالي:</h4>
                <p><b>المنتج:</b> {cart['product']}</p>
                <p><b>الكمية:</b> {cart['quantity']}</p>
                <p><b>المواصفات:</b> {cart['details']}</p>

                <hr style="border-color: rgba(255,255,255,0.1);">
                <div style="font-size: 1.3rem; font-weight: bold; color: #10b981;">المبلغ المستحق: {cart['price']:,.2f} EGP</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("لم تقم بإضافة أي منتج إلى السلة بعد. يمكنك اختيار المنتج من التبويب الأول.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📲 إرسال الطلب عبر الواتساب", type="primary", use_container_width=True):
            if name and phone:
                prod_title = st.session_state['cart']['product'] if 'cart' in st.session_state else "طلب جديد"
                prod_price = st.session_state['cart']['price'] if 'cart' in st.session_state else 0
                
                msg = f"طلب جديد من {name}%0Aرقم الهاتف: {phone}%0Aالمنتج: {prod_title}%0Aالإجمالي: {prod_price} EGP%0Aطريقة الدفع: {payment_method}"
                whatsapp_url = f"https://wa.me/201000000000?text={msg}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: block; text-align: center; background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; padding: 14px; border-radius: 12px; font-weight: bold; text-decoration: none; box-shadow: 0 10px 20px rgba(37,211,102,0.3);">إرسال الآن عبر الواتساب 🚀</a>', unsafe_allow_html=True)
            else:
                st.error("يرجى إدخال الاسم ورقم الهاتف أولاً.")
