import streamlit as st
from datetime import datetime

def smart_task_selector(api_client, auto_select_first=False):
    """
    Smart task selection that can auto-select or prompt user to choose
    Based on the notebook functionality
    """
    tasks = api_client.get_tracking_tasks()
    if not tasks or len(tasks) == 0:
        st.error("No tasks found on server.")
        return None
    
    # Auto-select if only one task and auto_select_first is True
    if len(tasks) == 1 and auto_select_first:
        task = tasks[0]
        task_id = task.get('_id')
        profile = task.get('target_profile', 'unknown')
        ttype = 'Competitor' if task.get('is_competitor') else 'Own Profile'
        st.success(f"Auto-selected only available task: @{profile} ({ttype})")
        return task_id
    
    # Show available tasks
    st.markdown('<h4 class="main-header">Select a task from server:</h4>', unsafe_allow_html=True)
    st.markdown("---")
    
    task_options = {}
    for idx, task in enumerate(tasks):
        profile = task.get('target_profile', 'unknown')
        ttype = 'Competitor' if task.get('is_competitor') else 'Own Profile'
        status = task.get('status', 'unknown')
        last_scraped = task.get('last_scraped', 'Never')
        
        option_key = f"{idx+1}. @{profile} ({ttype})"
        task_options[option_key] = task['_id']
        
        st.markdown(f"**{option_key}**")
        st.caption(f"Status: {status}, Last scraped: {last_scraped}")
    
    # Get user selection
    selected_option = st.selectbox(
        f"Select task number (1-{len(tasks)}):",
        options=list(task_options.keys()),
        index=None,
        placeholder="Choose a task..."
    )
    
    if selected_option:
        task_id = task_options[selected_option]
        profile = selected_option.split('. ')[1].split(' (')[0]
        st.success(f"Selected: @{profile} (ID: {task_id})")
        return task_id
    
    return None

