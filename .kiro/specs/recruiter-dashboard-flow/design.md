# Recruiter Dashboard Flow - Design Document

## Architecture Overview

The Recruiter Dashboard Flow will be implemented as a single-page application with progressive enhancement, featuring a step-by-step wizard interface that guides users through the complete resume ranking process.

## System Components

### 1. Frontend Components

#### Dashboard Controller (`templates/dashboard.html`)
- **Purpose**: Main dashboard interface with step-by-step navigation
- **Responsibilities**:
  - Manage step progression and validation
  - Handle form data persistence across steps
  - Coordinate file uploads and AI ranking
  - Display results and progress indicators

#### Step Components
1. **Job Title Step**: Simple text input with validation
2. **Job Description Step**: Textarea with rich validation
3. **File Selection Step**: Drag-and-drop interface with file management
4. **Upload Processing Step**: Batch upload with progress tracking
5. **Ranking Step**: AI processing trigger and results display

#### Progress Indicator Component
- Visual step tracker showing current position
- Completed steps marked with checkmarks
- Interactive navigation for completed steps

### 2. Backend Components

#### Authentication System (`app.py`)
- **Enhanced Login API**: Proper error distinction between registration and login
- **Role-Based Access Control**: Dashboard access based on user role
- **Session Management**: Secure session handling across dashboard steps
- **User Validation**: Comprehensive input validation and error handling
- **Registration Enhancement**: Role selection and storage

#### File Processing System (`services/file_handler.py`)
- **Multi-file Upload**: Batch processing of resume files
- **Format Validation**: Strict PDF/DOCX validation
- **Text Extraction**: Enhanced text processing for better AI input

#### AI Ranking Engine (`services/ai_engine.py`)
- **Enhanced Algorithm**: Job title relevance integration
- **Multi-factor Scoring**: Weighted algorithm with four factors
- **Result Formatting**: Structured output for frontend display

#### Database Layer (`services/database.py`)
- **User Management**: Secure user data handling with role support
- **Resume Storage**: Efficient file metadata and content storage
- **Session Persistence**: Dashboard state management
- **Role-Based Queries**: User filtering by role

## Data Flow Design

### 1. Authentication Flow
```
User Access → Route Check → Authentication Status
├── Not Authenticated → Redirect to Register/Login
│   ├── New User → Register (Select Role) → Login → Role Check → Dashboard
│   └── Existing User → Login → Role Check → Dashboard
└── Authenticated → Role Validation → Load Appropriate Dashboard
```

### 2. Dashboard Step Flow
```
Step 1 (Job Title) → Validation → Step 2 (Job Description)
                                      ↓
Step 5 (Ranking) ← Step 4 (Upload) ← Step 3 (File Selection)
```

### 3. Data Persistence
- **Client-side**: JavaScript variables for current session
- **Server-side**: Session storage for user state
- **Database**: Permanent storage for uploaded resumes and results

## API Design

### Enhanced Endpoints

#### `POST /api/login`
**Enhanced Error Handling with Role Support**:
```json
// Success Response
{
  "message": "Login successful",
  "role": "Recruiter",
  "redirect": "/dashboard"
}

// Error Response (Login)
{
  "error": "Invalid username or password"
}

// Error Response (Role Access)
{
  "error": "Access denied for this role"
}
```

#### `POST /api/register`
**Enhanced with Role Selection**:
```json
// Request
{
  "fullname": "John Doe",
  "username": "johndoe",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "role": "Recruiter"
}

// Success Response
{
  "message": "User registered successfully",
  "redirect": "/login"
}

// Error Response (Registration)
{
  "error": "User already exists"
}

// Error Response (Role Required)
{
  "error": "Role selection is required"
}
```

#### `POST /api/upload-resume`
**Batch Upload Support**:
```json
// Success Response
{
  "message": "Resume uploaded successfully",
  "file_id": "unique_file_id",
  "extracted_text_length": 1250
}
```

#### `POST /api/rank-resumes`
**Enhanced with Job Title**:
```json
// Request
{
  "job_title": "Senior Software Engineer",
  "job_description": "Detailed job requirements..."
}

// Response
{
  "results": [
    {
      "candidate_name": "John Doe",
      "score": 87.5,
      "rank": 1,
      "tfidf_score": 82.3,
      "keyword_score": 91.2,
      "title_relevance": 89.7,
      "resume_id": "resume_123"
    }
  ]
}
```

## User Interface Design

### 1. Visual Hierarchy

#### Progress Indicator
```
[1] ——— [2] ——— [3] ——— [4] ——— [5]
 ✓       ✓       •       ○       ○
Job     Job     Upload  Upload  Rank
Title   Desc    Files   Process Results
```

#### Step Cards
- **Active Step**: Highlighted with primary color border
- **Completed Steps**: Green checkmark, accessible for editing
- **Future Steps**: Disabled/grayed out
- **Navigation**: Back/Next buttons with smart enabling

