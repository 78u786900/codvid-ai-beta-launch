import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time
from typing import List, Dict, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import pages
from pages.login import show_login
from pages.dashboard import show_dashboard
from pages.profile_details import show_profile_details
from pages.projects import show_projects_page
from pages.project_chat import show_project_chat
from pages.project_tracker import show_project_tracker

# Import configuration
from config import Config

# Configure Streamlit page
st.set_page_config(
    page_title=Config.STREAMLIT_CONFIG["page_title"],
    page_icon=Config.STREAMLIT_CONFIG["page_icon"],
    layout=Config.STREAMLIT_CONFIG["layout"],
    initial_sidebar_state=Config.STREAMLIT_CONFIG["initial_sidebar_state"]
)

# Apply custom CSS for CodVid.AI branding
def apply_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #000000;
        margin-bottom: 1rem;
    }
    .brand-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .brand-subtitle {
        font-size: 1.2rem;
        color: #000000;
        text-align: center;
        margin-bottom: 2rem;
    }
    .premium-button {
        background-color: #000000;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .premium-button:hover {
        background-color: #333333;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .card-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    .profile-block {
        background: #F9FAFB;
        border: 2px solid #E5E7EB;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .profile-block:hover {
        border-color: #000000;
        background: #F0F0F0;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Prevent page swipe on mobile */
    body {
        overscroll-behavior: none;
        touch-action: pan-y;
        -webkit-overflow-scrolling: touch;
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
    .stApp {
        overscroll-behavior: none;
        touch-action: pan-y;
        -webkit-overflow-scrolling: touch;
    }
    /* Prevent pull-to-refresh and swipe gestures */
    html {
        overscroll-behavior: none;
        touch-action: pan-y;
    }
    * {
        -webkit-touch-callout: none;
        -webkit-user-select: none;
        -khtml-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    /* Allow text selection for inputs and text areas */
    input, textarea, [contenteditable] {
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
        user-select: text;
    }
    
    /* PERMANENT LEFT/RIGHT LAYOUT - Never stack vertically */
    .stColumns > div {
        min-width: 0 !important;
        flex-shrink: 0 !important;
    }
    
    /* Force 2:1 ratio columns to stay horizontal */
    .stColumns > div:first-child {
        width: 66.666667% !important;
        max-width: 66.666667% !important;
        min-width: 66.666667% !important;
    }
    
    .stColumns > div:last-child {
        width: 33.333333% !important;
        max-width: 33.333333% !important;
        min-width: 33.333333% !important;
    }
    
    /* Mobile responsive improvements */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
            max-width: 100%;
        }
        
        /* Keep left/right layout even on mobile */
        .stColumns > div:first-child {
            width: 66.666667% !important;
            max-width: 66.666667% !important;
            min-width: 66.666667% !important;
        }
        
        .stColumns > div:last-child {
            width: 33.333333% !important;
            max-width: 33.333333% !important;
            min-width: 33.333333% !important;
        }
        
        /* Better button spacing on mobile */
        .stButton > button {
            margin-bottom: 0.5rem;
            padding: 0.75rem 1rem;
            font-size: 1rem;
        }
        
        /* Profile blocks mobile optimization */
        .profile-block {
            padding: 0.75rem;
            margin-bottom: 0.75rem;
        }
        
        /* Card containers mobile */
        .card-container {
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        
        /* Brand title mobile */
        .brand-title {
            font-size: 2rem;
        }
        
        .brand-subtitle {
            font-size: 1rem;
        }
    }
    
    /* Remove default Streamlit spacing issues */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    /* Better spacing for sections */
    .main-header {
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Additional layout stability */
    .stColumns {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: flex-start !important;
    }
    
    /* Ensure dashboard layout never changes */
    .dashboard-layout {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
    }
    
    /* Quick Actions form styling */
    .stForm {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Form inputs styling */
    .stForm input, .stForm select {
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 0.5rem;
    }
    
    /* Form buttons styling */
    .stForm button {
        background: #000000;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    /* New Project Form styling */
    .stExpander {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        margin-top: 0.5rem;
    }
    
    .stExpander > div > div {
        padding: 1rem;
    }
    
    .stForm button:hover {
        background: #333333;
        transform: translateY(-1px);
    }
    
    /* GLOBAL APP MARGINS AND WHITE SPACE - Applied to ALL pages */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        padding-left: 4rem;
        padding-right: 4rem;
        max-width: 90%;
        margin: 0 auto;
    }
    
    /* Ensure proper spacing for mobile devices */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 98%;
        }
    }
    
    /* Add spacing between sections */
    .stMarkdown {
        margin-bottom: 1rem;
    }
    
    /* Better spacing for columns */
    .stColumns > div {
        padding: 0 0.5rem;
    }
    
    /* Add some breathing room around the main content */
    .stApp {
        background-color: #f8fafc;
        padding: 1rem !important;
    }
    
    /* Prevent button cutoff and ensure proper spacing */
    .stButton > button {
        margin: 0.5rem 0 !important;
        min-height: 44px !important;
        box-sizing: border-box !important;
    }
    
    /* Ensure top bar elements are fully visible */
    .stColumns > div {
        overflow: visible !important;
        min-height: auto !important;
    }
    
    .main .block-container {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    </style>
    <script>
    // Prevent swipe gestures
    let startX, startY;
    
    document.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchmove', function(e) {
        if (!startX || !startY) return;
        
        let diffX = startX - e.touches[0].clientX;
        let diffY = startY - e.touches[0].clientY;
        
        // Prevent horizontal swipes (left/right navigation)
        if (Math.abs(diffX) > Math.abs(diffY)) {
            e.preventDefault();
        }
    }, { passive: false });
    
    document.addEventListener('touchend', function() {
        startX = null;
        startY = null;
    });
    
    // Prevent browser back/forward swipe gestures
    window.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1) {
            const touch = e.touches[0];
            if (touch.clientX < 10 || touch.clientX > window.innerWidth - 10) {
                e.preventDefault();
            }
        }
    }, { passive: false });
    

    </script>
    """, unsafe_allow_html=True)

# Apply custom CSS
apply_custom_css()

def check_session_timeout():
    """Check if user session has timed out and auto-logout if needed"""
    if st.session_state.authenticated:
        current_time = time.time()
        time_since_last_activity = current_time - st.session_state.last_activity
        
        # Show warning at 13 minutes
        if time_since_last_activity > 780:  # 13 minutes
            if time_since_last_activity > st.session_state.session_timeout:
                # Auto-logout after 15 minutes
                st.session_state.authenticated = False
                st.session_state.session_token = None
                st.session_state.current_page = 'login'
                st.warning("Session expired due to inactivity. Please login again.")
                st.rerun()
            else:
                # Show warning
                remaining_time = int(st.session_state.session_timeout - time_since_last_activity)
                st.warning(f"Session will expire in {remaining_time} seconds due to inactivity.")
        
        # Update last activity on any user interaction
        if st.session_state.get('_last_interaction_time', 0) != current_time:
            st.session_state.last_activity = current_time
            st.session_state._last_interaction_time = current_time

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'session_token' not in st.session_state:
    st.session_state.session_token = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'current_project' not in st.session_state:
    st.session_state.current_project = None
if 'current_profile' not in st.session_state:
    st.session_state.current_profile = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
if 'log_raw_streaming' not in st.session_state:
    # Keep raw streaming chunk logging ON by default per user request
    st.session_state.log_raw_streaming = True
if 'api_logs' not in st.session_state:
    st.session_state.api_logs = []
if 'local_user_data' not in st.session_state:
    st.session_state.local_user_data = {
        "global_data": {"ai_memory": {}, "video_reflections": {}},
        "projects": {}
    }
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = time.time()
if 'session_timeout' not in st.session_state:
    st.session_state.session_timeout = 900  # 15 minutes in seconds

class APIClient:
    """API client for interacting with the backend"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session_token = None
        self.debug_enabled = False
    
    def set_debug(self, enabled: bool):
        self.debug_enabled = enabled

    def set_log_raw_streaming(self, enabled: bool):
        """Enable saving raw streaming chunks into the debug logs."""
        self.log_raw_streaming = enabled
    
    def _sanitize_headers(self, headers: dict) -> dict:
        sanitized = dict(headers or {})
        if 'Authorization' in sanitized:
            token = sanitized['Authorization']
            if isinstance(token, str) and token.startswith('Bearer '):
                sanitized['Authorization'] = 'Bearer ****'
        return sanitized
    
    def _append_log(self, entry: dict):
        try:
            st.session_state.api_logs.append(entry)
        except Exception:
            pass

    # ---------- Local cache helpers (demo-parity) ----------
    def _get_cache(self) -> dict:
        return st.session_state.local_user_data

    def apply_user_data_mods(self, context_mods: list[dict]):
        cache = self._get_cache()
        modified_projects: set[str] = set()
        for mod in context_mods or []:
            key_path = mod.get("key_path")
            mode = mod.get("mode")
            value = mod.get("value")
            if not isinstance(key_path, list) or mode not in {"create", "edit", "del", "append"}:
                continue
            if len(key_path) >= 2 and key_path[0] == "projects" and isinstance(key_path[1], str):
                if not (len(key_path) == 3 and key_path[2] == "mod_count"):
                    modified_projects.add(key_path[1])
            # Traverse to parent
            target = cache
            try:
                for key in key_path[:-1]:
                    if isinstance(target, dict):
                        if key not in target:
                            if mode == "create":
                                target[key] = {}
                            else:
                                raise KeyError
                        target = target[key]
                    elif isinstance(target, list) and isinstance(key, int):
                        target = target[key]
                    else:
                        raise TypeError
                last_key = key_path[-1]
                if mode == "create":
                    if isinstance(target, dict):
                        target[last_key] = value
                    elif isinstance(target, list) and isinstance(last_key, int):
                        if last_key == len(target):
                            target.append(value)
                        elif last_key < len(target):
                            target[last_key] = value
                elif mode == "edit":
                    if isinstance(target, dict):
                        target[last_key] = value
                    elif isinstance(target, list) and isinstance(last_key, int):
                        target[last_key] = value
                elif mode == "del":
                    if isinstance(target, dict):
                        if last_key in target:
                            del target[last_key]
                    elif isinstance(target, list) and isinstance(last_key, int):
                        if last_key < len(target):
                            target.pop(last_key)
                elif mode == "append":
                    if isinstance(target, dict):
                        if last_key not in target or not isinstance(target[last_key], list):
                            target[last_key] = []
                        target[last_key].append(value)
                    elif isinstance(target, list) and isinstance(last_key, int):
                        if last_key < len(target):
                            if not isinstance(target[last_key], list):
                                target[last_key] = []
                            target[last_key].append(value)
            except Exception:
                continue
        # Increment mod_count
        for project_name in modified_projects:
            try:
                proj = cache.get("projects", {}).get(project_name)
                if proj is not None:
                    proj["mod_count"] = int(proj.get("mod_count", 0)) + 1
            except Exception:
                continue

    def get_project_mod_count(self, project_name: str) -> int | None:
        payload = {"project_name": project_name}
        result = self._make_request("/codvid-ai/project/get-project-mod-count", method="POST", data=payload)
        if result and result.get("result"):
            return result.get("response", {}).get("mod_count")
        return None

    def load_project_into_cache(self, project_name: str) -> bool:
        data = {"project_name": project_name}
        res = self._make_request("/codvid-ai/project/get-project-data", method="POST", data=data)
        if res and res.get("result"):
            proj = res.get("response", {}).get("project_data")
            if proj is not None:
                cache = self._get_cache()
                cache.setdefault("projects", {})[project_name] = proj
                return True
        return False

    def check_and_reload_project_data(self, project_name: str) -> bool:
        cache = self._get_cache()
        server_mod = self.get_project_mod_count(project_name)
        local_mod = cache.get("projects", {}).get(project_name, {}).get("mod_count")
        if server_mod is None:
            return False
        if local_mod != server_mod:
            return self.load_project_into_cache(project_name)
        return True

    def ensure_project_loaded(self, project_name: str) -> bool:
        cache = self._get_cache()
        if project_name in cache.get("projects", {}):
            return True
        return self.load_project_into_cache(project_name)
    
    def _make_request(self, endpoint: str, method: str = "POST", data: dict | None = None, stream: bool = False, timeout_seconds: int = 300):
        """Make HTTP request to the API (supports streaming)"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Accept": "application/json"
        }
        
        if self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"
        
        payload = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            payload = {
                "schema_version": "4.0",
                "data": data
            }
        
        import time as _time
        start_time = _time.time()
        req_payload = payload
        req_headers = self._sanitize_headers(headers)
        
        try:
            if stream:
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    json=payload,
                    timeout=timeout_seconds,
                    stream=True,
                )
                # Do not append any client-generated summary for streaming responses here.
                # Raw server-sent JSON chunks will be logged verbatim in
                # `process_streaming_response` when `debug_enabled` and
                # `log_raw_streaming` are enabled.
                return response
            else:
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    json=payload,
                    timeout=timeout_seconds,
                )
                if response.status_code in [200, 201]:
                    res_json = response.json()
                    if self.debug_enabled:
                        self._append_log({
                            'timestamp': datetime.now().isoformat(),
                            'endpoint': endpoint,
                            'method': method.upper(),
                            'stream': False,
                            'request': {'url': url, 'headers': req_headers, 'body': req_payload},
                            'response': {'status_code': response.status_code, 'body': res_json},
                            'duration_ms': int((_time.time() - start_time) * 1000),
                        })
                    return res_json
                else:
                    print(f"API Error: {response.status_code} - {response.text}")
                    if self.debug_enabled:
                        self._append_log({
                            'timestamp': datetime.now().isoformat(),
                            'endpoint': endpoint,
                            'method': method.upper(),
                            'stream': False,
                            'request': {'url': url, 'headers': req_headers, 'body': req_payload},
                            'response': {'status_code': response.status_code, 'body': response.text},
                            'duration_ms': int((_time.time() - start_time) * 1000),
                        })
                    return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if self.debug_enabled:
                self._append_log({
                    'timestamp': datetime.now().isoformat(),
                    'endpoint': endpoint,
                    'method': method.upper(),
                    'stream': stream,
                    'request': {'url': url, 'headers': req_headers, 'body': req_payload},
                    'response': {'error': str(e)},
                    'duration_ms': int((_time.time() - start_time) * 1000),
                })
            return None
    
    def login(self, email: str, password: str) -> bool:
        """Login user"""
        data = {"auth_type": "email", "email": email, "password": password}
        result = self._make_request("/codvid-ai/auth/login", data=data)
        if result and result.get("result"):
            self.session_token = result.get("token")
            return True
        return False
    
    def signup(self, email: str, password: str) -> bool:
        """Sign up user"""
        data = {"auth_type": "email", "email": email, "password": password}
        result = self._make_request("/codvid-ai/auth/signup", data=data)
        return result and result.get("result")
    
    def delete_account(self) -> bool:
        """Delete user account"""
        result = self._make_request("/codvid-ai/user/delete-account", data={})
        if result and result.get("result"):
            self.session_token = None
            return True
        return False
    
    def get_project_list(self) -> List[str]:
        """Get list of user projects"""
        result = self._make_request("/codvid-ai/project/get-project-list", data={})
        if result and result.get("result"):
            return result.get("response", {}).get("project_list", [])
        return []
    
    def create_project(self, project_name: str) -> bool:
        """Create a new project"""
        data = {"project_name": project_name}
        result = self._make_request("/codvid-ai/project/create-project", data=data)
        return result and result.get("result")
    
    def delete_project(self, project_name: str) -> bool:
        """Delete a project"""
        data = {"project_name": project_name}
        
        # Add debug logging
        if self.debug_enabled:
            print(f"DEBUG: Attempting to delete project: {project_name}")
            print(f"DEBUG: Request data: {data}")
        
        result = self._make_request("/codvid-ai/project/delete-project", data=data)
        
        # Add debug logging for result
        if self.debug_enabled:
            print(f"DEBUG: Delete project result: {result}")
            if result:
                print(f"DEBUG: Result success: {result.get('result')}")
            else:
                print("DEBUG: No result returned from delete request")
        
        return result and result.get("result")
    
    def get_project_data(self, project_name: str) -> Optional[Dict]:
        """Get project data"""
        data = {"project_name": project_name}
        result = self._make_request("/codvid-ai/project/get-project-data", data=data)
        if result and result.get("result"):
            return result.get("response", {}).get("project_data")
        return None
    
    def ai_chat(self, project_name: str, message: str):
        """Send message to AI chat (streaming). Returns streaming response object.
        
        The response object can be iterated over to get chunks in real-time.
        """
        request_data = {
            "project_name": project_name,
            "message": {
                "role": "user",
                "type": "text",
                "text": message,
            },
        }
        import time as _time
        start_time = _time.time()
        response = self._make_request("/codvid-ai/ai/respond", method="POST", data=request_data, stream=True)
        if not response:
            return None
        
        # Return the streaming response object for real-time processing
        return response
    
    def process_streaming_response(self, response, project_name: str):
        """Process streaming response and yield text chunks in real-time.
        
        This method yields (text_chunk, is_final, data_mods) tuples.
        """
        aggregated_text = ""
        chunks_collected = []
        raw_chunks = []
        assistant_message_added_via_mods = False
        
        try:
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if not chunk:
                    continue
                # Save raw chunk if enabled for later logging
                try:
                    raw_chunks.append(chunk)
                except Exception:
                    pass

                # Log each raw chunk immediately if enabled
                try:
                    if getattr(self, 'debug_enabled', False) and getattr(self, 'log_raw_streaming', False):
                        # Try to parse chunk as JSON for clearer logs; otherwise store raw.
                        parsed = None
                        try:
                            parsed = json.loads(chunk)
                        except Exception:
                            parsed = None

                        entry = {
                            'timestamp': datetime.now().isoformat(),
                            'endpoint': '/codvid-ai/ai/respond',
                            'method': 'POST',
                            'stream': True,
                            'project': project_name,
                        }
                        if parsed is not None:
                            entry['response'] = parsed
                        else:
                            entry['response'] = {'raw': chunk}

                        self._append_log(entry)
                except Exception:
                    pass

                try:
                    chunk_data = json.loads(chunk)
                except Exception:
                    # Skip non-json chunks but continue collecting raw data
                    continue
                
                if chunk_data.get("result"):
                    chunks_collected.append(chunk_data)
                    resp = chunk_data.get("response", {})
                    
                    # Collect assistant text if provided
                    text_piece = resp.get("text") or resp.get("message", {}).get("text")
                    if text_piece:
                        aggregated_text += text_piece
                        # Yield the text chunk for real-time display
                        yield text_piece, False, None

                    # Parse data_mods to capture assistant messages appended to chats
                    data_mods = resp.get("data_mods") or []
                    if isinstance(data_mods, list):
                        # Apply to local cache
                        self.apply_user_data_mods(data_mods)
                        for mod in data_mods:
                            try:
                                key_path = mod.get("key_path")
                                mode = mod.get("mode")
                                value = mod.get("value")
                                if (
                                    isinstance(key_path, list)
                                    and len(key_path) >= 3
                                    and key_path[-2] == project_name
                                    and key_path[-1] == "chats"
                                    and mode in ("append", "create")
                                ):
                                    # Check if this mod adds an assistant message
                                    messages = value if isinstance(value, list) else [value]
                                    for m in messages:
                                        if isinstance(m, dict) and m.get("role") == "assistant":
                                            assistant_message_added_via_mods = True
                                            txt = m.get("text")
                                            if txt:
                                                aggregated_text += txt
                                                # Yield the text chunk for real-time display
                                                yield txt, False, None
                            except Exception:
                                continue
        except Exception as e:
            # Yield error information
            yield f"Error processing response: {str(e)}", True, None
            return
        
        # Optionally log raw streaming chunks for debugging/audit
        try:
            if getattr(self, 'debug_enabled', False) and getattr(self, 'log_raw_streaming', False):
                self._append_log({
                    'timestamp': datetime.now().isoformat(),
                    'endpoint': '/codvid-ai/ai/respond',
                    'method': 'POST',
                    'stream': True,
                    'project': project_name,
                    'raw_streaming_chunks': raw_chunks,
                    'raw_chunks_count': len(raw_chunks),
                })
        except Exception:
            pass

        # Yield final result
        yield aggregated_text, True, data_mods if 'data_mods' in locals() else []
    
    # Instagram Profile Tracking Methods
    def create_tracking_task(self, target_profile: str, is_competitor: bool = False) -> Optional[str]:
        """Create Instagram tracking task"""
        data = {"target_profile": target_profile, "is_competitor": is_competitor}
        result = self._make_request("/codvid-ai/ig-tracking/create_task", data=data)
        if result and result.get("result"):
            return result.get("response", {}).get("task_id")
        return None
    
    def get_tracking_tasks(self) -> List[Dict]:
        """Get all tracking tasks"""
        result = self._make_request("/codvid-ai/ig-tracking/get_tasks", method="GET")
        if result and result.get("result"):
            return result.get("response", {}).get("tasks", [])
        return []
    
    def get_task_details(self, task_id: str) -> Optional[Dict]:
        """Get detailed task information"""
        result = self._make_request(f"/codvid-ai/ig-tracking/get_task/{task_id}", method="GET")
        if result and result.get("result"):
            return result.get("response", {}).get("task")
        return None
    
    def force_scrape_task(self, task_id: str) -> bool:
        """Force scrape a task"""
        # Long-running job: allow up to 15 minutes
        result = self._make_request(
            f"/codvid-ai/ig-tracking/force_scrape/{task_id}",
            method="POST",
            timeout_seconds=900,
        )
        return result and result.get("result")
    
    def delete_tracking_task(self, task_id: str) -> bool:
        """Delete a tracking task"""
        result = self._make_request(f"/codvid-ai/ig-tracking/delete_task/{task_id}", method="DELETE")
        return result and result.get("result")
    
    def update_scrape_interval(self, task_id: str, interval_days: float) -> bool:
        """Update scrape interval for a task"""
        data = {"scrape_interval_days": interval_days}
        result = self._make_request(f"/codvid-ai/ig-tracking/update_scrape_interval/{task_id}", method="PUT", data=data)
        return result and result.get("result")
    
    def get_sentiment_summary(self, task_id: str) -> Optional[Dict]:
        """Get sentiment analysis summary"""
        result = self._make_request(f"/codvid-ai/ig-tracking/sentiment_summary/{task_id}", method="GET")
        if result and result.get("result"):
            return result.get("response", {}).get("sentiment_summary")
        return None
    
    # Instagram Reel Tracking Methods
    def create_reel_tracking_task(self, project_name: str, reel_url: str, scrape_interval_days: int = 2) -> Optional[str]:
        """Create reel tracking task"""
        data = {"project_name": project_name, "reel_url": reel_url, "scrape_interval_days": scrape_interval_days}
        result = self._make_request("/codvid-ai/ig-tracking/create_reel_task", data=data)
        if result and result.get("result"):
            return result.get("response", {}).get("task_id")
        return None
    
    def get_project_reel_tasks(self, project_name: str) -> List[Dict]:
        """Get reel tracking tasks for a project"""
        data = {"project_name": project_name}
        result = self._make_request("/codvid-ai/ig-tracking/get_project_reel_tasks", data=data)
        if result and result.get("result"):
            return result.get("response", {}).get("tasks", [])
        return []
    
    def force_scrape_reel_task(self, task_id: str) -> bool:
        """Force scrape a reel task"""
        # Long-running job: allow up to 15 minutes
        result = self._make_request(
            f"/codvid-ai/ig-tracking/force_scrape_reel/{task_id}",
            method="POST",
            timeout_seconds=900,
        )
        return result and result.get("result")

    def delete_reel_task(self, task_id: str) -> bool:
        """Delete a reel tracking task"""
        result = self._make_request(f"/codvid-ai/ig-tracking/delete_reel_task/{task_id}", method="DELETE")
        return result and result.get("result")

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get real-time processing status for a task (profile or reel)"""
        result = self._make_request(f"/codvid-ai/ig-tracking/task_status/{task_id}", method="GET")
        if result and result.get("result"):
            return result.get("response")
        return None

