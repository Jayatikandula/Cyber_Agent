import streamlit as st
from database import create_users_table, add_user, verify_user

create_users_table()

def auth_page():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "organization" not in st.session_state:
        st.session_state.organization = None

    if st.session_state.authenticated:
        return True

    st.title("🛡 CyberGuard AI")
    st.caption("Enterprise Threat Intelligence Platform")

    option = st.radio("Select Option", ["Login", "Signup"], horizontal=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        organization = st.text_input("Organization Name")

        if st.button("Create Account", use_container_width=True):
            if add_user(username, password, organization):
                st.success("Account created successfully")
            else:
                st.error("Username already exists")

    if option == "Login":
        if st.button("Login", use_container_width=True):
            user = verify_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user[1]
                st.session_state.role = user[3]
                st.session_state.organization = user[4]
                st.rerun()
            else:
                st.error("Invalid credentials")

    return False