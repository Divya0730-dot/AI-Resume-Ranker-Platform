import re
import math
from collections import Counter

class AIEngine:
    def __init__(self):
        pass
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and extra whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_keywords(self, text):
        """Extract important keywords from text"""
        # Common technical keywords and skills
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'node', 'express', 'django', 'flask', 'spring', 'mongodb',
            'mysql', 'postgresql', 'aws', 'azure', 'docker', 'kubernetes',
            'git', 'agile', 'scrum', 'machine learning', 'ai', 'data science',
            'html', 'css', 'bootstrap', 'jquery', 'api', 'rest', 'json',
            'sql', 'nosql', 'redis', 'elasticsearch', 'microservices',
            'devops', 'ci/cd', 'jenkins', 'terraform', 'ansible'
        ]
        
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in tech_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def calculate_keyword_match_score(self, resume_text, job_description):
        """Calculate keyword matching score"""
        resume_keywords = set(self.extract_keywords(resume_text))
        job_keywords = set(self.extract_keywords(job_description))
        
        if not job_keywords:
            return 0
        
        common_keywords = resume_keywords.intersection(job_keywords)
        keyword_score = len(common_keywords) / len(job_keywords)
        
        return min(keyword_score * 100, 100)  # Cap at 100
    
    def calculate_word_frequency_similarity(self, resume_text, job_description):
        """Calculate similarity based on word frequency"""
        try:
            # Preprocess texts
            resume_clean = self.preprocess_text(resume_text)
            job_clean = self.preprocess_text(job_description)
            
            # Get word frequencies
            resume_words = Counter(resume_clean.split())
            job_words = Counter(job_clean.split())
            
            # Calculate common words score
            common_words = set(resume_words.keys()) & set(job_words.keys())
            
            if not common_words:
                return 0
            
            # Calculate weighted similarity
            similarity_score = 0
            total_job_words = sum(job_words.values())
            
            for word in common_words:
                # Weight by frequency in job description
                word_weight = job_words[word] / total_job_words
                similarity_score += word_weight * min(resume_words[word], job_words[word])
            
            return min(similarity_score * 100, 100)
        
        except Exception as e:
            print(f"Word frequency calculation error: {e}")
            return 0
    
    def calculate_text_overlap_score(self, resume_text, job_description):
        """Calculate text overlap score using simple metrics"""
        resume_words = set(self.preprocess_text(resume_text).split())
        job_words = set(self.preprocess_text(job_description).split())
        
        if not job_words:
            return 0
        
        # Jaccard similarity
        intersection = len(resume_words & job_words)
        union = len(resume_words | job_words)
        
        if union == 0:
            return 0
        
        jaccard_score = intersection / union
        return jaccard_score * 100
    
    def rank_resumes(self, resumes, job_description, job_title="", job_position=""):
        """Rank resumes against job description and title with skill recommendations"""
        results = []
        
        # Combine job title and description for better context
        full_job_context = f"{job_title}\n\n{job_description}" if job_title else job_description
        
        for resume in resumes:
            resume_text = resume.get('extracted_text', '')
            
            # Calculate different similarity scores
            word_freq_score = self.calculate_word_frequency_similarity(resume_text, full_job_context)
            keyword_score = self.calculate_keyword_match_score(resume_text, full_job_context)
            overlap_score = self.calculate_text_overlap_score(resume_text, full_job_context)
            
            # Enhanced scoring with job title relevance
            title_relevance = self.calculate_title_relevance(resume_text, job_title) if job_title else 0
            
            # Weighted final score (35% word frequency, 30% keyword matching, 20% overlap, 15% title relevance)
            final_score = (word_freq_score * 0.35) + (keyword_score * 0.30) + (overlap_score * 0.20) + (title_relevance * 0.15)
            final_score = round(final_score, 2)
            
            # Generate skill recommendations
            skill_analysis = self.generate_skill_recommendations(job_title, job_description, resume_text)
            
            # Extract candidate name from file path or use username
            file_path = resume.get('resume_path', '')
            candidate_name = self.extract_candidate_name(file_path, resume.get('username', 'Unknown'))
            
            results.append({
                "candidate_name": candidate_name,
                "score": final_score,
                "resume_id": str(resume.get('_id')),
                "uploaded_at": resume.get('uploaded_at'),
                "tfidf_score": round(word_freq_score, 2),  # Using word frequency as TF-IDF alternative
                "keyword_score": round(keyword_score, 2),
                "title_relevance": round(title_relevance, 2),
                "skill_recommendations": skill_analysis['missing_skills'],
                "existing_skills": skill_analysis['existing_skills'],
                "skills_summary": {
                    "total_missing": skill_analysis['total_missing'],
                    "total_existing": skill_analysis['total_existing'],
                    "skill_match_percentage": round((skill_analysis['total_existing'] / max(skill_analysis['total_existing'] + skill_analysis['total_missing'], 1)) * 100, 2)
                },
                # Enhanced skill analysis data
                "hiring_strategies": skill_analysis.get('hiring_strategies', []),
                "development_plan": skill_analysis.get('development_plan', {}),
                "skill_gap_analysis": {
                    "gap_percentage": round((skill_analysis['total_missing'] / max(skill_analysis['total_missing'] + skill_analysis['total_existing'], 1)) * 100, 2),
                    "investment_recommendation": skill_analysis.get('development_plan', {}).get('investment_recommendation', 'Medium - Moderate training investment needed')
                }
            })
        
        # Sort by score in descending order and add rank
        results.sort(key=lambda x: x['score'], reverse=True)
        
        for i, result in enumerate(results):
            result['rank'] = i + 1
        
        return results
    
    def extract_skills_from_text(self, text):
        """Extract skills from text using keyword matching"""
        # Comprehensive skill database
        skills_database = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
                'spring', 'laravel', 'rails', 'asp.net', 'jquery', 'bootstrap', 'sass', 'less'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sql server',
                'sqlite', 'cassandra', 'dynamodb', 'firebase', 'mariadb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'google cloud', 'gcp', 'heroku', 'digitalocean', 'linode',
                'cloudflare', 'vercel', 'netlify'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions', 'terraform',
                'ansible', 'chef', 'puppet', 'vagrant', 'nginx', 'apache'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'data analysis', 'pandas', 'numpy', 'scikit-learn',
                'tensorflow', 'pytorch', 'keras', 'jupyter', 'tableau', 'power bi', 'spark'
            ],
            'mobile_development': [
                'android', 'ios', 'react native', 'flutter', 'xamarin', 'cordova', 'ionic'
            ],
            'testing': [
                'unit testing', 'integration testing', 'selenium', 'jest', 'pytest', 'junit',
                'cypress', 'postman', 'api testing'
            ],
            'project_management': [
                'agile', 'scrum', 'kanban', 'jira', 'trello', 'asana', 'project management'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
                'time management', 'adaptability', 'creativity'
            ]
        }
        
        text_lower = text.lower()
        found_skills = {}
        
        for category, skills in skills_database.items():
            found_skills[category] = []
            for skill in skills:
                if skill in text_lower:
                    found_skills[category].append(skill)
        
        return found_skills
    
    def generate_skill_recommendations(self, job_title, job_description, resume_text):
        """Generate comprehensive skill recommendations based on job position and description"""
        
        # Extract skills from job requirements
        job_text = f"{job_title} {job_description}"
        required_skills = self.extract_skills_from_text(job_text)
        
        # Extract skills from resume
        candidate_skills = self.extract_skills_from_text(resume_text)
        
        # Find skill gaps and existing skills
        skill_recommendations = []
        existing_skills = []
        
        for category, job_skills in required_skills.items():
            if job_skills:  # Only process categories with required skills
                candidate_category_skills = candidate_skills.get(category, [])
                
                # Track existing skills
                for skill in job_skills:
                    if skill in candidate_category_skills:
                        existing_skills.append({
                            'skill': skill.title(),
                            'category': category.replace('_', ' ').title(),
                            'status': 'existing'
                        })
                
                # Find skills to recommend (skills from job description not in resume)
                recommended_skills = [skill for skill in job_skills if skill not in candidate_category_skills]
                
                if recommended_skills:
                    # Generate recommendations for each skill
                    for skill in recommended_skills:
                        priority = self.calculate_skill_priority(skill, job_text)
                        recommendation = {
                            'skill': skill.title(),
                            'category': category.replace('_', ' ').title(),
                            'priority': priority,
                            'reason': self.generate_skill_reason(skill, job_title, category),
                            'status': 'recommended',
                            'development_strategy': self.generate_development_strategy(skill, category, priority),
                            'learning_resources': self.get_learning_resources(skill, category),
                            'time_estimate': self.estimate_learning_time(skill, category),
                            'alternative_skills': self.suggest_alternative_skills(skill, category)
                        }
                        skill_recommendations.append(recommendation)
        
        # If no specific recommendations from job description, generate position-specific recommendations
        if len(skill_recommendations) == 0:
            skill_recommendations = self.generate_position_specific_recommendations(job_title, job_description, candidate_skills)
        
        # Sort recommendations by priority (high to low)
        skill_recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        # Generate hiring strategy recommendations
        hiring_strategies = self.generate_hiring_strategies(skill_recommendations, existing_skills, job_title)
        
        return {
            'missing_skills': skill_recommendations[:10],  # Top 10 recommended skills
            'existing_skills': existing_skills[:10],       # Top 10 existing skills
            'total_missing': len(skill_recommendations),
            'total_existing': len(existing_skills),
            'hiring_strategies': hiring_strategies,
            'development_plan': self.create_development_plan(skill_recommendations[:5])  # Top 5 for development
        }
    
    def generate_position_specific_recommendations(self, job_title, job_description, candidate_skills):
        """Generate position-specific skill recommendations when job description doesn't have specific skills"""
        
        position_lower = job_title.lower()
        recommendations = []
        
        # Position-specific skill recommendations
        position_skills = {
            'frontend': [
                ('React', 'Web Technologies', 90, 'Modern frontend framework essential for UI development'),
                ('TypeScript', 'Programming Languages', 85, 'Type-safe JavaScript for scalable applications'),
                ('CSS3', 'Web Technologies', 80, 'Advanced styling for responsive designs'),
                ('Webpack', 'DevOps Tools', 75, 'Module bundler for optimized builds'),
                ('Redux', 'Web Technologies', 70, 'State management for complex applications')
            ],
            'backend': [
                ('Node.js', 'Programming Languages', 90, 'Server-side JavaScript runtime'),
                ('PostgreSQL', 'Databases', 85, 'Robust relational database system'),
                ('Docker', 'DevOps Tools', 80, 'Containerization for consistent deployments'),
                ('Redis', 'Databases', 75, 'In-memory caching for performance'),
                ('API Design', 'Web Technologies', 85, 'RESTful API architecture skills')
            ],
            'fullstack': [
                ('React', 'Web Technologies', 90, 'Frontend framework for modern UIs'),
                ('Node.js', 'Programming Languages', 90, 'Backend JavaScript runtime'),
                ('MongoDB', 'Databases', 80, 'NoSQL database for flexible data'),
                ('Docker', 'DevOps Tools', 75, 'Container technology for deployment'),
                ('AWS', 'Cloud Platforms', 85, 'Cloud infrastructure knowledge')
            ],
            'data': [
                ('Python', 'Programming Languages', 95, 'Primary language for data science'),
                ('Pandas', 'Data Science', 90, 'Data manipulation and analysis'),
                ('TensorFlow', 'Data Science', 85, 'Machine learning framework'),
                ('SQL', 'Databases', 90, 'Database querying for data analysis'),
                ('Tableau', 'Data Science', 75, 'Data visualization tool')
            ],
            'devops': [
                ('Kubernetes', 'DevOps Tools', 95, 'Container orchestration platform'),
                ('Terraform', 'DevOps Tools', 90, 'Infrastructure as Code tool'),
                ('AWS', 'Cloud Platforms', 90, 'Cloud platform expertise'),
                ('Jenkins', 'DevOps Tools', 80, 'CI/CD automation tool'),
                ('Ansible', 'DevOps Tools', 75, 'Configuration management')
            ],
            'product': [
                ('Agile', 'Project Management', 90, 'Agile methodology for product development'),
                ('Jira', 'Project Management', 85, 'Project tracking and management'),
                ('Data Analysis', 'Data Science', 80, 'Analytics for product decisions'),
                ('User Research', 'Soft Skills', 85, 'Understanding user needs'),
                ('Roadmap Planning', 'Project Management', 80, 'Strategic product planning')
            ],
            'designer': [
                ('Figma', 'Design Tools', 95, 'Modern design and prototyping tool'),
                ('User Research', 'Soft Skills', 90, 'Understanding user needs and behavior'),
                ('Prototyping', 'Design Tools', 85, 'Interactive prototype creation'),
                ('Design Systems', 'Design Tools', 80, 'Consistent design patterns'),
                ('Accessibility', 'Web Technologies', 85, 'Inclusive design practices')
            ],
            'qa': [
                ('Selenium', 'Testing', 90, 'Automated testing framework'),
                ('API Testing', 'Testing', 85, 'Testing backend services'),
                ('Jest', 'Testing', 80, 'JavaScript testing framework'),
                ('Performance Testing', 'Testing', 75, 'Load and stress testing'),
                ('Test Automation', 'Testing', 85, 'Automated test development')
            ]
        }
        
        # Determine which skill set to use
        selected_skills = []
        if 'frontend' in position_lower or 'front-end' in position_lower:
            selected_skills = position_skills.get('frontend', [])
        elif 'backend' in position_lower or 'back-end' in position_lower:
            selected_skills = position_skills.get('backend', [])
        elif 'fullstack' in position_lower or 'full-stack' in position_lower or 'full stack' in position_lower:
            selected_skills = position_skills.get('fullstack', [])
        elif 'data' in position_lower or 'scientist' in position_lower or 'analyst' in position_lower:
            selected_skills = position_skills.get('data', [])
        elif 'devops' in position_lower or 'sre' in position_lower:
            selected_skills = position_skills.get('devops', [])
        elif 'product' in position_lower and 'manager' in position_lower:
            selected_skills = position_skills.get('product', [])
        elif 'designer' in position_lower or 'ux' in position_lower or 'ui' in position_lower:
            selected_skills = position_skills.get('designer', [])
        elif 'qa' in position_lower or 'quality' in position_lower or 'test' in position_lower:
            selected_skills = position_skills.get('qa', [])
        else:
            # Default software engineering skills
            selected_skills = [
                ('Python', 'Programming Languages', 85, 'Versatile programming language'),
                ('Git', 'DevOps Tools', 90, 'Version control system'),
                ('Docker', 'DevOps Tools', 80, 'Containerization technology'),
                ('AWS', 'Cloud Platforms', 75, 'Cloud platform knowledge'),
                ('Agile', 'Project Management', 70, 'Agile development methodology')
            ]
        
        # Filter out skills the candidate already has
        for skill_name, category, priority, reason in selected_skills:
            # Check if candidate already has this skill
            has_skill = False
            for cat_skills in candidate_skills.values():
                if skill_name.lower() in [s.lower() for s in cat_skills]:
                    has_skill = True
                    break
            
            if not has_skill:
                recommendations.append({
                    'skill': skill_name,
                    'category': category,
                    'priority': priority,
                    'reason': reason,
                    'status': 'recommended',
                    'development_strategy': self.generate_development_strategy(skill_name, category, priority),
                    'learning_resources': self.get_learning_resources(skill_name, category),
                    'time_estimate': self.estimate_learning_time(skill_name, category),
                    'alternative_skills': self.suggest_alternative_skills(skill_name, category)
                })
        
        return recommendations
    
    def calculate_skill_priority(self, skill, job_text):
        """Calculate priority of a skill based on frequency in job description"""
        skill_count = job_text.lower().count(skill.lower())
        
        # High priority skills (mentioned multiple times or critical skills)
        critical_skills = ['python', 'java', 'javascript', 'react', 'aws', 'docker', 'kubernetes']
        
        if skill.lower() in critical_skills:
            return min(skill_count * 20 + 60, 100)
        else:
            return min(skill_count * 15 + 40, 100)
    
    def generate_skill_reason(self, skill, job_title, category):
        """Generate a reason why this skill should be learned"""
        reasons = {
            'programming_languages': f"Essential programming language for {job_title} role",
            'web_technologies': f"Key web technology required for modern {job_title} development",
            'databases': f"Database knowledge crucial for {job_title} data management",
            'cloud_platforms': f"Cloud expertise increasingly important for {job_title} scalability",
            'devops_tools': f"DevOps skills enhance {job_title} deployment and operations",
            'data_science': f"Data analysis capabilities valuable for {job_title} insights",
            'mobile_development': f"Mobile development skills expand {job_title} opportunities",
            'testing': f"Testing expertise ensures quality in {job_title} deliverables",
            'project_management': f"Project management skills enhance {job_title} leadership",
            'soft_skills': f"Soft skills critical for {job_title} success and collaboration"
        }
        
        return reasons.get(category, f"Important skill for {job_title} role advancement")
    
    def calculate_title_relevance(self, resume_text, job_title):
        if not job_title:
            return 0
        
        resume_lower = resume_text.lower()
        title_lower = job_title.lower()
        
        # Extract key terms from job title
        title_words = set(title_lower.split())
        
        # Common job title keywords
        title_keywords = [
            'senior', 'junior', 'lead', 'principal', 'manager', 'director',
            'engineer', 'developer', 'analyst', 'scientist', 'architect',
            'specialist', 'consultant', 'coordinator', 'administrator'
        ]
        
        # Score based on title word matches
        matches = 0
        total_words = len(title_words)
        
        for word in title_words:
            if word in resume_lower:
                matches += 1
        
        # Bonus for job title keywords
        title_keyword_matches = 0
        for keyword in title_keywords:
            if keyword in title_lower and keyword in resume_lower:
                title_keyword_matches += 1
        
        # Calculate relevance score
        word_match_score = (matches / total_words) * 70 if total_words > 0 else 0
        keyword_bonus = min(title_keyword_matches * 10, 30)
        
        return min(word_match_score + keyword_bonus, 100)
    
    def generate_job_description(self, job_position, job_title):
        """Generate a comprehensive job description based on position and title"""
        
        # Normalize the job position for matching
        position_lower = job_position.lower()
        
        # Job description templates based on common positions
        templates = {
            'Software Engineer': {
                'overview': 'We are seeking a talented Software Engineer to join our dynamic development team.',
                'responsibilities': [
                    'Design, develop, and maintain high-quality software applications',
                    'Collaborate with cross-functional teams to define and implement new features',
                    'Write clean, maintainable, and efficient code',
                    'Participate in code reviews and maintain coding standards',
                    'Debug and resolve technical issues',
                    'Stay updated with emerging technologies and industry trends'
                ],
                'required_skills': [
                    'Bachelor\'s degree in Computer Science or related field',
                    'Proficiency in programming languages such as Python, Java, or JavaScript',
                    'Experience with software development methodologies (Agile, Scrum)',
                    'Strong problem-solving and analytical skills',
                    'Knowledge of version control systems (Git)',
                    'Understanding of database systems and SQL'
                ],
                'preferred_skills': [
                    'Experience with cloud platforms (AWS, Azure, GCP)',
                    'Knowledge of containerization (Docker, Kubernetes)',
                    'Familiarity with CI/CD pipelines',
                    'Experience with testing frameworks',
                    'Understanding of software architecture patterns'
                ]
            },
            'Senior Software Engineer': {
                'overview': 'We are looking for an experienced Senior Software Engineer to lead technical initiatives and mentor our development team.',
                'responsibilities': [
                    'Lead the design and architecture of complex software systems',
                    'Mentor junior developers and conduct technical interviews',
                    'Drive technical decision-making and establish best practices',
                    'Collaborate with product managers and stakeholders on technical requirements',
                    'Optimize application performance and scalability',
                    'Lead code reviews and ensure high code quality standards'
                ],
                'required_skills': [
                    '5+ years of software development experience',
                    'Expert-level proficiency in multiple programming languages',
                    'Strong experience with system design and architecture',
                    'Leadership and mentoring experience',
                    'Deep understanding of software engineering principles',
                    'Experience with microservices and distributed systems'
                ],
                'preferred_skills': [
                    'Experience with cloud-native development',
                    'Knowledge of DevOps practices and tools',
                    'Experience with performance optimization',
                    'Understanding of security best practices',
                    'Experience with machine learning or AI technologies'
                ]
            },
            'Full-Stack Developer': {
                'overview': 'Join our team as a Full-Stack Developer to build end-to-end web applications using modern technologies.',
                'responsibilities': [
                    'Develop responsive web applications using modern frontend frameworks',
                    'Build and maintain backend APIs and services',
                    'Design and implement database schemas',
                    'Ensure cross-browser compatibility and mobile responsiveness',
                    'Integrate third-party services and APIs',
                    'Optimize applications for maximum speed and scalability'
                ],
                'required_skills': [
                    'Proficiency in frontend technologies (React, Angular, Vue.js)',
                    'Strong backend development skills (Node.js, Python, Java)',
                    'Experience with databases (SQL and NoSQL)',
                    'Knowledge of RESTful API design and development',
                    'Understanding of web security principles',
                    'Experience with version control and collaborative development'
                ],
                'preferred_skills': [
                    'Experience with cloud deployment and hosting',
                    'Knowledge of containerization and orchestration',
                    'Familiarity with GraphQL',
                    'Experience with testing frameworks and methodologies',
                    'Understanding of UI/UX design principles'
                ]
            },
            'Data Scientist': {
                'overview': 'We are seeking a Data Scientist to extract insights from complex datasets and drive data-driven decision making.',
                'responsibilities': [
                    'Analyze large datasets to identify trends and patterns',
                    'Develop and implement machine learning models',
                    'Create data visualizations and reports for stakeholders',
                    'Collaborate with engineering teams to deploy models to production',
                    'Design and conduct A/B tests and experiments',
                    'Communicate findings to both technical and non-technical audiences'
                ],
                'required_skills': [
                    'Advanced degree in Data Science, Statistics, or related field',
                    'Proficiency in Python or R for data analysis',
                    'Experience with machine learning libraries (scikit-learn, TensorFlow, PyTorch)',
                    'Strong statistical analysis and modeling skills',
                    'Experience with data visualization tools (Matplotlib, Seaborn, Tableau)',
                    'Knowledge of SQL and database systems'
                ],
                'preferred_skills': [
                    'Experience with big data technologies (Spark, Hadoop)',
                    'Knowledge of cloud platforms and MLOps practices',
                    'Experience with deep learning and neural networks',
                    'Understanding of business intelligence tools',
                    'Experience with time series analysis and forecasting'
                ]
            },
            'DevOps Engineer': {
                'overview': 'Join our team as a DevOps Engineer to streamline our development and deployment processes.',
                'responsibilities': [
                    'Design and maintain CI/CD pipelines',
                    'Manage cloud infrastructure and containerized applications',
                    'Implement monitoring and logging solutions',
                    'Automate deployment and scaling processes',
                    'Ensure system security and compliance',
                    'Collaborate with development teams to optimize workflows'
                ],
                'required_skills': [
                    'Experience with cloud platforms (AWS, Azure, GCP)',
                    'Proficiency in containerization (Docker, Kubernetes)',
                    'Knowledge of Infrastructure as Code (Terraform, CloudFormation)',
                    'Experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions)',
                    'Strong scripting skills (Bash, Python)',
                    'Understanding of networking and security principles'
                ],
                'preferred_skills': [
                    'Experience with monitoring tools (Prometheus, Grafana)',
                    'Knowledge of service mesh technologies',
                    'Experience with configuration management tools',
                    'Understanding of database administration',
                    'Experience with security scanning and compliance tools'
                ]
            },
            'Frontend Developer': {
                'overview': 'We are looking for a creative Frontend Developer to build beautiful and intuitive user interfaces.',
                'responsibilities': [
                    'Develop responsive and interactive web applications',
                    'Implement pixel-perfect designs from mockups',
                    'Optimize applications for maximum speed and scalability',
                    'Ensure cross-browser and cross-device compatibility',
                    'Collaborate with designers and backend developers',
                    'Write clean, maintainable, and well-documented code'
                ],
                'required_skills': [
                    'Proficiency in HTML5, CSS3, and JavaScript',
                    'Experience with modern frontend frameworks (React, Vue.js, Angular)',
                    'Understanding of responsive design principles',
                    'Knowledge of CSS preprocessors (SASS, LESS)',
                    'Experience with version control systems',
                    'Strong attention to detail and design aesthetics'
                ],
                'preferred_skills': [
                    'Experience with TypeScript',
                    'Knowledge of state management libraries (Redux, Vuex)',
                    'Familiarity with build tools (Webpack, Vite)',
                    'Understanding of web accessibility standards',
                    'Experience with animation libraries and CSS animations'
                ]
            },
            'Backend Developer': {
                'overview': 'Join our team as a Backend Developer to build robust and scalable server-side applications.',
                'responsibilities': [
                    'Design and develop RESTful APIs and microservices',
                    'Implement business logic and data processing workflows',
                    'Optimize database queries and application performance',
                    'Ensure application security and data protection',
                    'Write comprehensive unit and integration tests',
                    'Collaborate with frontend developers on API integration'
                ],
                'required_skills': [
                    'Proficiency in backend languages (Python, Java, Node.js, Go)',
                    'Experience with database design and management (SQL, NoSQL)',
                    'Knowledge of API design and development',
                    'Understanding of authentication and authorization',
                    'Experience with caching strategies (Redis, Memcached)',
                    'Strong problem-solving and debugging skills'
                ],
                'preferred_skills': [
                    'Experience with message queues (RabbitMQ, Kafka)',
                    'Knowledge of microservices architecture',
                    'Experience with GraphQL',
                    'Understanding of serverless computing',
                    'Experience with performance profiling and optimization'
                ]
            },
            'Product Manager': {
                'overview': 'We are seeking a strategic Product Manager to drive product vision and execution.',
                'responsibilities': [
                    'Define product strategy and roadmap',
                    'Gather and prioritize product requirements',
                    'Work closely with engineering, design, and marketing teams',
                    'Conduct market research and competitive analysis',
                    'Define and track key product metrics',
                    'Communicate product vision to stakeholders'
                ],
                'required_skills': [
                    'Bachelor\'s degree in Business, Computer Science, or related field',
                    '3+ years of product management experience',
                    'Strong analytical and problem-solving skills',
                    'Excellent communication and presentation skills',
                    'Experience with agile development methodologies',
                    'Understanding of user experience principles'
                ],
                'preferred_skills': [
                    'MBA or advanced degree',
                    'Technical background or engineering experience',
                    'Experience with product analytics tools',
                    'Knowledge of A/B testing and experimentation',
                    'Experience in SaaS or technology products'
                ]
            },
            'UI/UX Designer': {
                'overview': 'We are looking for a talented UI/UX Designer to create exceptional user experiences.',
                'responsibilities': [
                    'Design intuitive and visually appealing user interfaces',
                    'Conduct user research and usability testing',
                    'Create wireframes, prototypes, and high-fidelity mockups',
                    'Develop and maintain design systems and style guides',
                    'Collaborate with developers to ensure design implementation',
                    'Iterate designs based on user feedback and analytics'
                ],
                'required_skills': [
                    'Proficiency in design tools (Figma, Sketch, Adobe XD)',
                    'Strong portfolio demonstrating UI/UX design skills',
                    'Understanding of user-centered design principles',
                    'Knowledge of responsive and mobile design',
                    'Experience with prototyping and user testing',
                    'Strong visual design and typography skills'
                ],
                'preferred_skills': [
                    'Experience with motion design and animation',
                    'Knowledge of HTML/CSS basics',
                    'Understanding of accessibility standards',
                    'Experience with design systems',
                    'Knowledge of user research methodologies'
                ]
            },
            'QA Engineer': {
                'overview': 'Join our team as a QA Engineer to ensure the quality and reliability of our products.',
                'responsibilities': [
                    'Design and execute comprehensive test plans',
                    'Develop and maintain automated test suites',
                    'Identify, document, and track software defects',
                    'Perform functional, regression, and performance testing',
                    'Collaborate with developers to resolve issues',
                    'Ensure quality standards are met throughout the development cycle'
                ],
                'required_skills': [
                    'Experience with manual and automated testing',
                    'Knowledge of testing frameworks (Selenium, Jest, Pytest)',
                    'Understanding of software development lifecycle',
                    'Strong analytical and problem-solving skills',
                    'Experience with bug tracking tools (Jira, Bugzilla)',
                    'Attention to detail and quality-focused mindset'
                ],
                'preferred_skills': [
                    'Experience with API testing tools (Postman, REST Assured)',
                    'Knowledge of performance testing tools',
                    'Experience with CI/CD integration',
                    'Understanding of security testing',
                    'Programming skills for test automation'
                ]
            }
        }
        
        # Try to match the position with templates using fuzzy matching
        template = None
        
        # Direct match
        if job_position in templates:
            template = templates[job_position]
        else:
            # Fuzzy match - check if any template key is in the position
            for key in templates.keys():
                if key.lower() in position_lower or position_lower in key.lower():
                    template = templates[key]
                    break
            
            # Check for common variations
            if not template:
                if 'frontend' in position_lower or 'front-end' in position_lower or 'front end' in position_lower:
                    template = templates['Frontend Developer']
                elif 'backend' in position_lower or 'back-end' in position_lower or 'back end' in position_lower:
                    template = templates['Backend Developer']
                elif 'fullstack' in position_lower or 'full-stack' in position_lower or 'full stack' in position_lower:
                    template = templates['Full-Stack Developer']
                elif 'data' in position_lower and ('scientist' in position_lower or 'analyst' in position_lower):
                    template = templates['Data Scientist']
                elif 'devops' in position_lower or 'sre' in position_lower:
                    template = templates['DevOps Engineer']
                elif 'product' in position_lower and 'manager' in position_lower:
                    template = templates['Product Manager']
                elif 'designer' in position_lower or 'ux' in position_lower or 'ui' in position_lower:
                    template = templates['UI/UX Designer']
                elif 'qa' in position_lower or 'quality' in position_lower or 'test' in position_lower:
                    template = templates['QA Engineer']
                elif 'senior' in position_lower or 'lead' in position_lower or 'principal' in position_lower:
                    template = templates['Senior Software Engineer']
                else:
                    # Default to Software Engineer for any other technical position
                    template = templates['Software Engineer']
        
        # Customize the template based on job title
        seniority_level = 'senior' if 'senior' in job_title.lower() or 'lead' in job_title.lower() else 'standard'
        
        # Build the job description
        job_description = f"""
{job_title.upper()} POSITION

ABOUT THE ROLE:
{template['overview']}

KEY RESPONSIBILITIES:
{chr(10).join([f'• {resp}' for resp in template['responsibilities']])}

REQUIRED QUALIFICATIONS:
{chr(10).join([f'• {skill}' for skill in template['required_skills']])}

PREFERRED QUALIFICATIONS:
{chr(10).join([f'• {skill}' for skill in template['preferred_skills']])}

WHAT WE OFFER:
• Competitive salary and comprehensive benefits package
• Flexible work arrangements and remote work options
• Professional development opportunities and learning budget
• Collaborative and innovative work environment
• Opportunity to work with cutting-edge technologies
• Career growth and advancement opportunities

LOCATION: Remote / Hybrid / On-site (flexible)

TO APPLY:
Please submit your resume and a brief cover letter explaining your interest in this position and how your experience aligns with our requirements.

We are an equal opportunity employer committed to diversity and inclusion.
        """.strip()
        
        return job_description
    
    def generate_development_strategy(self, skill, category, priority):
        """Generate specific development strategy for a skill"""
        strategies = {
            'programming_languages': {
                'high': 'Intensive bootcamp or structured course with hands-on projects',
                'medium': 'Online tutorials with practice projects and code reviews',
                'low': 'Self-paced learning with documentation and small projects'
            },
            'web_technologies': {
                'high': 'Build full-stack projects and contribute to open source',
                'medium': 'Follow official tutorials and create portfolio projects',
                'low': 'Complete online courses and practice with simple applications'
            },
            'databases': {
                'high': 'Database administration course with real-world scenarios',
                'medium': 'Practice with sample datasets and query optimization',
                'low': 'Learn basic CRUD operations and database design principles'
            },
            'cloud_platforms': {
                'high': 'Pursue cloud certification with hands-on labs',
                'medium': 'Complete cloud provider training paths',
                'low': 'Start with free tier services and basic deployments'
            },
            'devops_tools': {
                'high': 'Set up complete CI/CD pipeline for personal projects',
                'medium': 'Practice with containerization and automation scripts',
                'low': 'Learn basic concepts through online tutorials'
            },
            'data_science': {
                'high': 'Complete data science specialization with capstone project',
                'medium': 'Work on Kaggle competitions and data analysis projects',
                'low': 'Learn statistical concepts and basic data visualization'
            },
            'soft_skills': {
                'high': 'Leadership training program and mentoring opportunities',
                'medium': 'Join professional groups and practice presentations',
                'low': 'Read relevant books and practice in daily interactions'
            }
        }
        
        priority_level = 'high' if priority >= 80 else 'medium' if priority >= 60 else 'low'
        return strategies.get(category, {}).get(priority_level, 'Structured learning with practical application')
    
    def get_learning_resources(self, skill, category):
        """Get specific learning resources for a skill"""
        resources = {
            'python': ['Python.org Tutorial', 'Codecademy Python', 'Real Python', 'Python Crash Course book'],
            'javascript': ['MDN Web Docs', 'JavaScript.info', 'FreeCodeCamp', 'Eloquent JavaScript book'],
            'react': ['React Official Docs', 'React Tutorial', 'Scrimba React Course', 'React Hooks Tutorial'],
            'aws': ['AWS Training', 'A Cloud Guru', 'AWS Certified Solutions Architect', 'AWS Free Tier'],
            'docker': ['Docker Official Tutorial', 'Docker Mastery Course', 'Play with Docker', 'Docker Deep Dive book'],
            'machine learning': ['Coursera ML Course', 'Fast.ai', 'Kaggle Learn', 'Hands-On ML book'],
            'sql': ['SQLBolt', 'W3Schools SQL', 'HackerRank SQL', 'SQL Zoo'],
            'git': ['Git Tutorial', 'Atlassian Git Tutorials', 'Pro Git book', 'GitHub Learning Lab']
        }
        
        skill_lower = skill.lower()
        return resources.get(skill_lower, ['Online courses', 'Official documentation', 'Practice projects', 'Community forums'])
    
    def estimate_learning_time(self, skill, category):
        """Estimate time needed to learn a skill"""
        time_estimates = {
            'programming_languages': '3-6 months',
            'web_technologies': '2-4 months',
            'databases': '2-3 months',
            'cloud_platforms': '3-5 months',
            'devops_tools': '2-4 months',
            'data_science': '4-8 months',
            'mobile_development': '3-6 months',
            'testing': '1-3 months',
            'project_management': '2-4 months',
            'soft_skills': '3-6 months'
        }
        
        return time_estimates.get(category, '2-4 months')
    
    def suggest_alternative_skills(self, skill, category):
        """Suggest alternative skills that could substitute"""
        alternatives = {
            'python': ['Java', 'JavaScript', 'C#'],
            'react': ['Angular', 'Vue.js', 'Svelte'],
            'aws': ['Azure', 'Google Cloud', 'DigitalOcean'],
            'docker': ['Podman', 'LXC', 'Vagrant'],
            'mysql': ['PostgreSQL', 'MongoDB', 'SQLite'],
            'jenkins': ['GitLab CI', 'GitHub Actions', 'CircleCI'],
            'kubernetes': ['Docker Swarm', 'Nomad', 'ECS']
        }
        
        skill_lower = skill.lower()
        return alternatives.get(skill_lower, ['Similar technologies in the same category'])
    
    def generate_hiring_strategies(self, missing_skills, existing_skills, job_title):
        """Generate alternative hiring strategies based on skill gaps"""
        strategies = []
        
        # Calculate skill gap severity
        total_required = len(missing_skills) + len(existing_skills)
        missing_count = len(missing_skills)
        gap_percentage = (missing_count / total_required * 100) if total_required > 0 else 0
        
        # High-priority missing skills
        critical_missing = [skill for skill in missing_skills if skill.get('priority', 0) >= 80]
        
        if gap_percentage <= 20:
            strategies.append({
                'strategy': 'Hire and Train',
                'description': 'Candidate has strong foundation. Provide targeted training for missing skills.',
                'timeline': '2-3 months',
                'success_probability': 'High (85-95%)',
                'investment': 'Low to Medium',
                'recommendation': 'Recommended - Good cultural and technical fit'
            })
        elif gap_percentage <= 40:
            strategies.append({
                'strategy': 'Structured Development Program',
                'description': 'Implement comprehensive training program with mentorship.',
                'timeline': '4-6 months',
                'success_probability': 'Medium-High (70-85%)',
                'investment': 'Medium',
                'recommendation': 'Consider if candidate shows strong learning ability'
            })
        elif gap_percentage <= 60:
            strategies.append({
                'strategy': 'Junior Role with Growth Path',
                'description': 'Hire for junior position with clear advancement criteria.',
                'timeline': '6-12 months',
                'success_probability': 'Medium (60-75%)',
                'investment': 'Medium to High',
                'recommendation': 'Suitable if long-term investment is acceptable'
            })
        else:
            strategies.append({
                'strategy': 'Alternative Role Consideration',
                'description': 'Consider for different role that better matches existing skills.',
                'timeline': 'Immediate',
                'success_probability': 'Variable',
                'investment': 'Low',
                'recommendation': 'Explore other positions within organization'
            })
        
        # Add specific strategies based on critical missing skills
        if len(critical_missing) > 3:
            strategies.append({
                'strategy': 'Team Pairing Strategy',
                'description': 'Pair with senior team member to accelerate learning of critical skills.',
                'timeline': '3-6 months',
                'success_probability': 'Medium-High (75-85%)',
                'investment': 'Medium',
                'recommendation': 'Effective for motivated candidates with good fundamentals'
            })
        
        # Add contract-to-hire option
        strategies.append({
            'strategy': 'Contract-to-Hire Evaluation',
            'description': 'Start with contract position to evaluate learning progress and fit.',
            'timeline': '3-6 months evaluation',
            'success_probability': 'High evaluation accuracy',
            'investment': 'Low initial risk',
            'recommendation': 'Reduces hiring risk while providing opportunity'
        })
        
        return strategies
    
    def create_development_plan(self, top_missing_skills):
        """Create a structured development plan for top missing skills"""
        if not top_missing_skills:
            return {'phases': [], 'total_timeline': '0 months', 'success_factors': []}
        
        phases = []
        current_month = 0
        
        # Group skills by learning complexity and dependencies
        quick_wins = [skill for skill in top_missing_skills if skill.get('priority', 0) < 60]
        medium_skills = [skill for skill in top_missing_skills if 60 <= skill.get('priority', 0) < 80]
        critical_skills = [skill for skill in top_missing_skills if skill.get('priority', 0) >= 80]
        
        # Phase 1: Quick wins and foundational skills
        if quick_wins:
            phases.append({
                'phase': 1,
                'title': 'Foundation Building',
                'duration': '1-2 months',
                'skills': [skill['skill'] for skill in quick_wins[:2]],
                'focus': 'Build confidence with achievable goals',
                'milestones': ['Complete basic tutorials', 'Build simple project', 'Pass skill assessment']
            })
            current_month += 2
        
        # Phase 2: Medium priority skills
        if medium_skills:
            phases.append({
                'phase': 2,
                'title': 'Skill Development',
                'duration': '2-4 months',
                'skills': [skill['skill'] for skill in medium_skills[:2]],
                'focus': 'Develop practical competency',
                'milestones': ['Complete intermediate projects', 'Contribute to team tasks', 'Demonstrate proficiency']
            })
            current_month += 3
        
        # Phase 3: Critical skills
        if critical_skills:
            phases.append({
                'phase': 3,
                'title': 'Advanced Mastery',
                'duration': '3-6 months',
                'skills': [skill['skill'] for skill in critical_skills[:2]],
                'focus': 'Achieve job-ready proficiency',
                'milestones': ['Lead project using skills', 'Mentor others', 'Meet performance standards']
            })
            current_month += 4
        
        success_factors = [
            'Regular progress reviews and feedback',
            'Hands-on project experience',
            'Mentorship and peer support',
            'Clear learning objectives and milestones',
            'Practical application opportunities'
        ]
        
        return {
            'phases': phases,
            'total_timeline': f'{current_month} months',
            'success_factors': success_factors,
            'investment_recommendation': self.calculate_investment_recommendation(top_missing_skills)
        }
    
    def calculate_investment_recommendation(self, missing_skills):
        """Calculate recommended investment level for candidate development"""
        if not missing_skills:
            return 'Low - Minimal training needed'
        
        avg_priority = sum(skill.get('priority', 0) for skill in missing_skills) / len(missing_skills)
        skill_count = len(missing_skills)
        
        if avg_priority >= 80 or skill_count >= 4:
            return 'High - Significant training investment required'
        elif avg_priority >= 60 or skill_count >= 2:
            return 'Medium - Moderate training investment needed'
        else:
            return 'Low - Minimal training investment needed'
    
    def extract_candidate_name(self, file_path, username, extracted_text=None):
        """Extract candidate name from resume text or file path"""
        try:
            # First, try to extract from resume text content
            if extracted_text:
                name_from_text = self._extract_name_from_text(extracted_text)
                if name_from_text:
                    return name_from_text
            
            # If no name found in text, return a generic placeholder
            # DO NOT use filename as it should be different from candidate name
            return "Candidate Name Not Found"
        except:
            return "Candidate Name Not Found"
    
    def _extract_name_from_text(self, text):
        """Extract candidate name from resume text content"""
        if not text:
            return None
        
        # Get first few lines where name is usually located
        lines = text.strip().split('\n')[:20]
        
        # Common patterns for names
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip lines with email, phone, or URLs
            if '@' in line or 'http' in line.lower() or any(char.isdigit() for char in line if line.count(char) > 3):
                continue
            
            # Skip common headers and keywords
            skip_words = ['resume', 'curriculum', 'vitae', 'cv', 'profile', 'contact', 
                         'email', 'phone', 'address', 'objective', 'summary', 'experience',
                         'education', 'skills', 'professional', 'personal', 'details',
                         'linkedin', 'github', 'portfolio', 'website', 'location', 'city']
            if any(word in line.lower() for word in skip_words):
                continue
            
            # Look for name pattern (2-4 words, capitalized, mostly letters)
            words = line.split()
            if 2 <= len(words) <= 4:
                # Check if words look like a name (capitalized, mostly letters)
                valid_words = []
                for word in words:
                    # Remove common punctuation
                    clean_word = word.strip('.,;:()[]{}"\'-')
                    # Check if it's a valid name word (starts with capital, mostly letters)
                    if (clean_word and 
                        len(clean_word) >= 2 and 
                        clean_word[0].isupper() and 
                        sum(c.isalpha() for c in clean_word) >= len(clean_word) * 0.8):
                        valid_words.append(clean_word)
                
                # If we have 2-4 valid name words, return them
                if 2 <= len(valid_words) <= 4:
                    full_name = ' '.join(valid_words)
                    # Make sure it's not too long and looks like a real name
                    if len(full_name) <= 50:
                        return full_name
        
        return None