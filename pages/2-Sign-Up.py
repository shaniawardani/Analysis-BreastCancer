import streamlit as st
from supabase import create_client, Client
import bcrypt
import jwt
import datetime
import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# Configure Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")  # Load JWT secret from environment variables

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("SUPABASE_URL or SUPABASE_KEY is not set in .env file or environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Translation dictionary
translations = {
    'en': {
        'signup': 'Sign Up',
        'email': 'Email',
        'username': 'Username',
        'password': 'Password',
        'invalid_email': "Please use an email that ends with '@gmail.com'",
        'create_account_error': 'Error creating account: ',
        'account_created': 'Account created successfully!',
    },
    'id': {
        'signup': 'Daftar',
        'email': 'Email',
        'username': 'Nama Pengguna',
        'password': 'Kata Sandi',
        'invalid_email': "Silakan gunakan email yang diakhiri dengan '@gmail.com'",
        'create_account_error': 'Gagal membuat akun: ',
        'account_created': 'Akun berhasil dibuat!',
    }
}

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

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def is_user_exists(username, email):
    response = supabase.from_('user').select("id").or_(
        f"username.eq.{username},email.eq.{email}"
    ).execute()
    return bool(response.data)

def signup(email, username, password):
    if is_user_exists(username, email):
        return None, "Username or email already exists."
    
    hashed_password = hash_password(password)
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        response = supabase.from_('user').insert({
            'email': email,
            'username': username,
            'password': hashed_password
        }).execute()

        if response.data:
            return response.data, None
        else:
            error_code = response.get("code")
            if error_code == '23505':  # Unique constraint violation
                return None, "Username or email already exists."
            else:
                logging.error(f"Failed to insert user data: {response}")
                return None, "Failed to create account. Please try again later."
    except Exception as e:
        logging.exception("An unexpected error occurred during signup.")
        return None, "An unexpected error occurred. Please try again later."

def signup_form():
    # Use translation based on selected language
    text = translations.get(st.session_state.get('language', 'en'))

    st.title(text['signup'])
    email = st.text_input(text['email'])
    username = st.text_input(text['username'])
    password = st.text_input(text['password'], type="password")

    if email and not email.endswith("@gmail.com"):
        st.error(text['invalid_email'])
    elif st.button(text['signup']):
        data, error = signup(email, username, password)
        if error:
            st.error(f"{text['create_account_error']}{error}")
        else:
            st.success(text['account_created'])
            st.markdown(
                "<meta http-equiv='refresh' content='0; url=/Login'>",
                unsafe_allow_html=True
            )

def main():
    inject_custom_css()
    render_sidebar()
    signup_form()

if __name__ == '__main__':
    main()
