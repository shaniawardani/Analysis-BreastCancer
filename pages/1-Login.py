import streamlit as st
from supabase import create_client, Client
import bcrypt
import re

# Configure Supabase
SUPABASE_URL = 'https://mylvpdlslvkpuhepzjpw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15bHZwZGxzbHZrcHVoZXB6anB3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMDk3NzkxNSwiZXhwIjoyMDQ2NTUzOTE1fQ.iwA7KbFFy-foQ8QJ-lZu6ylzMMiIElvesVpZsKaB4Tk'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        language = st.selectbox('Choose your language / Pilih bahasa Anda', ['en', 'id'])
        st.session_state['language'] = language


# def authenticate_user(email, password):
#     """Authenticate the user with Firebase."""
#     try:
#         user = auth.get_user_by_email(email)
#         st.success("Login Successful!")
#         return True
#     except firebase_admin.exceptions.FirebaseError as e:
#         st.error(f"Authentication failed: {e}")
#         return False

# def login_form():
#     st.title("Login")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if authenticate_user(email, password):
#             st.session_state['logged_in'] = True
#             st.session_state['email'] = email
#         else:
#             st.error("Authentication failed! Please check your email and password.")

def is_valid_email(email):
    # Define a regex pattern for validating an email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    return False

def login_form():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Email validation
    if email and not is_valid_email(email):
        st.error("Invalid email format. Please enter a valid email address.")

    if st.button("Login"):
        if login(email, password):
            st.session_state['logged_in'] = True  
            st.session_state['email'] = email 
            st.success("Login successful!")
            st.switch_page("pages/3-Analysis.py")
        else:
            st.error("Invalid email or password")


# # JWT secret
# JWT_SECRET = "your_jwt_secret_here"  # Replace with an actual secret, or load from environment variables

# # Generate a token
# def generate_token(user_id):
#     return jwt.encode({
#         'user_id': user_id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
#     }, JWT_SECRET, algorithm="HS256")

# # Decode a token
# def decode_token(token):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         return payload
#     except jwt.ExpiredSignatureError:
#         return None  # Token expired
#     except jwt.InvalidTokenError:
#         return None  # Invalid token

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

def logout():
    """Log out the user by clearing session state."""
    del st.session_state['logged_in']
    del st.session_state['username']
    del st.session_state['email']
    st.success("You have been logged out!")

def main():
    inject_custom_css()
    render_sidebar()

    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        #st.write("Welcome to the dashboard!")
        st.write(f"Welcome, {st.session_state['username']}!")

         # Add a logout button
        if st.button("Log Out"):
            logout()
            st.session_state['logged_in'] = False  # Set to False so it will show login form again
            #st.rerun()  # Refresh the app to go back to login form
            st.switch_page("Dashboard.py")
    else:        
        login_form()

if __name__ == '__main__':
    main()