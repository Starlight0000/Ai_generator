from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.utils import submit_render_request, check_render_status, play_video, generate_image

# Specify the database URL
DATABASE_URL = "sqlite:///C:/Users/Shiva/Desktop/ai project/content.db"  # Relative path, or use an absolute path

# Define the base class for models
Base = declarative_base()

# Define the Content model (same structure as your table)
class Content(Base):
    __tablename__ = "content"

    # Define the columns in the Content table
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    video_paths = Column(String)
    image_paths = Column(String)
    status = Column(String, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create a database session
def log_content_view(user_id, status):
    session = create_db_session()
    content_view = Content(user_id=user_id, status=status, timestamp=datetime.now())
    session.add(content_view)
    session.commit()

def create_db_session():
    return SessionLocal()

def store_in_db(session, user_id, prompt, video_url, image_url, status):
    """
    Store video metadata in the database.
    """
    try:
        new_content = Content(
            user_id=user_id,
            prompt=prompt,
            video_paths=video_url,
            image_paths = image_url,
            status=status,
            generated_at=datetime.utcnow()
        )
        session.add(new_content)
        session.commit()
        print("Video information stored in database.")
    except Exception as e:
        print(f"Error storing data in DB: {e}")
        session.rollback()


def generate_and_store(user_id, prompt):
    """
    Generate a video, play it, and store its metadata in the database.
    """
    session = create_db_session()
    try:
        # Submit render request
        render_id = submit_render_request(prompt)
        # Check render status and get video URL
        video_url = check_render_status(render_id)
        # Play the video
        # if video_url:
        #     play_video(video_url)
        image_url = generate_image(prompt)

        store_in_db(session, user_id, prompt, video_url, image_url, "completed")
        return video_url,image_url

    except Exception as e:
        print(f"Error during video generation: {e}")
        store_in_db(session, user_id, prompt, None, None, "failed")
        return None, None
    finally:
        session.close()