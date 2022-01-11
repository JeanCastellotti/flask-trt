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
    resume_file = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "candidate"}


class Recruiter(User):
    __tablename__ = "recruiters"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    company = db.Column(db.String(50))
    address = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)

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
    salary = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    # candidates = db.relationship("Candidate", secondary="Application", back_populates="jobs")
    applications = db.relationship("Application")


# applications = db.Table(
#     "applications", 
#     db.Column("job_id", db.Integer, db.ForeignKey("jobs.id"), primary_key=True),
#     db.Column("user_id"), db.Integer, db.ForeignKey("users.id", primary_key=True),
#     db.Column("")


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_active = db.Column(db.Boolean, default=False)
    candidate = db.relationship("Candidate")


