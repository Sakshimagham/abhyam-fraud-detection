# auth.py - Authentication module for all language pages
import streamlit as st
import random
import string
import hashlib
import json
import os
from datetime import datetime

# File path for storing users (simple JSON database)
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

# Initialize users file if it doesn't exist
def init_users_file():
    if not os.path.exists(USERS_FILE):
        default_users = {
            "sakshi": {
                "password_hash": hashlib.sha256("sakshi123".encode()).hexdigest(),
                "email": "sakshi@example.com",
                "security_question": "What is your pet name?",
                "security_answer_hash": hashlib.sha256("tommy".encode()).hexdigest(),
                "created_at": datetime.now().isoformat()
            }
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)

# Load users from file
def load_users():
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Generate reset code
def generate_reset_code():
    return ''.join(random.choices(string.digits, k=6))

# Initialize session state
def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'show_forgot_password' not in st.session_state:
        st.session_state.show_forgot_password = False
    if 'reset_step' not in st.session_state:
        st.session_state.reset_step = 1
    if 'reset_code' not in st.session_state:
        st.session_state.reset_code = ''
    if 'reset_username' not in st.session_state:
        st.session_state.reset_username = ''

# Login form
def show_login_form(texts):
    users = load_users()
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🔐 Login", use_container_width=True)
        with col2:
            forgot = st.form_submit_button("❓ Forgot Password", use_container_width=True)
        
        if submit:
            if username in users and users[username]['password_hash'] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password!")
        
        if forgot:
            st.session_state.show_forgot_password = True
            st.session_state.reset_step = 1
            st.rerun()

# Forgot password form
def show_forgot_password_form(texts):
    users = load_users()
    
    st.markdown("---")
    st.markdown("### 🔐 Forgot Password")
    
    if st.session_state.reset_step == 1:
        reset_username = st.text_input("Enter your username")
        if st.button("Next", use_container_width=True):
            if reset_username in users:
                st.session_state.reset_username = reset_username
                st.session_state.reset_step = 2
                st.rerun()
            else:
                st.error("Username not found!")
    
    elif st.session_state.reset_step == 2:
        user_data = users[st.session_state.reset_username]
        st.write(f"**Security Question:** {user_data['security_question']}")
        answer = st.text_input("Your answer", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Verify", use_container_width=True):
                if hash_password(answer.lower()) == user_data['security_answer_hash']:
                    reset_code = generate_reset_code()
                    st.session_state.reset_code = reset_code
                    st.session_state.reset_step = 3
                    st.info(f"Reset code sent to your email: {user_data['email']}")
                    st.code(f"Demo Code: {reset_code}", language="text")
                    st.rerun()
                else:
                    st.error("Incorrect answer!")
        with col2:
            if st.button("Back", use_container_width=True):
                st.session_state.reset_step = 1
                st.rerun()
    
    elif st.session_state.reset_step == 3:
        code = st.text_input("Enter 6-digit reset code", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reset Password", use_container_width=True):
                if code == st.session_state.reset_code:
                    if new_password == confirm_password and new_password:
                        # Update password
                        users[st.session_state.reset_username]['password_hash'] = hash_password(new_password)
                        save_users(users)
                        st.success("Password reset successfully! Please login.")
                        st.session_state.show_forgot_password = False
                        st.session_state.reset_step = 1
                        st.rerun()
                    else:
                        st.error("Passwords don't match or are empty!")
                else:
                    st.error("Invalid reset code!")
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_forgot_password = False
                st.session_state.reset_step = 1
                st.rerun()
    
    if st.button("← Back to Login"):
        st.session_state.show_forgot_password = False
        st.rerun()

# Registration form
def show_register_form(texts):
    users = load_users()
    
    with st.expander("📝 New User? Register Here"):
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_email = st.text_input("Email")
            security_q = st.text_input("Security Question (e.g., What is your pet name?)")
            security_a = st.text_input("Security Answer")
            
            if st.form_submit_button("Register"):
                if new_username and new_password and new_email and security_q and security_a:
                    if new_password == confirm_password:
                        if new_username not in users:
                            users[new_username] = {
                                "password_hash": hash_password(new_password),
                                "email": new_email,
                                "security_question": security_q,
                                "security_answer_hash": hash_password(security_a.lower()),
                                "created_at": datetime.now().isoformat()
                            }
                            save_users(users)
                            st.success("Registration successful! Please login.")
                        else:
                            st.error("Username already exists!")
                    else:
                        st.error("Passwords don't match!")
                else:
                    st.error("Please fill all fields!")

# Logged in user display
def show_logged_in_user(texts):
    st.success(f"✅ Logged in as **{st.session_state.username}**")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ''
            st.rerun()
    
    st.markdown("---")

# Main authentication sidebar function
def auth_sidebar(texts):
    init_session()
    
    st.markdown(f"### {texts.get('login', '🔐 Login / Username')}")
    
    if not st.session_state.logged_in:
        show_login_form(texts)
        
        if st.session_state.show_forgot_password:
            show_forgot_password_form(texts)
        
        show_register_form(texts)
    else:
        show_logged_in_user(texts)
    
    return st.session_state.logged_in, st.session_state.username

# Helper function to get login status
def is_logged_in():
    init_session()
    return st.session_state.logged_in

def get_current_user():
    init_session()
    return st.session_state.username if st.session_state.logged_in else None