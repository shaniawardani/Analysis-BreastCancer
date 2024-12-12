import streamlit as st
from supabase import create_client, Client
import bcrypt
import os
import re
import datetime
import jwt
from dotenv import load_dotenv


load_dotenv()

# Configure Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")  # Load JWT secret from environment variables

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL or SUPABASE_KEY is not set in .env file or environment variables.")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Generate a token
def generate_token(email):
    return jwt.encode({
        'user_id': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm="HS256")

# Decode a token
def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Refresh token expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid refresh token"}, 401

def set_page_config():
    """Set the initial page configuration."""
    st.set_page_config(
        page_icon="",
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
            background-color: #FFFFFF;
        }
        /* Styling for the sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFB3D9;
            color: white;
        }
        /* Center the form container */
        .form-container {
            max-width: 400px;
            margin: auto;
            padding: 40px;
            background-color: #FFFFFF;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        /* Styling for the form title */
        .form-title {
            font-size: 2rem;
            color: #8A2C52;
            font-weight: bold;
            margin-bottom: 20px;
            font-family: 'Poppins', sans-serif;
        }

        /* Input field styling */
        .stTextInput > div > div > input {
            width: 100%;
            padding: 12px;
            padding-left: 10px;
            border-radius: 8px;
            font-size: 1rem;
            border: 1px solid #E0E0E0;
            background-color: #F7F9FC;
            color: #333333;
            margin-bottom: 20px;
        }

        /* Button styling */
        .stButton > button {
            background-color: #A65277;
            color: white;
            font-size: 1rem;
            font-weight: bold;
            padding: 12px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            width: 100%;
        }

        /* Hover effect for button */
        .stButton > button:hover {
            background-color: #C2185B;
        }

        /* Link styling for additional actions */
        .footer-text {
            color: #333;
            font-size: 0.9rem;
            margin-top: 20px;
        }

        .footer-text a {
            color: #8A2C52;
            text-decoration: none;
            font-weight: bold;
        }

        .footer-text a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

translations = {
    'en': {
        'login': 'Login',
        'email': 'Email',
        'password': 'Password',
        'invalid_email': 'Invalid email format. Please enter a valid email address.',
        'login_success': 'Login successful!',
        'invalid_credentials': 'Invalid email or password',
        'welcome': 'Welcome, ',
    },
    'id': {
        'login': 'Masuk',
        'email': 'Email',
        'password': 'Kata Sandi',
        'invalid_email': 'Format email tidak valid. Silakan masukkan alamat email yang valid.',
        'login_success': 'Masuk berhasil!',
        'invalid_credentials': 'Email atau kata sandi salah',
        'welcome': 'Selamat datang, ',
    }
}

def render_sidebar():
    """Render the sidebar with navigation."""
    with st.sidebar:
        st.markdown(
           """
            <div style="text-align: center;">
                <img src='https://github.com/shaniawardani/Breast-Cancer-/blob/main/asset/logo.png?raw=true' class='sidebar-logo'/>
            </div>
            """, unsafe_allow_html=True
        )
        # Language selection in the sidebar
        language = st.selectbox('Language/Bahasa', ['en', 'id'])
        st.session_state['language'] = language


def is_valid_email(email):
    # Define a regex pattern for validating an email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    return False

def login_form():
    st.title(translations[st.session_state.get('language', 'en')]['login'])
    email = st.text_input(translations[st.session_state.get('language', 'en')]['email'])
    password = st.text_input(translations[st.session_state.get('language', 'en')]['password'], type="password")

    # Email validation
    if email and not is_valid_email(email):
        st.error(translations[st.session_state.get('language', 'en')]['invalid_email'])

    if st.button(translations[st.session_state.get('language', 'en')]['login']):
        if login(email, password):
            st.session_state['logged_in'] = True  
            st.session_state['email'] = email 
            st.success(translations[st.session_state.get('language', 'en')]['login_success'])
            st.switch_page("pages/3-Analysis.py")
        else:
            st.error(translations[st.session_state.get('language', 'en')]['invalid_credentials'])

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login(email, password):
    response = supabase.from_('user').select("*").eq("email", email).execute()
    if response.data:
        user = response.data[0]
        if verify_password(password, user['password']):
            st.session_state['username'] = user['username']
            return True
            
    return False

def main():
    inject_custom_css()
    render_sidebar()
    
    # Get the translation dictionary for the selected language
    text = translations[st.session_state.get('language', 'en')]

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.write(f"{text['welcome']}{st.session_state['username']}!")
    else:
        st.write()
        login_form()

if __name__ == '__main__':
    main()
