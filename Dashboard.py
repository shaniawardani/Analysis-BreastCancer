import streamlit as st

# Translations for English and Bahasa Indonesia
translations = {
    'en': {
        'greeting': 'Hello',
        'vision': 'Vision',
        'mission': 'Mission',
        'prevention': 'Prevention',
        'symptoms': 'Symptoms',
        'login_warning': 'You are not logged in. Please log in first.',
        'login_link': 'Click here to login',
        'title': 'Fighting Breast Cancer Takes Everyone',
        'subtitle': 'Cancer may challenge your body but it can never break your spirit.',
        'breast_cancer_info': '''Welcome to Breast Cancer Analysis! A website dedicated 
        to empowering patients, healthcare professionals, and researchers with advanced 
        tools for understanding and diagnosing breast cancer. Our platform leverages cutting-edge
        machine learning technology to analyze medical data, providing accurate and efficient 
        breast cancer classification to aid in early detection and personalized treatment plans.''',
        'vision_info': 'To integrate AI in healthcare, making breast cancer diagnosis faster and more precise, ultimately improving patient outcomes globally through accurate.',
        'mission_info': 'To leverage technology for early breast cancer diagnosis and personalized treatment, empowering healthcare providers with accurate, data-driven insights.',
        'prevention_info': '''Breast cancer prevention involves making healthy lifestyle choices and regular screenings. 
        Engaging in physical activities like walking, swimming, or running reduces the risk. 
        Aim for at least 30 minutes of exercise daily. A balanced diet with fruits, vegetables, whole grains, and lean proteins is key, while limiting processed foods and red meats. 
        Avoiding alcohol and quitting smoking are crucial as they increase cancer risk. Breastfeeding can also lower the risk, especially extended breastfeeding. 
        Regular screenings, particularly for those with a family history, are important for early detection.''',
        'symptoms_info': '''Breast cancer symptoms can vary, but common signs include a painless lump in the breast or armpit. Changes in breast shape or size, such as swelling, shrinkage, or asymmetry, should also be monitored. Skin changes, like redness or dimpling, may indicate cancer. Nipple changes, such as unusual discharge or alterations in appearance (inversion, scaling, itching), are also signs. Persistent pain in the breast can occur but is not always present. If any of these symptoms appear, consult a healthcare professional for early diagnosis.''',
    },
    'id': {
        'greeting': 'Halo',
        'vision': 'Visi',
        'mission': 'Misi',
        'prevention': 'Pencegahan',
        'symptoms': 'Gejala',
        'login_warning': 'Anda belum masuk. Silakan masuk terlebih dahulu.',
        'login_link': 'Klik di sini untuk masuk',
        'title': 'Melawan Kanker Payudara Membutuhkan Semua Orang',
        'subtitle': 'Kanker mungkin menantang tubuh Anda tetapi tidak bisa menghancurkan semangat Anda.',
        'breast_cancer_info': '''Selamat datang di Breast Cancer Analysis! Situs web yang didedikasikan untuk memberdayakan pasien, profesional perawatan kesehatan, dan peneliti dengan berbagai alat canggih untuk memahami dan mendiagnosis kanker payudara. Platform kami memanfaatkan teknologi pembelajaran mesin mutakhir untuk menganalisis data medis, menyediakan klasifikasi kanker payudara yang akurat dan efisien untuk membantu deteksi dini dan rencana perawatan yang dipersonalisasi.''',
        'vision_info': 'Untuk mengintegrasikan AI dalam perawatan kesehatan, membuat diagnosis kanker payudara lebih cepat dan lebih tepat, yang pada akhirnya meningkatkan hasil perawatan pasien secara global melalui keakuratan.',
        'mission_info': 'Untuk memanfaatkan teknologi untuk diagnosis dini kanker payudara dan perawatan yang dipersonalisasi, memberdayakan penyedia layanan kesehatan dengan wawasan yang akurat dan berbasis data.',
        'prevention_info': '''Pencegahan kanker payudara melibatkan pilihan gaya hidup sehat dan pemeriksaan rutin. Aktivitas fisik seperti berjalan, berenang, atau lari dapat mengurangi risiko. Usahakan berolahraga minimal 30 menit setiap hari. Pola makan seimbang dengan buah, sayur, biji-bijian, dan protein tanpa lemak sangat penting, sambil mengurangi konsumsi makanan olahan dan daging merah. Menghindari alkohol dan berhenti merokok juga penting karena keduanya meningkatkan risiko kanker. Menyusui dapat menurunkan risiko, terutama menyusui jangka panjang. Pemeriksaan rutin, terutama bagi yang memiliki riwayat keluarga kanker payudara, penting untuk deteksi dini.''',
        'symptoms_info': '''Gejala kanker payudara bisa bervariasi, tetapi tanda umum meliputi benjolan tidak nyeri di payudara atau ketiak. Perubahan bentuk atau ukuran payudara, seperti pembengkakan, penyusutan, atau ketidakseimbangan, perlu diwaspadai. Perubahan kulit, seperti kemerahan atau lekukan, juga bisa menjadi tanda awal. Perubahan pada puting, seperti cairan keluar atau perubahan penampilan (pembalikan, pengelupasan, gatal), juga perlu diperhatikan. Rasa sakit yang terus-menerus di payudara bisa terjadi, meski tidak selalu ada. Jika mengalami gejala ini, segera konsultasikan ke tenaga medis untuk diagnosis dini.''',
    }
}

