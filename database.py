from pymongo import MongoClient
from config import Config
from datetime import datetime, timezone
import os

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client.resume_ranker
            self.users = self.db.users
            self.resumes = self.db.resumes
            
            # Drop any existing problematic indexes
            try:
                self.users.drop_index("email_1")
                print("🗑️ Dropped problematic email index")
            except:
                pass  # Index might not exist
            
            # Create only the username unique index
            try:
                self.users.create_index("username", unique=True)
                print("✅ Created username unique index")
            except:
                pass  # Index might already exist
                
            self.mongo_available = True
            print("✅ MongoDB connected successfully")
        except Exception as e:
            print(f"⚠️ MongoDB not available, using in-memory storage: {e}")
            self.mongo_available = False
            # Fallback to in-memory storage
            self.users_memory = {}
            self.resumes_memory = []
    
    def user_exists(self, username):
        """Check if user exists in database"""
        if self.mongo_available:
            return self.users.find_one({"username": username}) is not None
        else:
            return username in self.users_memory
    
    def create_user(self, user_data):
        """Create a new user"""
        if self.mongo_available:
            return self.users.insert_one(user_data)
        else:
            # For in-memory storage, ensure password is stored as bytes for consistency
            user_data_copy = user_data.copy()
            if isinstance(user_data_copy['password'], str):
                user_data_copy['password'] = user_data_copy['password'].encode('utf-8')
            self.users_memory[user_data['username']] = user_data_copy
            return True
    
    def get_user(self, username):
        """Get user by username"""
        if self.mongo_available:
            return self.users.find_one({"username": username})
        else:
            return self.users_memory.get(username)
    
    def get_resume_by_id(self, resume_id):
        """Get resume by ID"""
        try:
            from bson import ObjectId
            resume = self.db.resumes.find_one({"_id": ObjectId(resume_id)})
            return resume
        except Exception as e:
            print(f"Error getting resume by ID: {e}")
            return None
    
    def save_resume(self, resume_data):
        """Save resume data to database"""
        if self.mongo_available:
            return self.resumes.insert_one(resume_data)
        else:
            resume_data['_id'] = len(self.resumes_memory) + 1
            self.resumes_memory.append(resume_data)
            return True
    
    def get_user_resumes(self, username):
        """Get all resumes for a user"""
        if self.mongo_available:
            return list(self.resumes.find({"username": username}))
        else:
            return [r for r in self.resumes_memory if r.get('username') == username]
    
    def get_session_resumes(self, username, session_id):
        """Get resumes for a specific ranking session"""
        if self.mongo_available:
            return list(self.resumes.find({
                "username": username, 
                "ranking_session_id": session_id
            }))
        else:
            return [r for r in self.resumes_memory 
                   if r.get('username') == username and r.get('ranking_session_id') == session_id]
    
    def clear_old_session_resumes(self, username):
        """Mark old resumes as not current session"""
        if self.mongo_available:
            self.resumes.update_many(
                {"username": username, "is_current_session": True},
                {"$set": {"is_current_session": False}}
            )
        else:
            for resume in self.resumes_memory:
                if resume.get('username') == username and resume.get('is_current_session'):
                    resume['is_current_session'] = False
    
    def save_ranking_session(self, ranking_data):
        """Save ranking session data for tracking"""
        if self.mongo_available:
            # Use a separate collection for ranking sessions
            if not hasattr(self, 'ranking_sessions'):
                self.ranking_sessions = self.db.ranking_sessions
            return self.ranking_sessions.insert_one(ranking_data)
        else:
            # For in-memory storage, add to a separate list
            if not hasattr(self, 'ranking_sessions_memory'):
                self.ranking_sessions_memory = []
            ranking_data['_id'] = len(self.ranking_sessions_memory) + 1
            self.ranking_sessions_memory.append(ranking_data)
            return True
    
    def get_resume_by_filename(self, username, filename):
        """Get resume by filename for a specific user"""
        if self.mongo_available:
            return self.resumes.find_one({"username": username, "filename": filename})
        else:
            for resume in self.resumes_memory:
                if resume.get('username') == username and resume.get('filename') == filename:
                    return resume
            return None
    
    def update_resume_score(self, resume_id, score):
        """Update resume score"""
        if self.mongo_available:
            return self.resumes.update_one(
                {"_id": resume_id},
                {"$set": {"score": score}}
            )
        else:
            for resume in self.resumes_memory:
                if resume.get('_id') == resume_id:
                    resume['score'] = score
                    return True
            return False
    
    # Admin functions
    def get_all_users(self):
        """Get all users for admin dashboard"""
        if self.mongo_available:
            return list(self.users.find({}))
        else:
            return list(self.users_memory.values())
    
    def get_all_resumes(self):
        """Get all resumes for admin dashboard"""
        if self.mongo_available:
            return list(self.resumes.find({}))
        else:
            return self.resumes_memory
    
    def delete_resume(self, resume_id):
        """Delete resume by ID"""
        try:
            if self.mongo_available:
                from bson import ObjectId
                result = self.resumes.delete_one({"_id": ObjectId(resume_id)})
                return result.deleted_count > 0
            else:
                # For in-memory storage
                for i, resume in enumerate(self.resumes_memory):
                    if str(resume.get('_id')) == str(resume_id):
                        self.resumes_memory.pop(i)
                        return True
                return False
        except Exception as e:
            print(f"Error deleting resume: {e}")
            return False
    
    def get_all_rankings(self):
        """Get all ranking results for admin dashboard"""
        if self.mongo_available:
            # Get resumes with scores, sorted by score descending
            return list(self.resumes.find({"score": {"$exists": True}}).sort("score", -1))
        else:
            ranked = [r for r in self.resumes_memory if 'score' in r]
            return sorted(ranked, key=lambda x: x.get('score', 0), reverse=True)
    
    def update_resume_score(self, resume_id, score, existing_skills):
        """Update resume with ranking score"""
        try:
            from bson import ObjectId
            if self.mongo_available:
                result = self.resumes.update_one(
                    {"_id": ObjectId(resume_id)},
                    {"$set": {
                        "score": score,
                        "existing_skills": existing_skills,
                        "ranked_at": datetime.now(timezone.utc)
                    }}
                )
                return result.modified_count > 0
            else:
                for resume in self.resumes_memory:
                    if str(resume.get('_id')) == resume_id:
                        resume['score'] = score
                        resume['existing_skills'] = existing_skills
                        resume['ranked_at'] = datetime.now(timezone.utc)
                        return True
                return False
        except Exception as e:
            print(f"Error updating resume score: {e}")
            return False
    
    def update_user_status(self, username, active):
        """Update user active status"""
        if self.mongo_available:
            result = self.users.update_one(
                {"username": username},
                {"$set": {"active": active}}
            )
            return result.modified_count > 0
        else:
            if username in self.users_memory:
                self.users_memory[username]['active'] = active
                return True
            return False
    
    def get_system_stats(self):
        """Get system statistics for admin dashboard"""
        if self.mongo_available:
            total_users = self.users.count_documents({})
            active_users = self.users.count_documents({"active": {"$ne": False}})
            total_resumes = self.resumes.count_documents({})
            
            # Count rankings from ranking_sessions collection
            if not hasattr(self, 'ranking_sessions'):
                self.ranking_sessions = self.db.ranking_sessions
            total_rankings = self.ranking_sessions.count_documents({})
            
            # Count job descriptions from job_descriptions collection
            if not hasattr(self, 'job_descriptions'):
                self.job_descriptions = self.db.job_descriptions
            total_jobs = self.job_descriptions.count_documents({})
        else:
            total_users = len(self.users_memory)
            active_users = len([u for u in self.users_memory.values() if u.get('active', True)])
            total_resumes = len(self.resumes_memory)
            
            # Count rankings from ranking_sessions_memory
            if not hasattr(self, 'ranking_sessions_memory'):
                self.ranking_sessions_memory = []
            total_rankings = len(self.ranking_sessions_memory)
            
            # Count job descriptions from job_descriptions_memory
            if not hasattr(self, 'job_descriptions_memory'):
                self.job_descriptions_memory = []
            total_jobs = len(self.job_descriptions_memory)
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_resumes": total_resumes,
            "total_rankings": total_rankings,
            "total_jobs": total_jobs
        }
    
    def remove_user(self, username):
        """Permanently remove a user from database"""
        try:
            if self.mongo_available:
                from bson import ObjectId
                result = self.users.delete_one({"username": username})
                return result.deleted_count > 0
            else:
                if username in self.users_memory:
                    del self.users_memory[username]
                    return True
                return False
        except Exception as e:
            print(f"Error removing user: {e}")
            return False
    
    def save_job_description(self, job_data):
        """Save job description to database"""
        if self.mongo_available:
            if not hasattr(self, 'job_descriptions'):
                self.job_descriptions = self.db.job_descriptions
            return self.job_descriptions.insert_one(job_data)
        else:
            if not hasattr(self, 'job_descriptions_memory'):
                self.job_descriptions_memory = []
            job_data['_id'] = len(self.job_descriptions_memory) + 1
            self.job_descriptions_memory.append(job_data)
            return True
    
    def get_all_job_descriptions(self):
        """Get all job descriptions for admin dashboard"""
        if self.mongo_available:
            if not hasattr(self, 'job_descriptions'):
                self.job_descriptions = self.db.job_descriptions
            return list(self.job_descriptions.find({}))
        else:
            if not hasattr(self, 'job_descriptions_memory'):
                self.job_descriptions_memory = []
            return self.job_descriptions_memory
    
    def delete_job_description(self, job_id):
        """Delete job description by ID"""
        try:
            if self.mongo_available:
                from bson import ObjectId
                if not hasattr(self, 'job_descriptions'):
                    self.job_descriptions = self.db.job_descriptions
                result = self.job_descriptions.delete_one({"_id": ObjectId(job_id)})
                return result.deleted_count > 0
            else:
                if not hasattr(self, 'job_descriptions_memory'):
                    self.job_descriptions_memory = []
                for i, job in enumerate(self.job_descriptions_memory):
                    if str(job.get('_id')) == str(job_id):
                        self.job_descriptions_memory.pop(i)
                        return True
                return False
        except Exception as e:
            print(f"Error deleting job description: {e}")
            return False