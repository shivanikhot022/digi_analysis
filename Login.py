# Import packages
import streamlit as st
import base64
import os

# Page configuration
st.set_page_config(page_title="Login", layout="centered")


# Function to set background image
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        /* Full page background image */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* Transparent top header */
        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}

        /* Labels */
        label {{
            color: black !important;
            font-size: 24px !important;
            font-weight: bold !important;
        }}

        /* Warning / error / success messages */
        [data-testid="stAlert"] {{
            font-size: 18px !important;
            font-weight: bold !important;
        }}

        /* Expander white background */
        [data-testid="stExpander"] {{
            background-color: white !important;
            border: 2px solid black !important;
            border-radius: 10px !important;
            padding: 5px !important;
        }}

        /* Expander heading */
        [data-testid="stExpander"] summary {{
            color: black !important;
            font-size: 17px !important;
            font-weight: bold !important;
        }}

        /* Expander inside text */
        [data-testid="stExpander"] p,
        [data-testid="stExpander"] div {{
            color: black !important;
            font-size: 16px !important;
            font-weight: bold !important;
        }}

        /* Login button */
        div.stButton > button {{
            width: 100%;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# Image path
base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets", "teady1.jpeg")

# Apply background image
set_bg(image_path)


# Title
st.markdown(
    "<h1 style='text-align:center; color:black;'>🧸 Digital Analytics Login</h1>",
    unsafe_allow_html=True
)


# Demo credentials expander
with st.expander("Demo Credentials (For Reviewer Access)", expanded=False):
    st.markdown("""
    **Email:** admin@gmail.com  
    **Password:** scalar@123
    """)


# Login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Login inputs
email = st.text_input("Email ID")
password = st.text_input("Password", type="password")


# Login button logic
if st.button("Login"):
    if email == "admin@gmail.com" and password == "scalar@123":
        st.session_state.logged_in = True
        st.success("Login Successful ✅")
        st.switch_page("pages/1_CEO.py")
    else:
        st.error("Invalid Email or Password ❌")