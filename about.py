import streamlit as st

# Translation dictionary
translations = {
    'en': {
        'title': 'About Us',
        'vision': 'Vision',
        'mission': 'Mission',
        'vision_text': 'To integrate AI and healthcare, making breast cancer diagnosis faster and more precise, ultimately improving patient outcomes worldwide.',
        'mission_text': 'To leverage technology for early breast cancer diagnosis and personalized treatment, empowering healthcare providers with accurate, data-driven insights.',
        'welcome': 'Welcome to Breast Cancer Analysis!',
        'about': '''Our website empowers patients, healthcare professionals, and researchers with tools for understanding breast cancer. Leveraging AI and machine learning, we analyze medical data for accurate classification, aiding early detection and personalized treatments.''',
    },
    'id': {
        'title': 'Tentang Kami',
        'vision': 'Visi',
        'mission': 'Misi',
        'vision_text': 'Mengintegrasikan AI dan layanan kesehatan, membuat diagnosis kanker payudara lebih cepat dan tepat untuk meningkatkan hasil perawatan pasien di seluruh dunia.',
        'mission_text': 'Memanfaatkan teknologi untuk diagnosis dini kanker payudara dan perawatan yang dipersonalisasi, memberikan wawasan akurat kepada penyedia layanan kesehatan.',
        'welcome': 'Selamat datang di Breast Cancer Analysis!',
        'about': '''Situs web kami memberdayakan pasien, profesional perawatan kesehatan, dan peneliti dengan alat untuk memahami kanker payudara. Dengan AI dan pembelajaran mesin, kami menganalisis data medis untuk klasifikasi yang akurat, membantu deteksi dini dan perawatan yang dipersonalisasi.''',
    }
}

# Page configuration
def set_page_config():
    st.set_page_config(
        page_title="Breast Cancer Analysis",
        page_icon="💖",
        layout="wide"
    )

# Inject custom CSS for design
def inject_custom_css():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #fbe7f2, #ffeef8);
        }
        h1, h2 {
            color: #d81b60;
            text-align: center;
        }
        p {
            color: #555;
            font-size: 1.1rem;
            line-height: 1.6;
            text-align: justify;
        }

        .vision, .mission {
            padding: 20px;
            border-radius: 20px;
            background: linear-gradient(135deg, #ffd9eb, #ffe5f2);
            box-shadow: 0px 4px 20px rgba(216, 27, 96, 0.15);
            text-align: center;
        }
        .vision:hover, .mission:hover {
            transform: translateY(-10px);
            transition: all 0.3s ease-in-out;
            box-shadow: 0px 8px 30px rgba(216, 27, 96, 0.3);
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #ffb3d9, #ffccde);
            color: white;
            padding: 20px;
        }
        .sidebar-logo {
            display: block;
            margin: 0 auto 20px;
            width: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar rendering
def render_sidebar():
    st.sidebar.markdown(
        """
        <div style="text-align: center;">
            <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/logo.png?raw=true' class='sidebar-logo'/>
        </div>
        """,
        unsafe_allow_html=True,
    )
    language = st.sidebar.selectbox("Language / Bahasa", ["en", "id"])
    st.session_state['language'] = language

# Main content
def render_content():
    # Get the selected language
    language = st.session_state.get('language', 'en')
    text = translations[language]

    # Welcome Section
    st.markdown(f"<h1>{text['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p>{text['about']}</p>", unsafe_allow_html=True)

    # Vision and Mission Section with Left and Right Aligned Columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            f"""
            <div class='vision'>
                <h2>{text['vision']}</h2>
                <p>{text['vision_text']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class='mission'>
                <h2>{text['mission']}</h2>
                <p>{text['mission_text']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Main function
def main():
    set_page_config()
    inject_custom_css()
    render_sidebar()
    render_content()

if __name__ == "__main__":
    main()
