from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ResumeSubmission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, index=True)
    resume_filename = Column(String, nullable=False)
    job_description = Column(Text, nullable=False)
    latex_path = Column(String)
    latex_content = Column(Text)
    cover_letter_path = Column(String)
    cover_letter_text = Column(Text)
    course_recommendations = Column(Text)
    evaluation_json = Column(Text, nullable=True)
