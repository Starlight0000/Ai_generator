
# AI Content Generator

This is a simple web application built with **Streamlit** that allows users to log in, generate AI-based videos and images using a provided prompt, and view their previously generated content. It uses a backend database to store and manage user-generated content, and it also allows users to display their past videos and images in a structured, easy-to-use interface.

------------------------------------------------------------------------------------------------------------------------------------------------

## Features

- **Login System**: Users can log in using a unique user ID.
- **Content Generation**: Users can input a prompt, and the app will generate an AI-based video and image based on that prompt.
- **Previous Content**: Users can view previously generated content (video and image) in a tabular format.
- **Notifications**: Users are notified when content generation is successful or if there is an error.
- **File Management**: Generated video and image files are stored in a structured folder system.

## Prerequisites

Make sure to install the following dependencies:

1. Python 3.8+ (recommended)
2. Install required Python packages using `pip`:
   ```bash```
3. pip install streamlit pandas sqlalchemy

## Setup 

1. **Clone the repository**

      ```
      git clone <repository-url>
      cd <repository-directory> ```

2. **Install dependencies**

      ``` pip install -r requirements.txt ``` 

4. **Run the application**

      ```python -m streamlit run app.py ```

6. **Using the App**

      Login: Enter your User ID to log in.
      Content Generation: Once logged in, input a motivational prompt to generate the AI content (video and image).
      View Content: After content generation, you can view the generated video and image. You can also see a history of your previously generated           content in a tabular format by clicking the "View Previous Content" button.

-----------------------------------------------------------------------------------------------------------------------------------------------

## File Structure 

```AI-Content-Generator/
├── app/
│   ├── database.py        # Contains database models and functions for content generation
│   ├── utils.py           # Utility functions like generate_and_store
├── static/
│   └── uploads/           # Directory for storing user-uploaded/generated videos and images
├── main.py                 # Main Streamlit app file
├── requirements.txt       # List of dependencies for the project
└── README.md              # This file
```
------------------------------------------------------------------------------------------------------------------------------------------------

##License
MIT License. See LICENSE.

markdown
Copy code

### Key Changes:
- Shortened explanations for key features and setup.
- Kept necessary instructions for running the app and setting up the database.
- Simplified file structure and usage instructions.
    