# Page configuration
def set_page_config():
    st.set_page_config(
        page_icon="./asset/logo.png",
        page_title="Breast Cancer Analysis",
        layout="wide",
        initial_sidebar_state="expanded",
    )

# Custom CSS styling
def inject_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F6F6F6;
        }
        /* Styling for the sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFB3D9;
            color: white;
            padding-top: 20px;
            font-size: 1.1rem;
        }
        /* Sidebar logo styling */
        .sidebar-logo {
            display: block;
            margin: 0 auto;
            width: 80px;
            height: auto;
        }
        /* Custom font styling */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        .custom-font {
            font-family: 'Poppins', Changa One;
            color: #1E1E1E;
        }
        .bold-heading {
            font-weight: 600;
            font-size: 2rem;
            color: #D81B60;
        }
        .subtitle {
            font-size: 1.8rem;
            color: #333;
            margin-top: 10px;
        }
        .section-heading {
            font-weight: 600;
            font-size: 1.5rem;
            margin-top: 30px;
            text-align: center;
            color: #D81B60;
        }
        .section-content {
            font-size: 1.1rem;
            color: #555;
            text-align: justify;
            line-height: 1.6;
            margin-top: 15px;
        }
        /* Styling for content sections with hover effect */
        .content-container {
            padding: 20px;
            background-color: #FFB3D9;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .content-container:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }
        .cta-button {
            background-color: #D81B60;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-align: center;
            display: inline-block;
            margin-top: 20px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        /* Removing hover effect from title/intro section */
        .no-hover {
            box-shadow: none !important;
            transform: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar rendering
def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center;">
                <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/logo.png?raw=true' class='sidebar-logo'/>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Language selection in the sidebar
        language = st.selectbox('Language/Bahasa', ['en', 'id'])
        st.session_state['language'] = language

# Main function
def main():
    set_page_config()
    render_sidebar()
    inject_custom_css()

    # Get the selected language text
    text = translations[st.session_state.get('language', 'en')]

    # Main content columns without hover effect for the title
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            f"""
            <h1 class='custom-font bold-heading no-hover'>
                {text['title']}
            </h1>
            <p class='subtitle custom-font no-hover'>{text['subtitle']}</p>
            """,
            unsafe_allow_html=True
        )
          
    with col2:
        st.markdown(
            f"""
            <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/jumbotron1.png?raw=true' class='header-image'/>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(f"<div class='content-container'><h2 class='section-heading'>{text['greeting']}</h2><p class='section-content'>{text['breast_cancer_info']}</p></div>", unsafe_allow_html=True)
    # Vision, Mission, Prevention, Symptoms Sections in columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"<div class='content-container'><h2 class='section-heading'>{text['vision']}</h2><p class='section-content'>{text['vision_info']}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='content-container'><h2 class='section-heading'>{text['symptoms']}</h2><p class='section-content'>{text['symptoms_info']}</p></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='content-container'><h2 class='section-heading'>{text['mission']}</h2><p class='section-content'>{text['mission_info']}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='content-container'><h2 class='section-heading'>{text['prevention']}</h2><p class='section-content'>{text['prevention_info']}</p></div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()