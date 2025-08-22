import streamlit as st

def show_projects_page(api_client):
    """Show projects page with chat, reel tracking, and project management
    
    Features:
    - Create new projects
    - View existing projects
    - Access project chat and tracker
    - Delete individual projects (with confirmation)
    - Bulk delete multiple projects (with safety checks)
    - Active project protection (cannot be deleted while active)
    """
    st.markdown('<h1 class="brand-title">Projects</h1>', unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    with col2:
        if st.button("Projects", use_container_width=True, disabled=True):
            pass
    with col3:
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.session_token = None
            st.session_state.current_page = 'login'
            st.rerun()
    
    st.markdown("---")
    
    # Get projects
    projects = api_client.get_project_list()
    
    # Create new project
    st.markdown('<h2 class="main-header">Create New Project</h2>', unsafe_allow_html=True)
    with st.expander("Add New Project", expanded=False):
        with st.form("create_project_form"):
            project_name = st.text_input("Project Name", placeholder="Enter project name")
            submit = st.form_submit_button("Create Project")
            
            if submit:
                if project_name:
                    if api_client.create_project(project_name):
                        st.success(f"✅ Created project: {project_name}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to create project")
                else:
                    st.error("Please enter a project name")
    
    # Display projects
    st.markdown('<h2 class="main-header">Your Projects</h2>', unsafe_allow_html=True)
    
    if not projects:
        st.info("No projects found. Create your first project above!")
    else:
        # Bulk delete option
        with st.expander("Bulk Delete Projects", expanded=False):
            st.warning("**Danger Zone**: This will permanently delete selected projects and all their data!")
            st.info("**What gets deleted:** All project data, chat history, tracking tasks, and analytics will be permanently removed.")
            
            # Filter out the currently active project from bulk delete options
            current_project = st.session_state.current_project
            deletable_projects = [p for p in projects if p != current_project]
            
            if current_project:
                st.info(f"**{current_project}** is currently active and cannot be deleted")
            
            selected_projects = st.multiselect(
                "Select projects to delete:",
                deletable_projects,
                help="Choose the projects you want to delete (active project is excluded)"
            )
            
            if selected_projects:
                st.error(f"You are about to delete {len(selected_projects)} project(s): {', '.join(selected_projects)}")
                col_bulk1, col_bulk2 = st.columns(2)
                with col_bulk1:
                    if st.button("Delete Selected", type="primary", key="bulk_delete"):
                        st.info(f"Deleting {len(selected_projects)} project(s)...")
                        success_count = 0
                        failed_count = 0
                        for project in selected_projects:
                            st.write(f"Deleting project: {project}")
                            if api_client.delete_project(project):
                                success_count += 1
                                st.write(f"Successfully deleted: {project}")
                                # Remove from local cache if it exists
                                try:
                                    if project in st.session_state.local_user_data.get("projects", {}):
                                        del st.session_state.local_user_data["projects"][project]
                                except Exception:
                                    pass
                            else:
                                failed_count += 1
                                st.write(f"Failed to delete: {project}")
                        
                        if failed_count == 0:
                            st.success(f"Successfully deleted {success_count} project(s)!")
                        else:
                            st.warning(f"Deleted {success_count} project(s), failed to delete {failed_count} project(s)")
                        st.rerun()
                with col_bulk2:
                    if st.button("Cancel", key="bulk_cancel"):
                        st.rerun()
        
        st.markdown("---")
        
        for project in projects:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.markdown(f"**{project}**")
                with col2:
                    if st.button("Chat", key=f"chat_{project}"):
                        st.session_state.current_project = project
                        # Ensure project loaded in cache for chat view
                        api_client.ensure_project_loaded(project)
                        st.session_state.current_page = 'project_chat'
                        st.rerun()
                with col3:
                    if st.button("Tracker", key=f"tracker_{project}"):
                        st.session_state.current_project = project
                        st.session_state.current_page = 'project_tracker'
                        st.rerun()
                with col4:
                    # Check if this project is currently active
                    is_active = st.session_state.current_project == project
                    delete_disabled = is_active
                    
                    if delete_disabled:
                        st.info("Active")
                    else:
                        # Use session state to track delete confirmation
                        delete_key = f"delete_confirm_{project}"
                        if delete_key not in st.session_state:
                            st.session_state[delete_key] = False
                        
                        if not st.session_state[delete_key]:
                            if st.button("Delete", key=f"delete_{project}", type="secondary"):
                                st.session_state[delete_key] = True
                                st.rerun()
                        else:
                            # Show confirmation dialog
                            st.warning(f"Are you sure you want to delete project '{project}'? This action cannot be undone!")
                            col_confirm1, col_confirm2 = st.columns(2)
                            with col_confirm1:
                                if st.button("Yes, Delete", key=f"confirm_delete_{project}", type="primary"):
                                    st.info(f"Deleting project '{project}'...")
                                    if api_client.delete_project(project):
                                        st.success(f"Project '{project}' deleted successfully!")
                                        # Remove from local cache if it exists
                                        try:
                                            if project in st.session_state.local_user_data.get("projects", {}):
                                                del st.session_state.local_user_data["projects"][project]
                                        except Exception:
                                            pass
                                        # Clear the delete confirmation state
                                        if delete_key in st.session_state:
                                            del st.session_state[delete_key]
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to delete project '{project}'")
                                        st.session_state[delete_key] = False
                                        st.rerun()
                            with col_confirm2:
                                if st.button("Cancel", key=f"cancel_delete_{project}"):
                                    st.session_state[delete_key] = False
                                    st.rerun() 