import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime

def show_project_tracker(api_client):
    """Show project reel tracking interface"""
    if not st.session_state.current_project:
        st.error("No project selected")
        st.button("Back to Projects", on_click=lambda: setattr(st.session_state, 'current_page', 'projects'))
        return
    
    project = st.session_state.current_project
    
    # Project selector and navigation tabs at the top
    st.markdown('<h1 class="brand-title">Project Tracker</h1>', unsafe_allow_html=True)
    
    # Project selector and navigation
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        # Project dropdown selector
        projects = api_client.get_project_list()
        if projects:
            current_project_idx = projects.index(project) if project in projects else 0
            selected_project = st.selectbox(
                "Select Project:",
                options=projects,
                index=current_project_idx,
                key="project_selector_tracker"
            )
            if selected_project != project:
                st.session_state.current_project = selected_project
                st.rerun()
    
    with col2:
        if st.button("Chat", use_container_width=True):
            st.session_state.current_page = 'project_chat'
            st.rerun()
    
    with col3:
        if st.button("Tracker", use_container_width=True, disabled=True):
            pass  # Current tab
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back to Projects"):
            st.session_state.current_page = 'projects'
            st.rerun()
    with col2:
        # Use session state to track delete confirmation
        if "delete_confirm_tracker" not in st.session_state:
            st.session_state["delete_confirm_tracker"] = False
        
        if not st.session_state["delete_confirm_tracker"]:
            if st.button("Delete Project", type="secondary"):
                st.session_state["delete_confirm_tracker"] = True
                st.rerun()
        else:
            # Show confirmation dialog
            st.warning(f"Are you sure you want to delete project '{project}'? This action cannot be undone!")
            col_confirm1, col_confirm2 = st.columns(2)
            with col_confirm1:
                if st.button("Yes, Delete", key="confirm_delete_tracker"):
                    st.info(f"Deleting project '{project}'...")
                    if api_client.delete_project(project):
                        st.success(f"Project '{project}' deleted successfully!")
                        # Remove from local cache if it exists
                        try:
                            if project in st.session_state.local_user_data.get("projects", {}):
                                del st.session_state.local_user_data["projects"][project]
                        except Exception:
                            pass
                        # Clear current project and go back to projects
                        st.session_state.current_project = None
                        st.session_state.current_page = 'projects'
                        # Clear the delete confirmation state
                        if "delete_confirm_tracker" in st.session_state:
                            del st.session_state["delete_confirm_tracker"]
                        st.rerun()
                    else:
                        st.error(f"Failed to delete project '{project}'")
                        st.session_state["delete_confirm_tracker"] = False
                        st.rerun()
            with col_confirm2:
                if st.button("Cancel", key="cancel_delete_tracker"):
                    st.session_state["delete_confirm_tracker"] = False
                    st.rerun()
    
    st.markdown("---")

    # Load existing reel tasks once for the page
    reel_tasks = api_client.get_project_reel_tasks(project)

    # Always-visible status panel at the top
    st.markdown('<h3 class="main-header">Current Reel Task Status</h3>', unsafe_allow_html=True)
    selected_task_id = st.session_state.get('monitor_reel_task_id')
    # If nothing selected yet, default to first task if available
    if not selected_task_id and reel_tasks:
        selected_task_id = reel_tasks[0].get('_id')
        st.session_state.monitor_reel_task_id = selected_task_id

    if reel_tasks:
        # Allow user to pick which task to monitor
        id_to_label = {}
        for t in reel_tasks:
            label = f"{t.get('reel_id','Unknown')}"
            id_to_label[t['_id']] = label
        labels = list(id_to_label.values())
        ids = list(id_to_label.keys())
        # Map current selection index
        try:
            current_idx = ids.index(selected_task_id) if selected_task_id in ids else 0
        except Exception:
            current_idx = 0
        choice = st.selectbox("Choose a task:", options=labels, index=current_idx)
        # Update selection
        for tid, lbl in id_to_label.items():
            if lbl == choice:
                st.session_state.monitor_reel_task_id = tid
                selected_task_id = tid
                break

        # Show status
        status = api_client.get_task_status(selected_task_id)
        if status:
            if status.get('is_processing'):
                st.info("Reel task is processing...")
                latest_event = status.get('latest_event')
                if latest_event:
                    st.caption(
                        f"Latest: {latest_event.get('event_type', 'event')} at "
                        f"{datetime.fromtimestamp(latest_event.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}"
                    )
            else:
                st.success("Reel task is idle/completed")
        else:
            st.warning("Unable to fetch reel task status.")
    else:
        st.caption("No reel tasks yet.")

    st.markdown("---")

    # Add new reel to track
    st.markdown('<h3 class="main-header">Add Reel to Track</h3>', unsafe_allow_html=True)
    with st.expander("Add Instagram Reel", expanded=False):
        with st.form("add_reel_form"):
            reel_url = st.text_input(
                "Instagram Reel URL", 
                placeholder="https://www.instagram.com/reel/...",
                help="Paste the full Instagram reel URL here"
            )
            
            # Add scraping interval settings
            st.markdown('<h4 class="main-header">Scraping Settings</h4>', unsafe_allow_html=True)
            scrape_interval = st.number_input(
                "Scrape Interval (days)", 
                min_value=0.5, 
                max_value=30.0, 
                value=2.0,
                step=0.5,
                help="How often to automatically scrape this reel (0.5 = 12 hours, 1 = daily, 7 = weekly)"
            )
            
            st.caption(f"Reel will be scraped every {scrape_interval} days")
            
            submit = st.form_submit_button("Add Reel to Track")
            
            if submit:
                if reel_url:
                    task_id = api_client.create_reel_tracking_task(project, reel_url, scrape_interval)
                    if task_id:
                        st.success(f"Added reel to tracking with {scrape_interval}-day interval")
                        st.rerun()
                    else:
                        st.error("Failed to add reel to tracking")
                else:
                    st.error("Please enter a reel URL")
    
    # Display existing reel tasks
    st.markdown('<h3 class="main-header">Tracked Reels</h3>', unsafe_allow_html=True)

    if not reel_tasks:
        st.info("No reels are being tracked. Add your first reel above!")
    else:
        st.markdown(f"**Total tracked reels:** {len(reel_tasks)}")
        
        for task in reel_tasks:
            with st.container():
                st.markdown("---")
                
                # Reel info
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Reel ID:** {task.get('reel_id', 'N/A')}")
                    st.caption(f"**URL:** {task.get('reel_url', 'N/A')}")
                    
                    # Show current interval
                    current_interval = task.get('scrape_interval_days', 2)
                    st.caption(f"**Current interval:** {current_interval} days")
                    
                    # Show last scraped
                    if task.get('last_scraped'):
                        last_scraped = datetime.fromtimestamp(task['last_scraped'])
                        st.caption(f"**Last scraped:** {last_scraped.strftime('%Y-%m-%d %H:%M')}")

                    # Show live processing status for this task
                    try:
                        t_status = api_client.get_task_status(task['_id'])
                        if t_status and t_status.get('is_processing'):
                            st.caption("Status: processing")
                        else:
                            st.caption("Status: idle")
                    except Exception:
                        pass
                
                with col2:
                    # Actions
                    if st.button("Force Scrape", key=f"force_scrape_reel_{task['_id']}"):
                        with st.spinner("Starting reel scrape in background..."):
                            if api_client.force_scrape_reel_task(task['_id']):
                                st.success("Scraping initiated! Monitoring status...")
                                st.session_state.monitor_reel_task_id = task['_id']
                            else:
                                st.error("Failed to scrape")
                    
                    if st.button("Update Interval", key=f"update_reel_interval_{task['_id']}"):
                        st.session_state.editing_reel_task_id = task['_id']
                        st.session_state.editing_reel_current_interval = current_interval
                        st.rerun()
                    
                    if st.button("Delete", key=f"delete_reel_{task['_id']}"):
                        if hasattr(api_client, 'delete_reel_task') and api_client.delete_reel_task(task['_id']):
                            st.success("Reel task deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete reel task")
                
                # Show reel data if available
                reel_data = task.get('reel_data', {})
                if reel_data:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Likes", f"{reel_data.get('likes', 0):,}")
                    with col2:
                        st.metric("Comments", f"{reel_data.get('comments', 0):,}")
                    with col3:
                        st.metric("Views", f"{reel_data.get('views', 0):,}")
                    with col4:
                        sentiment = reel_data.get('sentiment_analysis', {}).get('overall_sentiment', 'neutral')
                        st.metric("Sentiment", sentiment.title())
        
        # Interval update form for reels
        if hasattr(st.session_state, 'editing_reel_task_id'):
            st.markdown('<h4 class="main-header">Update Reel Scraping Interval</h4>', unsafe_allow_html=True)
            with st.form("update_reel_interval_form"):
                new_interval = st.number_input(
                    "New Scrape Interval (days)",
                    min_value=0.5,
                    max_value=30.0,
                    value=st.session_state.editing_reel_current_interval,
                    step=0.5,
                    help="How often to automatically scrape this reel"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update Interval"):
                        if api_client.update_scrape_interval(st.session_state.editing_reel_task_id, new_interval):
                            st.success(f"Updated reel interval to {new_interval} days")
                            del st.session_state.editing_reel_task_id
                            del st.session_state.editing_reel_current_interval
                            st.rerun()
                        else:
                            st.error("Failed to update interval")
                
                with col2:
                    if st.form_submit_button("Cancel"):
                        del st.session_state.editing_reel_task_id
                        del st.session_state.editing_reel_current_interval
                        st.rerun()
        
        # Show detailed reel data
        if reel_tasks:
            st.markdown('<h4 class="main-header">Reel Performance</h4>', unsafe_allow_html=True)
            
            # Create performance chart
            performance_data = []
            for task in reel_tasks:
                if task.get('reel_data'):
                    reel_data = task['reel_data']
                    performance_data.append({
                        'Reel ID': task.get('reel_id', 'Unknown'),
                        'Likes': reel_data.get('likes', 0),
                        'Comments': reel_data.get('comments', 0),
                        'Views': reel_data.get('views', 0)
                    })
            
            if performance_data:
                df = pd.DataFrame(performance_data)
                
                # Create performance chart
                fig = make_subplots(
                    rows=1, cols=3,
                    subplot_titles=('Likes', 'Comments', 'Views'),
                    specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
                )
                
                fig.add_trace(
                    go.Bar(x=df['Reel ID'], y=df['Likes'], name='Likes'),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Bar(x=df['Reel ID'], y=df['Comments'], name='Comments'),
                    row=1, col=2
                )
                fig.add_trace(
                    go.Bar(x=df['Reel ID'], y=df['Views'], name='Views'),
                    row=1, col=3
                )
                
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True) 

    # Live reel task status monitor (always visible if a task is selected)
    st.markdown("---")
    st.markdown('<h4 class="main-header">Current Reel Task Status</h4>', unsafe_allow_html=True)
    selected_task_id = st.session_state.get('monitor_reel_task_id')
    if not selected_task_id and reel_tasks:
        # Default to first task to show status
        selected_task_id = reel_tasks[0].get('_id')
    if selected_task_id:
        status = api_client.get_task_status(selected_task_id)
        if status:
            if status.get('is_processing'):
                st.info("Reel task is processing...")
                latest_event = status.get('latest_event')
                if latest_event:
                    st.caption(
                        f"Latest: {latest_event.get('event_type', 'event')} at "
                        f"{datetime.fromtimestamp(latest_event.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}"
                    )
            else:
                st.success("Reel task is idle/completed")
        else:
            st.warning("Unable to fetch reel task status.")