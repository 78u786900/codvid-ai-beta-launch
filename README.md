# CodVid.AI - Instagram Analytics Platform

A premium, production-ready Streamlit mobile web app for Instagram analytics and tracking, built with a focus on minimalistic design and AI-powered insights. Built based on the functionality from the demo notebooks.

## Features

### 🔐 Authentication
- User signup and login system
- Secure session management
- Account deletion capability

### 📊 Instagram Profile Tracking
- **Own Profile Tracking**: Track your own Instagram profiles
- **Competitor Analysis**: Track unlimited competitor profiles
- **Automatic Scraping**: Scheduled scraping with configurable intervals
- **Manual Scraping**: Force immediate data collection
- **Performance Metrics**: Likes, comments, views analysis
- **Sentiment Analysis**: AI-powered comment sentiment analysis

### 📁 Project Management
- **Project Creation**: Create multiple projects for different campaigns
- **AI Chat Integration**: Interactive AI chat for each project
- **Reel Tracking**: Track specific Instagram reels within projects

### 📈 Analytics & Visualization
- **Performance Charts**: Interactive charts for likes, comments, views
- **Sentiment Distribution**: Pie charts for sentiment analysis
- **Data Tables**: Detailed post and comment data
- **Real-time Updates**: Live data refresh capabilities

## User Journey Flow

1. **Sign Up/Login**: Users create an account or log in
2. **Dashboard**: Manage Instagram profile tracking tasks
   - Create tracking tasks for own profiles (limited to one)
   - Create unlimited competitor tracking tasks
   - View all tracked profiles with status and last scrape info
3. **Profile Details**: Click on any profile to see detailed analytics
   - View scraped data and performance metrics
   - Force manual scraping
   - Configure automatic scraping intervals
   - View sentiment analysis results
4. **Projects**: Navigate to project management
   - Create new projects
   - Access project-specific features
5. **Project Features**:
   - **Explorer Page**: Interactive AI chat for project-specific assistance
   - **Tracker Page**: Track specific Instagram reels within the project

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the web_app directory**
   ```bash
   cd web_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the app**
   - Open your browser and go to `http://localhost:8501`
   - The app will automatically open in your default browser

## API Configuration

The app is configured to use the development backend by default:
- **Base URL**: `https://codvid-ai-backend-development.up.railway.app`

To change the environment, modify the `APIClient` initialization in `main.py`:
```python
api_client = APIClient("https://codvid-ai-backend-production.up.railway.app")  # Production
# or
api_client = APIClient("http://localhost:8080")  # Local
```

## Usage Guide

### Getting Started

1. **Create Account**: Sign up with your email and password
2. **Login**: Access your dashboard
3. **Add Instagram Profiles**: Create tracking tasks for profiles you want to monitor
4. **View Analytics**: Click on any profile to see detailed analytics
5. **Create Projects**: Organize your work into projects
6. **Use AI Chat**: Get AI assistance for your projects
7. **Track Reels**: Add specific reels to track within projects

### Key Features

#### Profile Tracking
- **Own Profile**: Track your own Instagram profile (limited to one)
- **Competitors**: Track unlimited competitor profiles
- **Automatic Updates**: Set scraping intervals (0.5 to 30 days)
- **Manual Updates**: Force immediate scraping when needed

#### Analytics Dashboard
- **Performance Metrics**: Total likes, comments, views
- **Post Analysis**: Recent posts with engagement data
- **Sentiment Analysis**: AI-powered comment sentiment analysis
- **Visual Charts**: Interactive charts for data visualization

#### Project Management
- **Multiple Projects**: Create and manage multiple projects
- **AI Integration**: Chat with AI for project-specific assistance
- **Reel Tracking**: Track specific Instagram reels within projects

## Technical Architecture

### Frontend
- **Streamlit**: Modern web framework for data apps
- **Mobile-Responsive**: Optimized for mobile devices
- **Interactive UI**: Real-time updates and user interactions

### Backend Integration
- **RESTful API**: Integration with the backend services
- **Authentication**: JWT token-based authentication
- **Real-time Data**: Live data fetching and updates

### Data Visualization
- **Plotly**: Interactive charts and graphs
- **Pandas**: Data manipulation and analysis
- **Real-time Updates**: Live data refresh capabilities

## File Structure

```
web_app/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── pages/                 # Page modules
    ├── __init__.py        # Package initialization
    ├── login.py           # Authentication page
    ├── dashboard.py       # Main dashboard
    ├── profile_details.py # Profile analytics
    ├── projects.py        # Project management
    ├── project_chat.py    # AI chat interface
    └── project_tracker.py # Reel tracking interface
```

## Mobile Optimization

The app is optimized for mobile devices with:
- **Responsive Design**: Adapts to different screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Mobile Navigation**: Simplified navigation for mobile
- **Fast Loading**: Optimized for mobile network speeds

## Troubleshooting

### Common Issues

1. **Connection Errors**: Check if the backend server is running
2. **Authentication Issues**: Ensure correct email/password
3. **Data Not Loading**: Try refreshing the page or force scraping
4. **Mobile Display Issues**: Use landscape mode for better viewing

### Support

For technical support or feature requests, please refer to the original demo notebooks for implementation details.

## Development

### Adding New Features

1. **Create new page module** in `pages/` directory
2. **Update main.py** to include the new page routing
3. **Test thoroughly** with different data scenarios
4. **Update documentation** as needed

### Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add comments for complex logic
- Maintain consistent formatting

## License

This project is based on the demo notebooks and follows the same licensing terms. 