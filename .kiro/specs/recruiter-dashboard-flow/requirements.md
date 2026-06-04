# Recruiter Dashboard Flow - Requirements Specification

## Overview
Create an intuitive, step-by-step recruiter dashboard that guides users through the complete resume ranking process, from job definition to AI-powered candidate evaluation.

## User Stories

### Epic: Step-by-Step Dashboard Experience
**As a recruiter**, I want a guided dashboard experience that walks me through the resume ranking process step-by-step, so that I can efficiently evaluate candidates without confusion or missing critical steps.

### Story 1: Sequential Job Information Collection
**As a recruiter**, I want to enter job details in a logical sequence (title first, then description), so that I can build a complete job profile before uploading resumes.

### Story 2: Guided Resume Upload Process
**As a recruiter**, I want a clear upload process that shows me when files are selected vs. when they're actually uploaded to the system, so that I understand the difference between file selection and system processing.

### Story 3: Intuitive Ranking Workflow
**As a recruiter**, I want a final ranking step that uses all my previously entered information, so that I can see how candidates match against my specific job requirements.

### Story 4: Seamless Authentication Experience
**As a returning recruiter**, I want to log in directly without registration barriers, so that I can quickly access my dashboard and start ranking candidates.

### Story 5: Clear Registration vs Login Distinction
**As a new recruiter**, I want clear messaging that distinguishes between registration errors and login errors, so that I'm not confused about whether I need to register or just log in.

### Story 6: Role-Based Registration
**As a new user**, I want to select my role (Recruiter) during registration, so that the system can provide me with the appropriate dashboard and functionality based on my role.

## Acceptance Criteria

### 1. Dashboard Flow Sequence
**Given** a recruiter has successfully logged in  
**When** they access the dashboard  
**Then** they should see a step-by-step interface with the following sequence:
1. Job Title entry (Step 1)
2. Job Description entry (Step 2)  
3. Resume file selection (Step 3)
4. Upload confirmation and processing (Step 4)
5. Ranking execution (Step 5)

### 2. Step Progression Logic
**Given** a recruiter is on any step of the dashboard  
**When** they attempt to proceed to the next step  
**Then** the current step must be completed and validated before progression is allowed

**And** they should be able to navigate back to previous steps to make changes

### 3. Job Title Validation
**Given** a recruiter is on Step 1 (Job Title)  
**When** they click "Next" without entering a job title  
**Then** they should see an error message "Please enter a job title"  
**And** they should remain on Step 1

**When** they enter a valid job title and click "Next"  
**Then** they should progress to Step 2 (Job Description)  
**And** Step 1 should be marked as completed

### 4. Job Description Validation
**Given** a recruiter is on Step 2 (Job Description)  
**When** they click "Next" without entering a job description  
**Then** they should see an error message "Please enter a job description"  
**And** they should remain on Step 2

**When** they enter a valid job description and click "Next"  
**Then** they should progress to Step 3 (Resume Upload)  
**And** Step 2 should be marked as completed

### 5. Resume File Selection
**Given** a recruiter is on Step 3 (Resume Upload)  
**When** they select PDF or DOCX files  
**Then** the files should be displayed in a list with file names and sizes  
**And** they should be able to remove individual files  
**And** the "Next" button should only be enabled when at least one file is selected

**When** they try to select non-PDF/DOCX files  
**Then** they should see an error message about invalid file formats  
**And** only valid files should be added to the selection

### 6. Upload Processing Step
**Given** a recruiter has selected files and progressed to Step 4  
**When** they click "Upload All Resumes"  
**Then** they should see a progress indicator for each file being uploaded  
**And** they should see success/failure status for each file  
**And** the "Next" button should only be enabled after all files are successfully uploaded

### 7. Resume Ranking Execution
**Given** a recruiter has completed all previous steps and is on Step 5  
**When** they click "Rank All Resumes"  
**Then** the system should use both the job title and job description for ranking  
**And** they should see a loading indicator during processing  
**And** results should be displayed with candidate names, scores, and rankings

