import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header



# ===== Configuração da Página =====
st.set_page_config(page_title="Login System", page_icon="🔐", layout="centered")

# ===== Estado Inicial =====
if "page" not in st.session_state:
    st.session_state.page = "login"

# ===== Funções =====
def go_to_signup():
    st.session_state.page = "signup"

def go_to_login():
    st.session_state.page = "login"

def validate_login(user, pwd):
    if not user or not pwd:
        st.error("⚠ Please fill all fields.")
    elif user == "admin" and pwd == "123":
        st.success("✅ Login successful!")
        rain(emoji="🎉", font_size=54, falling_speed=5, animation_length="infinite")
    else:
        st.error("❌ Invalid username or password.")

def validate_signup(name, email, pwd, confirm):
    if not name or not email or not pwd or not confirm:
        st.error("⚠ Please fill all fields.")
    elif pwd != confirm:
        st.error("❌ Passwords do not match.")
    else:
        st.success("✅ Account created successfully! You can now log in.")
        go_to_login()

# ===== Tela de Login =====
if st.session_state.page == "login":
    with st.container():
        colored_header("🔐 Sign In", description="Access your account", color_name="blue-70")
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            login_btn = st.button("Login", type="primary", use_container_width=True)
            st.link_button("Continue with Google", "https://accounts.google.com/signin", type="secondary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if login_btn:
                validate_login(username, password)

        st.markdown("---")
        st.write("Don't have an account?")
        st.button("Create an Account", on_click=go_to_signup, type="secondary", use_container_width=True)

# ===== Tela de Cadastro =====
elif st.session_state.page == "signup":
    with st.container():
        colored_header("🆕 Create Account", description="Join us today", color_name="green-70")
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            name = st.text_input("👤 Full Name")
            email = st.text_input("📧 Email")
            password = st.text_input("🔑 Password", type="password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password")
            register_btn = st.button("Register", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if register_btn:
                validate_signup(name, email, password, confirm_password)

        st.markdown("---")
        st.write("Already have an account?")
        st.button("Back to Login", on_click=go_to_login, type="secondary", use_container_width=True)