def main():
    """Main application"""
    # Check session timeout
    check_session_timeout()
    
    # Get API configuration
    api_url = Config.get_api_url()
    api_client = APIClient(api_url)
    
    # Set session token if available
    if st.session_state.session_token:
        api_client.session_token = st.session_state.session_token
    
    # Debug sidebar controls
    with st.sidebar:
        st.markdown("---")
        st.subheader("Debug")
        st.session_state.debug_mode = st.checkbox("Enable debug mode", value=st.session_state.debug_mode)
        if st.button("Clear API logs"):
            st.session_state.api_logs = []
            st.success("Cleared logs")
    # Apply debug and raw-streaming flags to client
    api_client.set_debug(st.session_state.debug_mode)
    api_client.set_log_raw_streaming(st.session_state.log_raw_streaming)

    # Page routing
    if not st.session_state.authenticated:
        show_login(api_client)
    else:
        # Update session token
        st.session_state.session_token = api_client.session_token
        
        # Route to appropriate page
        if st.session_state.current_page == 'dashboard':
            show_dashboard(api_client)
        elif st.session_state.current_page == 'profile_details':
            show_profile_details(api_client)
        elif st.session_state.current_page == 'projects':
            show_projects_page(api_client)
        elif st.session_state.current_page == 'project_chat':
            show_project_chat(api_client)
        elif st.session_state.current_page == 'project_tracker':
            show_project_tracker(api_client)
        else:
            st.session_state.current_page = 'dashboard'
            show_dashboard(api_client)

    # Debug log viewer in sidebar (below controls)
    if st.session_state.debug_mode and st.session_state.api_logs:
        with st.sidebar:
            st.markdown("---")
            st.subheader("API Logs")
            # Show latest first
            for i, entry in enumerate(reversed(st.session_state.api_logs)):
                title = f"{entry.get('method')} {entry.get('endpoint')} ({entry.get('response',{}).get('status_code', entry.get('response',{}).get('error', 'stream'))})"
                with st.expander(title):
                    st.markdown(f"**Timestamp:** {entry.get('timestamp')}")
                    st.markdown(f"**Duration:** {entry.get('duration_ms')} ms")
                    st.markdown(f"**Stream:** {entry.get('stream')}")
                    st.markdown("**Request:**")
                    st.json(entry.get('request', {}))
                    st.markdown("**Response:**")
                    st.json(entry.get('response', {}))

if __name__ == "__main__":
    main()