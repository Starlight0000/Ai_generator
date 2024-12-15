import os
import streamlit as st
from datetime import datetime
import pandas as pd
from app.database import create_db_session, Content  # Import your database session creation
from app.database import generate_and_store  # Import the generate_and_store function from utils.py

# Set up the page configuration
st.set_page_config(page_title="AI Generator", layout="wide")

# Check if the user is logged in by looking at the session state
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# Sidebar for navigation between pages
page = st.sidebar.radio("Select a Page", ["Login", "Content Generation", "Previous Content"])

if page == "Login":
    st.title("Login to AI Content Generator")

    # User login form
    user_id = st.text_input("Enter your User ID:")

    if st.button("Login"):
        if user_id:
            st.session_state['user_id'] = user_id
            st.sidebar.success(f"Logged in as {user_id}")
        else:
            st.sidebar.error("Please enter a valid User ID.")

elif page == "Content Generation":
    # Ensure user is logged in before allowing content generation
    if not st.session_state['user_id']:
        st.error("You must log in first!")
        st.stop()  # Stop further execution

    user_id = st.session_state['user_id']
    st.title(f"Welcome {user_id}! Generate AI Content")

    # Sidebar for User Input
    prompt = st.text_area("Enter a motivational text prompt:")

    if st.button("Generate Content"):
        if not prompt:
            st.error("Prompt is required to generate content!")
        else:
            with st.spinner("Generating video and image..."):
                session = create_db_session()
                content_entry = Content(user_id=user_id, prompt=prompt, status="Processing")
                session.add(content_entry)
                session.commit()

                # Define directory to save videos
                user_dir = os.path.join("static/uploads", f"user_{user_id}")
                os.makedirs(user_dir, exist_ok=True)

                try:
                    # Call your function to generate video and image
                    video_url, image_url = generate_and_store(user_id, prompt)

                    # Store the video and image URLs in the DB
                    content_entry.video_paths = video_url
                    content_entry.image_paths = image_url
                    content_entry.status = "Completed"
                    content_entry.generated_at = datetime.now()

                    session.commit()

                    # Indicate success in the app with a notification
                    st.success("Video and Image generated successfully!")
                    st.toast("Video and Image generated successfully!", icon="🎉")
                    st.balloons()  # Add celebratory balloons on success
                    st.session_state["video_paths"] = video_url  # Save video path for later use
                    st.session_state["image_paths"] = image_url  # Save image path for later use
                    st.session_state["content_generated"] = True  # Flag to indicate both video and image are generated

                except Exception as e:
                    content_entry.status = "Failed"
                    session.commit()
                    # Notify the user about the error
                    st.error(f"Error during video/image generation: {e}")
                    st.session_state["content_generated"] = False

    # Display Generated Video and Image
    if st.session_state.get("content_generated"):
        # Create a button for displaying the video
        if st.button("Show Video"):
            if st.session_state.get("video_paths"):
                st.header("Generated Video")
                st.video(st.session_state["video_paths"])  # Display video
            else:
                st.warning("No video generated yet.")
        
        # Create a button for displaying the image
        if st.button("Show Image"):
            if st.session_state.get("image_paths"):
                st.header("Generated Image")
                st.image(st.session_state["image_paths"], caption="Here’s your generated image!", use_container_width=True)  # Display image
            else:
                st.warning("No image generated yet.")

        # Display a footer or message indicating both contents are ready
        st.markdown("---")
        st.write("Your video and image have been generated successfully. Enjoy your AI-created content!")

    # Button to show previous content
    # if st.button("View Previous Content"):
    #     st.session_state["view_previous_content"] = True

elif page == "Previous Content":
    # Ensure user is logged in before showing previous content
    if not st.session_state['user_id']:
        st.error("You must log in first!")
        st.stop()  # Stop further execution

    user_id = st.session_state['user_id']
    st.title(f"Your Previous Content ({user_id})")

    # Fetch the user's previous content from the database
    session = create_db_session()
    previous_content = session.query(Content).filter_by(user_id=user_id).order_by(Content.generated_at.desc()).all()

    if previous_content:
        # Prepare data for table display
        data = []
        for content in previous_content:
            data.append({
                "Prompt": content.prompt,
                "Video": f"[Watch Video]({content.video_paths})" if content.video_paths else "No Video",
                "Image": f"[View Image]({content.image_paths})" if content.image_paths else "No Image",
                "Generated At": content.generated_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Convert the data to a DataFrame for table display
        df = pd.DataFrame(data)

        # Display the content in table format
        st.dataframe(df)

    else:
        st.write("No previous content found. Start generating your first AI content!")
