from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.CHAR(60), nullable=False)
    role = db.Column(db.String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": role}

    def __repr__(self):
        return f"User({self.email}, {self.role})"


class Candidate(User):
    __tablename__ = "candidates"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    resume_file = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    applications = db.relationship("Application", back_populates="candidate")

    __mapper_args__ = {"polymorphic_identity": "candidate"}


class Recruiter(User):
    __tablename__ = "recruiters"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    company = db.Column(db.String(50))
    address = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    jobs = db.relationship("Job", back_populates="recruiter", cascade="all, delete")

    __mapper_args__ = {"polymorphic_identity": "recruiter"}


class Consultant(User):
    __tablename__ = "consultants"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "consultant"}


class Administrator(User):
    __tablename__ = "administrators"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "administrator"}


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    working_hours = db.Column(db.ARRAY(db.String), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    recruiter_id = db.Column(db.Integer, 
                             db.ForeignKey("recruiters.user_id"), 
                             nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    applications = db.relationship("Application", back_populates="job", cascade="all, delete")
    recruiter = db.relationship("Recruiter", back_populates="jobs")


class Application(db.Model):
    __tablename__ = "applications"
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    job = db.relationship("Job", back_populates="applications")
    candidate = db.relationship("Candidate", back_populates="applications")


