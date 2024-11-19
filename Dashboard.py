# import streamlit as st

# # Translations for English and Bahasa Indonesia
# translations = {
#     'en': {
#         'greeting': 'Hello',
#         'login_warning': 'You are not logged in. Please log in first.',
#         'login_link': 'Click here to login',
#         'title': 'Fighting Breast Cancer Takes Everyone',
#         'subtitle': 'Cancer may challenge your body but it can never break your spirit.'
#     },
#     'id': {
#         'greeting': 'Halo',
#         'login_warning': 'Anda belum masuk. Silakan masuk terlebih dahulu.',
#         'login_link': 'Klik di sini untuk masuk',
#         'title': 'Melawan Kanker Payudara Membutuhkan Semua Orang',
#         'subtitle': 'Kanker mungkin menantang tubuh Anda tetapi tidak bisa menghancurkan semangat Anda.'
#     }
# }

# def set_page_config():
#     """Set the initial page configuration."""
#     st.set_page_config(
#         page_icon="./asset/logo.png",
#         page_title="Breast Cancer Analysis",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

# def inject_custom_css():
#     """Inject custom CSS for styling."""
#     st.markdown(
#         """
#         <style>
#         .stApp {
#             background-color: #F6F6F6;
#         }
#         /* Styling for the sidebar */
#         [data-testid="stSidebar"] {
#             background-color: #FFB3D9;
#             color: white;
#         }
#         /* Sidebar logo styling */
#         .sidebar-logo {
#             display: block;
#             margin: 0 auto;
#             width: 80px;
#             height: auto;
#         }
#         /* Header image */
#         .header-image {
#             width: 100%;
#             height: auto;
#             margin-bottom: 20px;
#         }
#         /* Custom font styling */
#         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
#         .custom-font {
#             font-family: 'Poppins', sans-serif;
#             color: #1E1E1E;
#         }
#         .bold-heading {
#             font-weight: 700;
#             color: #D81B60;
#         }
#         .subtitle {
#             font-size: 1.2rem;
#             color: #333;
#         }
#         </style>
#         <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/jumbotron1.png?raw=true' class='header-image'/>
#         """,
#         unsafe_allow_html=True,
#     )

# def render_sidebar():
#     """Render the sidebar with language selection."""
#     with st.sidebar:
#         st.markdown(
#             """
#             <div style="text-align: center;">
#                 <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/logo.png?raw=true' class='sidebar-logo'/>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
        
#         # Language selection in the sidebar
#         language = st.selectbox('Choose your language / Pilih bahasa Anda', ['en', 'id'])
#         st.session_state['language'] = language

# def main():
#     set_page_config()
#     render_sidebar()

#     # Get the translation dictionary for the selected language
#     text = translations[st.session_state.get('language', 'en')]
    
#     # Initialize session state variables if not already present
#     if 'logged_in' not in st.session_state:
#         st.session_state['logged_in'] = False
#     if 'username' not in st.session_state:
#         st.session_state['username'] = ''
    

#     if st.session_state['logged_in']:
#         st.write(f"{text['greeting']}{st.session_state['username']}")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown(
#                 f"""
#                 <h1 class='custom-font bold-heading'>
#                     {text['title']}
#                 </h1>
#                 <p class='subtitle custom-font'>{text['subtitle']}</p>
#                 """,
#                 unsafe_allow_html=True
#             )
        
#         with col2:
#             inject_custom_css()
#     else:
#         st.warning(text['login_warning'])
#         st.write(f"[{text['login_link']}](http://localhost:8501/Login)") 

# if __name__ == '__main__':
#     main()

import streamlit as st

# Translations for English and Bahasa Indonesia
translations = {
    'en': {
        'greeting': 'Hello',
        'login_warning': 'You are not logged in. Please log in first.',
        'login_link': 'Click here to login',
        'title': 'Fighting Breast Cancer Takes Everyone',
        'subtitle': 'Cancer may challenge your body but it can never break your spirit.'
    },
    'id': {
        'greeting': 'Halo',
        'login_warning': 'Anda belum masuk. Silakan masuk terlebih dahulu.',
        'login_link': 'Klik di sini untuk masuk',
        'title': 'Melawan Kanker Payudara Membutuhkan Semua Orang',
        'subtitle': 'Kanker mungkin menantang tubuh Anda tetapi tidak bisa menghancurkan semangat Anda.'
    }
}

def set_page_config():
    """Set the initial page configuration."""
    st.set_page_config(
        page_icon="./asset/logo.png",
        page_title="Breast Cancer Analysis",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def inject_custom_css():
    """Inject custom CSS for styling."""
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
        }
        /* Sidebar logo styling */
        .sidebar-logo {
            display: block;
            margin: 0 auto;
            width: 80px;
            height: auto;
        }
        /* Header image */
        .header-image {
            width: 100%;
            height: auto;
            margin-bottom: 20px;
        }
        /* Custom font styling */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        .custom-font {
            font-family: 'Poppins', sans-serif;
            color: #1E1E1E;
        }
        .bold-heading {
            font-weight: 700;
            color: #D81B60;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #333;
        }
        </style>
        <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/jumbotron1.png?raw=true' class='header-image'/>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    """Render the sidebar with language selection."""
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
        language = st.selectbox('Choose your language / Pilih bahasa Anda', ['en', 'id'])
        st.session_state['language'] = language


def main():
    set_page_config()
    render_sidebar()

    # Get the translation dictionary for the selected language
    text = translations[st.session_state.get('language', 'en')]
    
    #Initialize session state variables if not already present
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ''

    # if st.session_state['logged_in']:
    #     st.write(f"{text['greeting']}{st.session_state['username']}")
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <h1 class='custom-font bold-heading'>
                {text['title']}
            </h1>
            <p class='subtitle custom-font'>{text['subtitle']}</p>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        inject_custom_css()
    # else:
    #     st.warning(text['login_warning'])
    #     st.write(f"[{text['login_link']}](http://localhost:8501/Login)") 

    

if __name__ == '__main__':
    main()