### 8. Existing User Login Behavior
**Given** a user account already exists in the system  
**When** the user enters their correct username and password on the login page  
**Then** they should be successfully logged in  
**And** they should be redirected to the dashboard  
**And** they should NOT see any "User already exists" message

### 9. New User Registration Flow
**Given** a new user wants to create an account  
**When** they access the application  
**Then** they should be redirected to the registration page first  
**And** after successful registration, they should be redirected to the login page  
**And** after successful login, they should access the dashboard

### 10. Registration Error Handling
**Given** a user tries to register with an existing username  
**When** they submit the registration form  
**Then** they should see "User already exists" message  
**And** they should remain on the registration page  
**And** they should be able to edit their details and try again  
**And** their form data should be preserved (except password fields)

### 11. Login Error Distinction
**Given** a user is on the login page  
**When** they enter incorrect credentials  
**Then** they should see "Invalid username or password" message  
**And** they should NOT see "User already exists" message  
**And** they should remain on the login page to retry

### 12. Visual Progress Indication
**Given** a recruiter is using the dashboard  
**When** they are on any step  
**Then** they should see a visual progress indicator showing:
- Current step highlighted
- Completed steps marked with checkmarks
- Future steps shown but not accessible
- Clear step numbers and titles

### 13. Navigation Controls
**Given** a recruiter is on any step (except Step 1)  
**When** they want to make changes to previous steps  
**Then** they should see a "Back" button that allows them to return to previous steps  
**And** their previously entered data should be preserved  
**And** they should be able to navigate forward again after making changes

### 14. Enhanced AI Ranking
**Given** a recruiter has provided both job title and job description  
**When** the ranking process executes  
**Then** the AI should consider both job title relevance and description matching  
**And** results should show detailed scoring breakdown  
**And** candidates should be ranked from highest to lowest match score

### 15. Responsive Design
**Given** a recruiter accesses the dashboard on any device  
**When** they use the step-by-step interface  
**Then** the layout should be responsive and usable on desktop, tablet, and mobile devices  
**And** all functionality should work consistently across devices

### 16. Role Selection During Registration
**Given** a new user is on the registration page  
**When** they fill out the registration form  
**Then** they should see a "Select Role" field with "Recruiter" as an option  
**And** they must select a role before registration can be completed  
**And** the selected role should be stored in the database

### 17. Role-Based Dashboard Access
**Given** a user has registered with the "Recruiter" role  
**When** they successfully log in  
**Then** they should be redirected to the Recruiter Dashboard  
**And** they should have access to all recruiter-specific features

### 18. Role Validation
**Given** a user attempts to access the recruiter dashboard  
**When** the system checks their role  
**Then** only users with "Recruiter" role should have access  
**And** users without proper role should be redirected appropriately

## Technical Requirements

### Authentication
- Secure session management
- Proper bcrypt password hashing
- Clear distinction between registration and login errors
- Session persistence across dashboard steps
- Role-based access control
- Role selection and storage during registration

### File Handling
- Support for PDF and DOCX files only
- File size validation (max 16MB per file)
- Multiple file selection and upload
- Secure file storage and text extraction

### AI Processing
- Integration of job title into ranking algorithm
- Enhanced scoring with multiple factors:
  - Word frequency similarity (35%)
  - Keyword matching (30%)
  - Text overlap (20%)
  - Job title relevance (15%)

### User Interface
- Modern, professional design
- Clear visual hierarchy
- Intuitive navigation
- Loading states and progress indicators
- Error handling with user-friendly messages

### Performance
- Efficient file upload processing
- Responsive AI ranking
- Smooth step transitions
- Minimal loading times

## Success Metrics
- Users complete the full dashboard flow without confusion
- Reduced support requests about the ranking process
- High user satisfaction with the step-by-step guidance
- Successful authentication for both new and existing users
- Accurate resume rankings using enhanced AI algorithm

## Dependencies
- Flask web framework
- MongoDB database
- bcrypt for password hashing
- File processing libraries (PyPDF2, python-docx)
- Custom AI ranking engine

## Constraints
- Must maintain backward compatibility with existing user accounts
- File uploads limited to PDF and DOCX formats
- Dashboard must work without JavaScript for basic functionality
- All user data must be securely handled and stored