import streamlit as st
import os
from google import genai

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="PRINT FLASH | مطبعة برنت فلاش 3D",
    page_icon="⚡",
    layout="wide"
)

# --- 2. Gemini API Setup ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    api_working = True
except Exception:
    api_working = False

# --- 3. 3D & Ultra-Modern CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }

    /* 3D Hero Banner */
    .hero-3d {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8C42 50%, #9A3412 100%);
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(255, 75, 75, 0.3), inset 0 2px 4px rgba(255,255,255,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 30px;
        transform: perspective(1000px) rotateX(2deg);
        transition: transform 0.5s ease;
    }
    .hero-3d:hover {
        transform: perspective(1000px) rotateX(0deg) scale(1.01);
    }
    .hero-3d h1 {
        font-size: 3rem !important;
        font-weight: 900;
        color: #FFFFFF !important;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    /* 3D Cards */
    .card-3d {
        background: #1e293b;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease-in-out;
        margin-bottom: 20px;
    }
    .card-3d:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 35px rgba(255, 75, 75, 0.25);
        border-color: #FF4B4B;
    }
    
    .price-tag-3d {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
        margin-top: 15px;
    }
    
    .instapay-box {
        background: #ffffff;
        color: #000000;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        margin-top: 15px;
    }

    /* Input Fields Customization */
    div[data-baseweb="select"], div[data-baseweb="input"] input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. Products Data ---
PRODUCTS = {
    "استيكرات (Stickers)": {
        "price": 2.5,
        "image": "https://images.unsplash.com/photo-1572375992501-4b0892d50c69?auto=format&fit=crop&w=800&q=80",
        "desc": "استيكرات مقاومة للماء والقطع بجودة طباعة فائقة وتفاصيل دقيقة."
    },
    "كروت شخصية (Business Cards)": {
        "price": 1.5,
        "image": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80",
        "desc": "كروت بزنس فاخرة مع خيارات سلوفان مطفأ أو لامع لترك انطباع لا يُنسى."
    },
    "فلايرات ودعايات (Flyers)": {
        "price": 3.0,
        "image": "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=800&q=80",
        "desc": "فلايرات دعاية بألوان زاهية وورق كوشيه ممتاز لتسويق مشروعك."
    },
    "بنرات ويافطات (Banners)": {
        "price": 15.0,
        "image": "https://images.unsplash.com/photo-1542744094-3a31b272c490?auto=format&fit=crop&w=800&q=80",
        "desc": "طباعة بنرات أوت دور وإن دور بأحجام كبيرة خامات عالية التحمل."
    },
    "بلوك نوت (Block Note)": {
        "price": 12.0,
        "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=800&q=80",
        "desc": "دفاتر ملاحظات مخصصة بشعار شركتك لتنظيم أفكارك ودعايتك."
    },
    "كتب وكتالوجات (Books & Catalogs)": {
        "price": 25.0,
        "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
        "desc": "طباعة وتجليد الكتب والكتالوجات بأعلى معايير الجودة والتغليف."
    }
}

INSTAPAY_USERNAME = "abdelrahman_yassen22@instapay"

# --- 5. Header Banner ---
st.markdown("""
<div class="hero-3d">
    <h1>⚡ PRINT FLASH 3D</h1>
    <p>PRINT MORE, SAVE MORE — تجربة طباعة حديثة وسريعة مع عروض واجهة مجسمة</p>
    <span style="background: rgba(0,0,0,0.4); padding: 8px 18px; border-radius: 20px; font-weight: bold; font-size: 1.1rem;">
        🔥 خصم 30% فلاش مطبق تلقائياً على كل الطلبات!
    </span>
</div>
""", unsafe_allow_html=True)

# --- 6. Navigation Tabs ---
tab1, tab2, tab3 = st.tabs(["🛍️ معرض المنتجات والأسعار", "🤖 مساعد التصميم الذكي", "💳 الدفع وتأكيد الطلب"])

# --- TAB 1: Products & Calculator ---
with tab1:
    st.subheader("إليك معرض منتجاتنا مع الحاسبة المباشرة:")
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        selected_product_name = st.selectbox("اختر المنتج:", list(PRODUCTS.keys()))
        prod_data = PRODUCTS[selected_product_name]
        
        st.markdown(f"""
        <div class="card-3d">
            <img src="{prod_data['image']}" style="width: 100%; border-radius: 12px; height: 220px; object-fit: cover; margin-bottom: 12px;">
            <h3>{selected_product_name}</h3>
            <p style="color: #cbd5e1;">{prod_data['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        quantity = st.number_input("الكمية المطلوبة:", min_value=10, value=100, step=10)
        paper_weight = st.selectbox("وزن الورق (GSM):", ["150 GSM قياسي", "300 GSM ثقيل", "350 GSM فاخر"])
        lamination = st.selectbox("نوع السلوفان/التغليف:", ["بدون", "مطفي (Matte)", "لامع (Glossy)", "مخملي (Soft-touch)"])

    raw_total = prod_data["price"] * quantity
    discounted_total = raw_total * 0.70  # 30% Discount
    
    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="price-tag-3d">
            <p style="font-size: 1.2rem; font-weight: bold; margin: 0;">الإجمالي النهائي بعد الخصم</p>
            <h1 style="font-size: 3rem; margin: 10px 0; color: #FFFFFF;">{discounted_total:,.2f} EGP</h1>
            <p style="text-decoration: line-through; color: #fca5a5; font-size: 1.2rem;">{raw_total:,.2f} EGP</p>
            <p style="font-size: 0.95rem; margin-top: 5px;">🎉 وفرت 30% في هذا العرض!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ إضافة الطلب إلى السلة", use_container_width=True, type="primary"):
            st.session_state['cart'] = {
                'product': selected_product_name,
                'quantity': quantity,
                'price': discounted_total,
                'details': f"{paper_weight} | سلوفان: {lamination}"
            }
            st.success("تم حجز المنتج وإضافته بنجاح! انتقل لتبويب الدفع لإنهاء الطلب.")

# --- TAB 2: AI Design Consultant ---
with tab2:
    st.subheader("🤖 مستشار الذكاء الاصطناعي للتصميم والطباعة")
    st.write("هل تحتار في اختيار نوع الورق أو الأبعاد المناسبة لبطاقتك أو مطبوعاتك؟ اسأل المساعد الذكي!")
    
    user_prompt = st.text_input("اكتب سؤالك هنا (مثال: ما هو أفضل وزن ورقي للكرت الشخصي؟):")
    if st.button("استشارة المساعد الذكي"):
        if user_prompt:
            if api_working:
                with st.spinner("جاري التفكير والإجابة..."):
                    try:
                        system_instruction = "أنت مستشار احترافي وخبير في مجالات الطباعة والتصميم لمطبعة PRINT FLASH. أجب باللغة العربية بأسلوب مشجع ومختصر."
                        response = client.models.generate_content(
                            model='gemini-3.6-flash',
                            contents=f"{system_instruction}\n\nالسؤال: {user_prompt}"
                        )
                        st.markdown("### الإجابة:")
                        st.info(response.text)
                    except Exception as err:
                        st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {err}")
            else:
                st.error("لم يتم العثور على مفتاح API بشكل صحيح في Secrets.")
        else:
            st.warning("يرجى كتابة السؤال أولاً.")

# --- TAB 3: InstaPay QR & Checkout ---
with tab3:
    st.subheader("💳 إتمام الطلب والدفع عبر InstaPay")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        name = st.text_input("الاسم بالكامل")
        phone = st.text_input("رقم الهاتف (واتساب)")
        payment_method = st.selectbox("طريقة الدفع الفضلى:", ["InstaPay (انستا باي)", "فودافون كاش", "الدفع عند الاستلام"])
        
        # Display InstaPay QR Image directly if uploaded
        if payment_method == "InstaPay (انستا باي)":
            st.markdown(f"""
            <div class="instapay-box">
                <h4 style="color: #6b21a8; margin-bottom: 5px;">دفعة سريعة عبر InstaPay ⚡</h4>
                <p style="font-size: 0.9rem; color: #475569;">امسح رمز الـ QR أدناه من تطبيق انستا باي للدفع المباشر:</p>
            </div>
            """, unsafe_allow_html=True)
            
            if os.path.exists("instapay_qr.jpg"):
                st.image("instapay_qr.jpg", use_column_width=True)
            else:
                st.warning("تأكد من رفع صورة instapay_qr.jpg على GitHub لظهور رمز QR الخاص بك.")
                
            st.markdown(f"""
            <div style="text-align: center; font-weight: bold; color: #6b21a8; margin-top: 8px;">
                اسم الحساب: <code>{INSTAPAY_USERNAME}</code>
            </div>
            """, unsafe_allow_html=True)
            
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if 'cart' in st.session_state:
            cart = st.session_state['cart']
            st.markdown(f"""
            <div class="card-3d">
                <h4 style="color: #FF4B4B;">ملخص الطلب الحالي:</h4>
                <p><b>المنتج:</b> {cart['product']}</p>
                <p><b>الكمية:</b> {cart['quantity']}</p>
                <p><b>التفاصيل:</b> {cart['details']}</p>
                <h3 style="color: #10b981;">الإجمالي: {cart['price']:,.2f} EGP</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("لم تقم بإضافة أي منتج للسلة حتى الآن من تبويب معرض المنتجات.")

        if st.button("📲 تأكيد وإرسال الطلب عبر الواتساب", type="primary", use_container_width=True):
            if name and phone:
                prod_title = st.session_state['cart']['product'] if 'cart' in st.session_state else "طلب جديد"
                prod_price = st.session_state['cart']['price'] if 'cart' in st.session_state else 0
                
                msg = f"طلب جديد من {name}%0Aرقم الهاتف: {phone}%0Aالمنتج: {prod_title}%0Aالإجمالي: {prod_price} EGP%0Aطريقة الدفع: {payment_method}"
                whatsapp_url = f"https://wa.me/201000000000?text={msg}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="display: inline-block; width: 100%; text-align: center; background-color: #25D366; color: white; padding: 12px; border-radius: 8px; font-weight: bold; text-decoration: none;">الانتقال إلى الواتساب للتأكيد 🚀</a>', unsafe_allow_html=True)
            else:
                st.error("يرجى كتابة الاسم ورقم الهاتف أولاً.")
