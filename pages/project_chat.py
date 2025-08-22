import streamlit as st
import json
from datetime import datetime

def show_project_chat(api_client):
    """Show project chat interface matching the exact UI from the image"""
    if not st.session_state.current_project:
        st.error("No project selected")
        st.button("Back to Dashboard", on_click=lambda: setattr(st.session_state, 'current_page', 'dashboard'))
        return
    
    project = st.session_state.current_project
    
    # Function to load existing chat history from API
    def load_project_chat_history(api_client, project):
        try:
            # Ensure the project key exists in session state
            if project not in st.session_state.local_user_data["projects"]:
                st.session_state.local_user_data["projects"][project] = {}
            if "chats" not in st.session_state.local_user_data["projects"][project]:
                st.session_state.local_user_data["projects"][project]["chats"] = []
            
            # Try to get existing chat data from project data if available
            try:
                project_data = api_client.get_project_data(project)
                if project_data and isinstance(project_data, dict):
                    # Check if project data contains chat history
                    if "chats" in project_data and isinstance(project_data["chats"], list):
                        st.session_state.local_user_data["projects"][project]["chats"] = project_data["chats"]
                    elif "chat_history" in project_data and isinstance(project_data["chat_history"], list):
                        st.session_state.local_user_data["projects"][project]["chats"] = project_data["chat_history"]
            except Exception:
                # If API call fails, keep existing local chats
                pass
                
        except Exception as e:
            # If anything fails, ensure we have a safe structure
            if project not in st.session_state.local_user_data["projects"]:
                st.session_state.local_user_data["projects"][project] = {}
            if "chats" not in st.session_state.local_user_data["projects"][project]:
                st.session_state.local_user_data["projects"][project]["chats"] = []
    
    # Simplified top bar - one row only
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # CodVid.AI branding above Home button - matching dashboard size
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 2.0rem; font-weight: 700; color: #000000; margin-bottom: 1.3rem; margin-top: 1.0rem;">CodVid.AI</div>
            <div style="font-size: 1.1rem; color: #000000;">Interactive Inno-mod Chat</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Home button (left side)
        if st.button("Home", key="home_button", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col2:
        # Project dropdown selector with refresh capability
        projects = api_client.get_project_list()
        
        # Project selector only (no refresh button)
        if projects:
            current_project_idx = projects.index(project) if project in projects else 0
            selected_project = st.selectbox(
                f"**{project}** ▼",
                options=projects,
                index=current_project_idx,
                key="project_selector_chat",
                label_visibility="collapsed"
            )
        
        # Handle project selection change
        if 'selected_project' in locals() and selected_project != project:
            st.session_state.current_project = selected_project
            # Load chat history for the new project
            load_project_chat_history(api_client, selected_project)
            st.rerun()
        
        # Add New Project button below project selector
        if st.button("Add New Project", key="add_project_button", use_container_width=True):
            st.session_state.show_add_project_form = True
            st.rerun()
        
        # New Project Creation Form
        if st.session_state.get('show_add_project_form', False):
            with st.expander("Create New Project", expanded=True):
                with st.form("create_project_form", clear_on_submit=True):
                    project_name = st.text_input("Project Name", placeholder="Enter project name", key="new_project_name")
                    project_description = st.text_area("Project Description (Optional)", placeholder="Enter project description", key="new_project_description")
                    
                    col_submit, col_cancel = st.columns(2)
                    with col_submit:
                        submit = st.form_submit_button("Create Project", use_container_width=True)
                    with col_cancel:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            st.session_state.show_add_project_form = False
                            st.rerun()
                    
                    if submit and project_name:
                        try:
                            # Create new project via API (following the notebook pattern)
                            if project_name not in projects:
                                # First create the project on the server
                                success = api_client.create_project(project_name)
                                if success:
                                    # Load the project data into cache
                                    api_client.load_project_into_cache(project_name)
                                    
                                    # Update local project list
                                    projects = api_client.get_project_list()
                                    
                                    # Set as current project
                                    st.session_state.current_project = project_name
                                    st.session_state.show_add_project_form = False
                                    st.success(f"Project '{project_name}' created successfully on server!")
                                    st.rerun()
                                else:
                                    st.error("Failed to create project on server. Please try again.")
                            else:
                                st.error("Project name already exists!")
                        except Exception as e:
                            st.error(f"Failed to create project: {e}")
                    elif submit:
                        st.error("Please enter a project name")
    

    
    # Convert Chat/Tracker buttons to dropdown lists
    col1, col2 = st.columns([1, 1])
    with col1:
        # Chat button (same design as Tracker)
        if st.button("Chat", key="chat_button", use_container_width=True):
            # Already on chat page, do nothing or refresh
            st.rerun()
    
    with col2:
        # Tracker button
        if st.button("Tracker", key="tracker_button", use_container_width=True):
            st.session_state.current_page = 'project_tracker'
            st.rerun()
    
    # Get tracking tasks for profile selector in form
    tasks = api_client.get_tracking_tasks()
    
    # Chat conversation area - make it scrollable with fixed height
    st.markdown("**Chat History**")
    
    # Initialize chat history for this specific project
    if 'local_user_data' not in st.session_state:
        st.session_state.local_user_data = {}
    if "projects" not in st.session_state.local_user_data:
        st.session_state.local_user_data["projects"] = {}
    if project not in st.session_state.local_user_data["projects"]:
        st.session_state.local_user_data["projects"][project] = {}
    if "chats" not in st.session_state.local_user_data["projects"][project]:
        st.session_state.local_user_data["projects"][project]["chats"] = []
    
    # Load chat history for current project
    load_project_chat_history(api_client, project)
    
    # Create a fixed-size scrollable chat grid container using Streamlit's native container
    with st.container():
        # Apply the CSS styling directly to this container
        st.markdown("""
        <style>
        .stContainer {
            max-height: 65vh !important;
            height: auto !important;
            overflow-y: auto !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
            background: #fafafa !important;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        
        /* Ensure all content inside stays within borders */
        .stContainer > * {
            max-width: 100% !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }
        
        /* Force message content to stay within container */
        .stContainer .stMarkdown {
            max-width: 100% !important;
            overflow: hidden !important;
        }
        
        /* Handle URL overflow and make message boxes flexible */
        .stContainer .stMarkdown a {
            word-break: break-all !important;
            overflow-wrap: break-word !important;
            max-width: 100% !important;
        }
        
        /* Make message boxes more flexible for URLs */
        div[style*="display: inline-block"] {
            max-width: 85% !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
        # Prefer chats from local user data cache if available
        local_chats = None
        try:
            local_chats = st.session_state.local_user_data["projects"][project]["chats"]
        except Exception:
            local_chats = None

        # Chat messages content
        # Always prefer local cache chats if available
        messages_src = local_chats if isinstance(local_chats, list) and local_chats else []
            
        # Real chat room layout - messages on left/right with exact styling
        if not messages_src:
            st.info("No messages yet. Start a conversation!")
        else:
            for i, message in enumerate(messages_src):
                role = message.get('role')
                mtype = message.get('type')
                content = message.get('content') or message.get('text') or ''

                # Event messages as collapsible dropdowns
                if mtype == 'event':
                    event_type = message.get('event_type', 'event')
                    with st.expander(f"**{event_type}**", expanded=False):
                        st.markdown(f"**Event Type:** {event_type}")
                        st.markdown(f"**Content:** {content}")
                        
                        # Show additional event data if available
                        if message.get('options'):
                            st.markdown("**Options:**")
                            for opt in message.get('options', []):
                                st.markdown(f"- `{opt}`")
                        
                        # Show raw message data for debugging
                        st.markdown("**Raw Data:**")
                        st.json(message)

                # Tool messages as collapsible dropdowns
                elif role == 'tool':
                    with st.expander(f"**Tool: {content[:50]}...**", expanded=False):
                        st.markdown(f"**Tool Output:**")
                        st.markdown(f"```json\n{content}\n```")
                        
                        # Try to parse and display JSON nicely
                        try:
                            parsed = json.loads(content)
                            st.markdown("**Parsed Data:**")
                            st.json(parsed)
                        except:
                            st.markdown("**Raw Content:**")
                            st.text(content)

                # Standard role-based rendering with exact styling from image
                elif role == 'user':
                    # User messages on the right with softer dark background and timestamp (matching AI style)
                    current_time = datetime.now().strftime("%I:%M %p")  # Format like "11:52 PM"
                    st.markdown(
                        f'<div style="text-align: right; margin: 8px 0;">'
                        f'<div style="display: inline-block; background-color: #374151; color: white; '
                        f'padding: 10px 15px; border-radius: 15px; max-width: 70%; text-align: left; '
                        f'border: 1px solid #4B5563;">'
                        f'<strong>YOU</strong><br>'
                        f'<small style="color: #D1D5DB;">{current_time}</small><br>'
                        f'{content}</div>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                elif role == 'assistant':
                    # AI messages on the left with light grey background and timestamp
                    current_time = datetime.now().strftime("%I:%M %p")  # Format like "11:52 PM"
                    st.markdown(
                        f'<div style="text-align: left; margin: 8px 0;">'
                        f'<div style="display: inline-block; background-color: #F3F4F6; color: #111827; '
                        f'padding: 10px 15px; border-radius: 15px; max-width: 70%; border: 1px solid #E5E7EB;">'
                        f'<strong>AI ASSISTANT</strong><br>'
                        f'<small style="color: #6B7280;">{current_time}</small><br>'
                        f'{content}</div>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f"**{role or 'system'}:** {content}")

                # Minimal spacing between messages (no horizontal lines)
                if i < len(messages_src) - 1:
                    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
    
        # Close chat grid container (Streamlit container closes automatically)
    
    # Fixed bottom input area - always visible at bottom
    
    # Create a fixed input section at the bottom
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            # Profile selector directly in the form (replaces the "Message to AI" label)
            profile_options = ["N/A"] + [task['target_profile'] for task in tasks] if tasks else ["N/A"]
            selected_profile = st.selectbox(
                "Select profile to tag:",
                options=profile_options,
                index=0,
                key="profile_selector_form"
            )
            message = st.text_input(
                "Type your message...",
                placeholder="Type your message...",
                key="chat_input"
            )
        with col2:
            submit = st.form_submit_button("Send Message", use_container_width=True)
        
        if submit and message:
            # Combine profile tag with message if profile is selected
            if selected_profile != 'N/A':
                combined_message = f"@{selected_profile}: {message}"
            else:
                combined_message = message
            
            # Add user message to local cache and fallback history
            try:
                st.session_state.local_user_data["projects"][project]["chats"].append({
                    'role': 'user', 'type': 'text', 'text': combined_message
                })
            except Exception:
                st.session_state.chat_history.append({'role': 'user', 'text': combined_message})

            # Get AI response (streaming)
            with st.spinner("AI is thinking..."):
                streaming_response = api_client.ai_chat(project, combined_message)
                
                if streaming_response:
                    # Create a placeholder for the streaming AI response
                    ai_message_placeholder = st.empty()
                    
                    # Process streaming response in real-time
                    aggregated_text = ""
                    assistant_message_added_via_mods = False
                    
                    try:
                        for text_chunk, is_final, data_mods in api_client.process_streaming_response(streaming_response, project):
                            if text_chunk:
                                aggregated_text += text_chunk
                                # Update the placeholder in real-time
                                ai_message_placeholder.markdown(f"**AI:** {aggregated_text}")
                            
                            # Check if this was added via data_mods
                            if data_mods and not assistant_message_added_via_mods:
                                for mod in data_mods:
                                    try:
                                        key_path = mod.get("key_path")
                                        mode = mod.get("mode")
                                        value = mod.get("value")
                                        if (
                                            isinstance(key_path, list)
                                            and len(key_path) >= 3
                                            and key_path[-2] == project
                                            and key_path[-1] == "chats"
                                            and mode in ("append", "create")
                                        ):
                                            messages = value if isinstance(value, list) else [value]
                                            for m in messages:
                                                if isinstance(m, dict) and m.get("role") == "assistant":
                                                    assistant_message_added_via_mods = True
                                                    break
                                    except Exception:
                                        continue
                            
                            # If final, break the loop
                            if is_final:
                                break
                        
                        # Add the complete AI response to chat history if not already added via data_mods
                        if aggregated_text and not assistant_message_added_via_mods:
                            try:
                                st.session_state.local_user_data["projects"][project]["chats"].append({
                                    'role': 'assistant', 'type': 'text', 'text': aggregated_text
                                })
                            except Exception:
                                st.session_state.chat_history.append({'role': 'assistant', 'text': aggregated_text})
                                
                    except Exception as e:
                        st.error(f"Error processing streaming response: {e}")
                else:
                    st.error("Failed to get AI response")

            st.rerun()
    
    # Close input container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add custom CSS for input container and scrollbar styling
    st.markdown("""
    <style>
    .input-container {
        position: relative;
        background: white;
        border-top: 1px solid #e5e7eb;
        padding: 1rem 0;
        z-index: 2;
        margin-top: 1rem;
    }
    
    /* Custom scrollbar for the chat container */
    .stContainer::-webkit-scrollbar {
        width: 8px;
    }
    
    .stContainer::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    .stContainer::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    .stContainer::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    </style>
    """, unsafe_allow_html=True) 