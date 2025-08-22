import streamlit as st

def show_login(api_client):
    """Show login and signup forms with account deletion"""
    # CodVid.AI Branding Header
    st.markdown('<h1 class="brand-title">CodVid.AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Premium Instagram Analytics & AI Insights</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Create tabs for login and signup
    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Delete Account"])
    
    with tab1:
        st.markdown('<h2 class="main-header">Login</h2>', unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if email and password:
                    with st.spinner("Logging in..."):
                        if api_client.login(email, password):
                            # Persist session token for next run cycle
                            st.session_state.session_token = api_client.session_token
                            st.session_state.authenticated = True
                            st.session_state.current_page = 'dashboard'
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Login failed. Please check your credentials.")
                else:
                    st.error("Please fill in all fields.")
    
    with tab2:
        st.markdown('<h2 class="main-header">Sign Up</h2>', unsafe_allow_html=True)
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email", placeholder="your@email.com")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if email and password:
                    if password == confirm_password:
                        with st.spinner("Creating account..."):
                            if api_client.signup(email, password):
                                st.success("Account created successfully! You can now login.")
                            else:
                                st.error("Failed to create account. Email might already be in use.")
                    else:
                        st.error("Passwords do not match.")
                else:
                    st.error("Please fill in all fields.")
    
    with tab3:
        st.markdown('<h2 class="main-header">Delete Account</h2>', unsafe_allow_html=True)
        st.warning("""
        **WARNING**: This will permanently delete your account and ALL associated data, including:
        • Instagram tracking tasks
        • Projects and chat history
        • All analytics data
        • This action CANNOT be undone!
        """)
        
        with st.form("delete_account_form"):
            st.markdown("**First Confirmation:**")
            confirm1 = st.text_input("Type 'DELETE' to continue", key="delete_confirm1")
            
            st.markdown("**Second Confirmation:**")
            email_confirm = st.text_input("Enter your email to confirm", key="delete_email")
            
            submit_delete = st.form_submit_button("🗑️ Delete Account")
            
            if submit_delete:
                if confirm1 == 'DELETE' and email_confirm:
                    with st.spinner("Deleting account..."):
                        if api_client.delete_account():
                            st.success("✅ Account successfully deleted!")
                            st.session_state.authenticated = False
                            st.session_state.session_token = None
                            st.info("All data has been removed. You can create a new account anytime.")
                        else:
                            st.error("❌ Failed to delete account. Please try again or contact support.")
                else:
                    st.error("❌ Confirmation failed. Please type 'DELETE' and enter your email correctly.") 