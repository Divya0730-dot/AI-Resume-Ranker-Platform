# AI Resume Ranker - Full-Stack Web Application

A comprehensive AI-powered resume ranking system that allows users to upload resumes and rank them against job descriptions using advanced NLP techniques.

## 🚀 Features

- **User Authentication**: Secure registration and login with bcrypt password hashing
- **Resume Upload**: Support for PDF and DOCX files with text extraction
- **AI-Powered Ranking**: Intelligent resume ranking using keyword matching and text similarity
- **Modern UI**: Professional, responsive design with smooth animations
- **API-Level Validation**: Comprehensive frontend and backend validation
- **Real-time Feedback**: Live password strength checking and instant error messages

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: MongoDB (with in-memory fallback)
- **AI/NLP**: Custom text analysis algorithms
- **File Processing**: PyPDF2, python-docx
- **Security**: bcrypt password hashing

## 📋 Prerequisites

- Python 3.8+
- MongoDB (optional - app works with in-memory storage)
- Modern web browser

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-ranker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   # Create .env file
   SECRET_KEY=your-secret-key
   MONGO_URI=mongodb://localhost:27017/resume_ranker
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 🎯 Usage

### 1. Registration
- Navigate to the registration page
- Fill in your details with a strong password
- Password must contain:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character

### 2. Login
- Use your registered credentials to log in
- Access the dashboard upon successful authentication

### 3. Upload Resumes
- Drag and drop PDF or DOCX files
- Or click to browse and select files
- Multiple files can be uploaded at once

### 4. Rank Resumes
- Enter a job description in the text area
- Click "Rank Resumes" to analyze
- View results with scores and rankings

## 🏗️ Project Structure

```
resume-ranker/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── services/
│   ├── __init__.py
│   ├── database.py       # Database operations
│   ├── ai_engine.py      # AI ranking algorithms
│   └── file_handler.py   # File upload and text extraction
├── templates/
│   ├── register.html     # Registration page
│   ├── login.html        # Login page
│   └── dashboard.html    # Main dashboard
├── uploads/              # Uploaded resume files
└── .env/                 # Environment variables
```

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **Input Validation**: Frontend and backend validation
- **File Security**: Secure file upload with type checking
- **Session Management**: Flask sessions for authentication
- **CORS Protection**: Configured for secure API access

## 🤖 AI Ranking Algorithm

The system uses multiple techniques to rank resumes:

1. **Keyword Matching**: Identifies technical skills and relevant terms
2. **Word Frequency Analysis**: Analyzes word importance and frequency
3. **Text Overlap**: Calculates similarity between resume and job description
4. **Weighted Scoring**: Combines multiple metrics for final score

## 📊 API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User authentication
- `POST /api/upload-resume` - Resume file upload
- `POST /api/rank-resumes` - Resume ranking
- `POST /api/logout` - User logout

## 🎨 UI Features

- **Modern Design**: Professional SaaS-style interface
- **Responsive Layout**: Works on desktop and mobile
- **Real-time Validation**: Live password strength checking
- **Smooth Animations**: Enhanced user experience
- **Progress Indicators**: Visual feedback for operations

## 🚀 Deployment

For production deployment:

1. Set up MongoDB instance
2. Configure environment variables
3. Use a production WSGI server (gunicorn, uWSGI)
4. Set up reverse proxy (nginx)
5. Enable HTTPS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues or have questions, please create an issue in the repository.