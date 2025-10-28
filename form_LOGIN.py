import streamlit as st
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header
from user_interface.utils.DB import UserRepository
from observer_pattern import Subject, StreamlitNotifier, LoginLogger


# ===== Configuração da Página =====
st.set_page_config(page_title="Login System", page_icon="🔐", layout="centered")

db = UserRepository()

# ===== Funções =====
def go_to_signup():
    st.session_state.page = "signup"
    st.rerun()
def go_to_login():
    st.session_state.page = "login"
    st.rerun()

login_subject = Subject()

# Adicionar observadores
login_subject = Subject()
login_subject.add_observer(LoginLogger())
login_subject.add_observer(StreamlitNotifier())

def validate_login(username, password):
    if not username or not password:
        st.error("⚠ Please fill all fields.")
        return

    user_data = db.validar_login(username, password)
    if user_data:
        st.session_state["user_id"] = user_data["user_id"]
        st.session_state["username"] = user_data["username"]

        st.success(f"✅ Welcome, {user_data['username']}!")
    
        # 🔔 Notifica os observadores
        login_subject.notify_observers(f"User '{username}' logged in successfully!", success=True)

        st.session_state.page = "begin"
        st.rerun()
    else:
        st.error("❌ Invalid username or password.")
        # 🔔 Notifica os observadores do erro
        login_subject.notify_observers(f"Failed login attempt for username: {username}", success=False)



def validate_signup(username, email, password, confirm):
    if not username or not email or not password or not confirm:
        st.error("⚠ Please fill all fields.")
        return
    
    success = db.validar_signup(username, email, password, confirm)
    
    if success:
        st.success("✅ Account created successfully! You can now log in.")
        go_to_login()
    else:

        pass


def login():
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
    
def register():
     # ===== Tela de Cadastro =====
    with st.container():
        colored_header("🆕 Create Account", description="Join us today", color_name="green-70")
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            username = st.text_input("👤 Full Name")
            email = st.text_input("📧 Email")
            password = st.text_input("🔑 Password", type="password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password")
            register_btn = st.button("Register", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if register_btn:
                validate_signup(username, email, password, confirm_password)

        st.markdown("---")
        st.write("Already have an account?")
        st.button("Back to Login", on_click=go_to_login, type="secondary", use_container_width=True)