def show_dashboard(api_client):
    """Show main dashboard with Instagram tracking tasks"""
    st.markdown('<h1 class="brand-title">CodVid.AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Instagram Analytics Dashboard</p>', unsafe_allow_html=True)
    
    # Get tracking tasks and user profile
    tasks = api_client.get_tracking_tasks()
    
    # Top section with user profile (left) and action buttons (right) - PERMANENT LAYOUT
    col1, col2 = st.columns([2, 1], gap="medium")
    
    with col1:
        # Your Profile Section (Left)
        st.markdown('<h3 class="main-header">Your Profile</h3>', unsafe_allow_html=True)
        
        # Find user's own profile
        own_profile = None
        if tasks:
            own_profile = next((task for task in tasks if not task.get('is_competitor')), None)
        
        if own_profile:
            st.markdown(f"**Username:** @{own_profile['target_profile']}")
            st.markdown(f"**Status:** {own_profile.get('status', 'Active')}")
            if own_profile.get('last_scraped'):
                from datetime import datetime
                last_scraped = datetime.fromtimestamp(own_profile['last_scraped'])
                st.markdown(f"**Last Updated:** {last_scraped.strftime('%Y-%m-%d %H:%M')}")
            else:
                st.markdown("**Last Updated:** Never")
            
            # Add View Details and Delete buttons for own profile
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("View Details", key="view_own_profile", use_container_width=True):
                    st.session_state.current_profile = own_profile
                    st.session_state.current_page = 'profile_details'
                    st.rerun()
            with col_btn2:
                if st.button("Delete Task", key="delete_own_profile", use_container_width=True):
                    if api_client.delete_tracking_task(own_profile['_id']):
                        st.success("Own profile task deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete own profile task")
        else:
            st.info("No own profile found. Create one below.")
    
    with col2:
        # Quick Actions Section (Right)
        st.markdown('<h3 class="main-header">Quick Actions</h3>', unsafe_allow_html=True)
        
        # Button 1: Project Chat
        if st.button("Project Chat", use_container_width=True, key="quick_chat"):
            # Get projects and go directly to the latest one
            projects = api_client.get_project_list()
            if projects:
                # Use the last project as the latest (most recently created)
                latest_project = projects[-1]
                
                # Ensure project data is loaded into cache before navigating
                if api_client.ensure_project_loaded(latest_project):
                    st.session_state.current_project = latest_project
                    st.session_state.current_page = 'project_chat'
                    st.rerun()
                else:
                    st.error(f"Failed to load project data for '{latest_project}'. Please try again.")
            else:
                st.error("No projects found. Please create a project first.")
        
        # Button 2: Add Task
        if st.button("Add Task", use_container_width=True, key="quick_add"):
            st.session_state.show_add_task = True
            st.rerun()
        
        # Button 3: Logout
        if st.button("Logout", use_container_width=True, key="quick_logout"):
            st.session_state.authenticated = False
            st.session_state.session_token = None
            st.session_state.current_page = 'login'
            st.rerun()
    
                # Show add task form directly under Quick Actions if requested
        if st.session_state.get('show_add_task', False):
            st.markdown("---")
            st.markdown('<h4 class="main-header">Create New Tracking Task</h4>', unsafe_allow_html=True)
            with st.form("create_task_form"):
                profile_name = st.text_input("Instagram Username", placeholder="e.g., foodxtaste")
                is_competitor = st.checkbox("Track as Competitor (uncheck for Own Profile)")
                
                # Add scraping interval settings
                st.markdown('<h5 class="main-header">Scraping Settings</h5>', unsafe_allow_html=True)
                scrape_interval = st.number_input(
                    "Scrape Interval (days)", 
                    min_value=0.5, 
                    max_value=30.0, 
                    value=2.0,
                    step=0.5,
                    help="How often to automatically scrape this profile (0.5 = 12 hours, 1 = daily, 7 = weekly)"
                )
                
                st.caption(f"Profile will be scraped every {scrape_interval} days")
                
                col_submit, col_cancel = st.columns(2)
                with col_submit:
                    submit = st.form_submit_button("Create Task", use_container_width=True)
                with col_cancel:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_add_task = False
                        st.rerun()
                
                if submit:
                    if profile_name:
                        task_id = api_client.create_tracking_task(profile_name, is_competitor)
                        if task_id:
                            # Update the scrape interval after creation
                            if api_client.update_scrape_interval(task_id, scrape_interval):
                                st.success(f"Created tracking task for @{profile_name} with {scrape_interval}-day interval")
                            else:
                                st.success(f"Created tracking task for @{profile_name} (using default interval)")
                            st.session_state.show_add_task = False
                            st.rerun()
                        else:
                            st.error("Failed to create tracking task")
                    else:
                        st.error("Please enter a profile name")
        
        st.markdown("---")
        
    # Environment selector (based on notebooks)
    st.sidebar.subheader("Environment Settings")
    from config import Config
    current_env = Config.get_environment()
    new_env = st.sidebar.selectbox(
        "API Environment:",
        options=["development", "local", "production", "betamale"],
        index=["development", "local", "production", "betamale"].index(current_env) if current_env in ["development", "local", "production", "betamale"] else 0
    )
    
    if new_env != current_env:
        if st.sidebar.button("Update Environment"):
            Config.set_environment(new_env)
            st.sidebar.success(f"Environment updated to: {new_env}")
            st.rerun()
    
    st.sidebar.markdown(f"**Current API:** {Config.get_api_url()}")
    
    # Competitor Profiles Grid
    if tasks:
        competitor_profiles = [task for task in tasks if task.get('is_competitor', False)]
        if competitor_profiles:
            st.markdown('<h2 class="main-header">Competitor Profiles</h2>', unsafe_allow_html=True)
            
            # Create 2-column grid for competitor profiles
            cols = st.columns(2)
            for idx, task in enumerate(competitor_profiles):
                col_idx = idx % 2
                with cols[col_idx]:
                    # Create detailed profile card
                    with st.container():
                        st.markdown(f"**@{task['target_profile']}**")
                        st.caption(f"Status: {task.get('status', 'Active')}")
                        
                        if task.get('last_scraped'):
                            last_scraped = datetime.fromtimestamp(task['last_scraped'])
                            st.caption(f"Last Updated: {last_scraped.strftime('%Y-%m-%d %H:%M')}")
                        else:
                            st.caption("Last Updated: Never")
                        
                        # Add View Details and Delete buttons
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button(
                                "View Details", 
                                key=f"profile_{task['_id']}", 
                                use_container_width=True,
                                help=f"Click to view analytics for @{task['target_profile']}"
                            ):
                                # Handle click to view profile details
                                st.session_state.current_profile = task
                                st.session_state.current_page = 'profile_details'
                                st.rerun()
                        
                        with col_btn2:
                            if st.button(
                                "Delete Task", 
                                key=f"delete_profile_{task['_id']}", 
                                use_container_width=True,
                                help=f"Delete tracking task for @{task['target_profile']}"
                            ):
                                if api_client.delete_tracking_task(task['_id']):
                                    st.success(f"Deleted tracking task for @{task['target_profile']}")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to delete tracking task for @{task['target_profile']}")
                        
                        st.markdown("---")
            
            st.markdown("---")
    
    # Add task form is now shown directly under Quick Actions section 