### 2. Responsive Design

#### Desktop Layout
- Full-width step cards with side-by-side navigation
- Large progress indicator at top
- Detailed file upload interface

#### Mobile Layout
- Stacked step cards
- Compact progress indicator
- Touch-friendly file upload

### 3. Interaction Design

#### Step Transitions
- Smooth animations between steps
- Form validation before progression
- Data persistence across navigation
- Loading states for async operations

#### File Upload UX
- Drag-and-drop visual feedback
- File list with remove options
- Upload progress indicators
- Error handling for invalid files

## Security Design

### 1. Authentication Security
- **Password Hashing**: bcrypt with 12 salt rounds
- **Session Management**: Secure Flask sessions
- **Input Validation**: Server-side validation for all inputs
- **CSRF Protection**: Built-in Flask CSRF handling

### 2. File Upload Security
- **Format Validation**: Strict PDF/DOCX checking
- **Size Limits**: 16MB maximum per file
- **Secure Storage**: Isolated upload directory
- **Filename Sanitization**: Prevent directory traversal

### 3. Data Protection
- **User Isolation**: Users can only access their own data
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Template escaping
- **Secure Headers**: Content Security Policy

## Performance Design

### 1. Frontend Optimization
- **Progressive Loading**: Load steps as needed
- **Client-side Validation**: Immediate feedback
- **Efficient DOM Updates**: Minimal reflows
- **Caching**: Static asset caching

### 2. Backend Optimization
- **Async Processing**: Non-blocking file uploads
- **Database Indexing**: Optimized queries
- **Memory Management**: Efficient text processing
- **Connection Pooling**: Database connection optimization

### 3. AI Processing Optimization
- **Batch Processing**: Multiple resumes at once
- **Caching**: Repeated job description analysis
- **Efficient Algorithms**: Optimized similarity calculations
- **Memory Usage**: Streaming text processing

## Error Handling Design

### 1. User-Facing Errors
- **Clear Messages**: Non-technical language
- **Contextual Help**: Specific guidance for resolution
- **Visual Indicators**: Color-coded error states
- **Recovery Options**: Clear paths to fix issues

### 2. System Error Handling
- **Graceful Degradation**: Fallback options
- **Logging**: Comprehensive error tracking
- **Monitoring**: Performance and error metrics
- **Recovery**: Automatic retry mechanisms

## Testing Strategy

### 1. Unit Testing
- **Authentication Logic**: Login/registration flows
- **File Processing**: Upload and text extraction
- **AI Algorithm**: Ranking accuracy
- **Database Operations**: CRUD operations

### 2. Integration Testing
- **End-to-End Flow**: Complete dashboard workflow
- **API Testing**: All endpoint functionality
- **File Upload Testing**: Various file types and sizes
- **Cross-browser Testing**: Compatibility verification

### 3. User Acceptance Testing
- **Usability Testing**: Step-by-step flow intuition
- **Performance Testing**: Load times and responsiveness
- **Accessibility Testing**: Screen reader compatibility
- **Mobile Testing**: Touch interface functionality

## Deployment Considerations

### 1. Environment Configuration
- **Development**: Local MongoDB, debug enabled
- **Production**: Secure database, optimized settings
- **Environment Variables**: Secure configuration management

### 2. Scalability
- **Database Scaling**: MongoDB replica sets
- **File Storage**: Distributed file system
- **Load Balancing**: Multiple application instances
- **Caching**: Redis for session storage

### 3. Monitoring
- **Application Metrics**: Response times, error rates
- **User Analytics**: Step completion rates
- **Performance Monitoring**: Resource usage
- **Error Tracking**: Comprehensive logging

## Implementation Phases

### Phase 1: Core Authentication
- Enhanced login/registration error handling
- Session management improvements
- Basic dashboard structure

### Phase 2: Step-by-Step Interface
- Progress indicator implementation
- Step navigation logic
- Form validation and persistence

### Phase 3: File Upload Enhancement
- Multi-file selection interface
- Batch upload processing
- Progress tracking and error handling

### Phase 4: AI Integration
- Job title relevance algorithm
- Enhanced scoring system
- Results display optimization

### Phase 5: Polish and Testing
- UI/UX refinements
- Performance optimization
- Comprehensive testing
- Documentation completion

## Success Criteria

### Technical Metrics
- **Page Load Time**: < 2 seconds
- **File Upload Success Rate**: > 99%
- **AI Processing Time**: < 10 seconds for 10 resumes
- **Error Rate**: < 1% for valid operations

### User Experience Metrics
- **Step Completion Rate**: > 95%
- **User Satisfaction**: > 4.5/5 rating
- **Support Tickets**: < 5% of users need help
- **Return Usage**: > 80% of users return within 30 days

This design provides a comprehensive foundation for implementing the Recruiter Dashboard Flow with all specified requirements while ensuring scalability, security, and excellent user experience.