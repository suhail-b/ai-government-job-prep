# AI Government Job Prep | भारत सरकारी नौकरी तैयारी

A comprehensive AI-powered platform for Indian government job preparation with bilingual support (English/Hindi).

## Features

### Core Functionality
- **AI Quiz Generator**: Personalized quizzes with adaptive difficulty
- **Study Plan Creator**: AI-generated personalized study schedules
- **Mock Interview System**: AI-powered interview practice with feedback
- **Current Affairs Tracker**: Latest updates and practice questions
- **Performance Analytics**: Comprehensive progress tracking and insights

### User Experience
- **Bilingual Interface**: Complete English and Hindi support
- **Indian Cultural Design**: Flag-themed UI with appropriate styling
- **Progressive Web App**: Install on mobile devices like a native app
- **Responsive Design**: Optimized for desktop, tablet, and mobile

### Technical Features
- **Real-time AI Integration**: OpenAI GPT-4o for content generation
- **Session Management**: Persistent user data during sessions
- **Achievement System**: Badges and points for motivation
- **Data Export/Import**: Backup and restore user progress

## Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-gov-job-prep.git
cd ai-gov-job-prep

# Install dependencies
pip install streamlit streamlit-option-menu openai plotly pandas numpy requests

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the application
streamlit run app.py --server.port 5000
```

### Deployment Options

1. **Streamlit Cloud** (Recommended)
   - Free hosting with easy GitHub integration
   - Automatic HTTPS and custom domains
   - Built-in secret management

2. **Railway**
   - Full-stack deployment platform
   - Automatic scaling and monitoring
   - Custom domain support

3. **PWA Installation**
   - Works on any HTTPS deployment
   - Install on mobile devices
   - Offline capabilities

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## Project Structure

```
ai-gov-job-prep/
├── app.py                 # Main Streamlit application
├── modules/               # Feature modules
│   ├── quiz.py           # AI quiz generation
│   ├── study_plan.py     # Personalized study plans
│   ├── analytics.py      # Performance tracking
│   ├── mock_interview.py # AI interview practice
│   └── current_affairs.py # News and current events
├── utils/                # Utility modules
│   ├── ai_services.py    # OpenAI integration
│   ├── data_manager.py   # Session state management
│   └── language_manager.py # Bilingual content
├── static/               # Static assets
│   ├── manifest.json     # PWA configuration
│   └── sw.js            # Service worker
├── .streamlit/           # Streamlit configuration
│   └── config.toml      # App settings and theme
├── railway.json          # Railway deployment config
├── nixpacks.toml        # Build configuration
└── DEPLOYMENT_GUIDE.md  # Comprehensive deployment guide
```

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here  # Required for AI features
```

### Streamlit Configuration
The app uses Indian flag colors as the theme:
- Primary Color: #FF9933 (Saffron)
- Secondary Color: #138808 (Green)
- Background: #FFFFFF (White)

## Usage Guide

### Setting Up Your Profile
1. Open the application
2. Select your preferred language (English/Hindi)
3. Complete profile setup on the home page
4. Choose your target exam and study schedule

### Taking AI Quizzes
1. Navigate to the AI Quiz section
2. Select topic and difficulty level
3. Choose number of questions (5-20)
4. Generate AI-powered questions
5. Review results and explanations

### Creating Study Plans
1. Go to Study Plan section
2. Ensure profile is complete
3. Generate AI-powered personalized schedule
4. Follow daily, weekly, and monthly goals

### Mock Interviews
1. Access Mock Interview section
2. Choose interview topic and type
3. Answer questions with detailed responses
4. Receive AI-powered feedback and scoring

### Current Affairs Practice
1. Visit Current Affairs section
2. Select news category and time period
3. Generate recent current affairs questions
4. Track your knowledge of recent events

### Analytics Dashboard
1. View comprehensive performance metrics
2. Track progress over time
3. Identify strong and weak topics
4. Monitor study streaks and achievements

## Supported Exam Types

- UPSC Civil Services
- SSC (CGL, CHSL)
- Banking (IBPS, SBI)
- Railway (RRB)
- State PSC
- Teaching (CTET, TET)
- Defense (CDS, NDA)
- Police/Constable
- Other competitive exams

## Quiz Topics Available

### English Topics
- General Knowledge
- Indian History
- Geography
- Indian Polity & Constitution
- Economics
- Current Affairs
- Science & Technology
- Environment & Ecology
- Mathematics
- English Language
- Logical Reasoning
- Computer Knowledge

### Hindi Topics (हिंदी विषय)
- सामान्य ज्ञान
- भारतीय इतिहास
- भूगोल
- भारतीय राजव्यवस्था
- अर्थशास्त्र
- समसामयिकी
- विज्ञान और प्रौद्योगिकी
- पर्यावरण
- गणित
- अंग्रेजी
- तर्कशक्ति
- कंप्यूटर ज्ञान

## Technical Requirements

### Minimum Requirements
- Python 3.11+
- Internet connection for AI features
- Modern web browser
- OpenAI API key

### Recommended Setup
- 4GB RAM
- Stable internet connection
- Chrome/Firefox/Safari browser
- Mobile device for PWA installation

## API Integration

### OpenAI Services Used
- **GPT-4o**: Latest model for question generation
- **Chat Completions**: For interviews and explanations
- **JSON Mode**: Structured response formatting
- **Content Filtering**: Safe, educational content

### Content Generation
- Questions are generated in real-time
- Content is contextually relevant to Indian exams
- Difficulty levels are properly calibrated
- Cultural appropriateness is maintained

## Security & Privacy

### Data Handling
- No permanent user data storage
- Session-based information only
- No personal information collected
- Privacy-focused design

### API Security
- Environment variable protection
- No API keys in code
- Secure token handling
- Rate limiting considerations

## Performance Optimization

### Caching Strategy
- Session state for user data
- Efficient API call management
- Minimal resource usage
- Fast loading times

### Scalability
- Stateless application design
- Horizontal scaling ready
- Efficient memory usage
- Optimized for concurrent users

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow Python PEP 8 standards
- Comment complex logic
- Use meaningful variable names
- Maintain bilingual support

## Support

### Common Issues
- API key configuration
- Import path problems
- PWA installation issues
- Mobile responsiveness

### Getting Help
- Check the deployment guide
- Review configuration files
- Test API key validity
- Verify all dependencies

## License

This project is designed for educational purposes and government job preparation in India.

## Acknowledgments

- OpenAI for AI capabilities
- Streamlit for the web framework
- Indian government exam preparation community
- Contributors and testers

---

**Ready to start your government job preparation journey with AI? Deploy the app and begin studying smarter today!**