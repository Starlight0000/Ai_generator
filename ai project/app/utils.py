import requests
import os
import json
import time
import webbrowser

# Shotstack API key and endpoint
SHOTSTACK_API_KEY = "2GynYYkunvRzHzUGXgqHOwCVMQXW2LSoGgRSrOyJ"
SHOTSTACK_API_URL = "https://api.shotstack.io/v1"

POLLINATIONS_API_URL = "https://api.pollinations.ai/prompt"

def submit_render_request(prompt):
    """
    Submit a render request to the Shotstack API.
    """
    url = f"{SHOTSTACK_API_URL}/render"
    headers = {"x-api-key": SHOTSTACK_API_KEY, "Content-Type": "application/json"}
    payload = {
        "timeline": {
            "soundtrack": {"src": "https://shotstack-assets.s3.amazonaws.com/music/disco.mp3"},
            "tracks": [
                {
                    "clips": [
                        {
                            "asset": {
                                "type": "title",
                                "text": prompt
                            },
                            "start": 0,
                            "length": 3
                        }
                    ]
                }
            ]
        },
        "output": {"format": "mp4", "resolution": "hd"}
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if response.status_code == 201:
        render_id = response_data["response"]["id"]
        print(f"Render successfully queued. Render ID: {render_id}")
        return render_id
    else:
        raise RuntimeError(f"Error submitting render request: {response.text}")

def check_render_status(render_id):
    """
    Check the status of the render request.
    """
    url = f"{SHOTSTACK_API_URL}/render/{render_id}"
    headers = {"x-api-key": SHOTSTACK_API_KEY}

    while True:
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            status = response_data["response"]["status"]
            print(f"Render status: {status}")

            if status == "done":
                return response_data["response"]["url"]
            elif status == "failed":
                raise RuntimeError("Render failed.")
            else:
                time.sleep(10)  # Wait and poll again
        else:
            raise RuntimeError(f"Error checking render status: {response.text}")

def play_video(video_url):
    """
    Open the video in a web browser.
    """
    print(f"Playing video at {video_url}")
    webbrowser.open(video_url)

def generate_image(prompt):
    """
    Generate an image based on the given prompt.

    Parameters:
    prompt (str): The text prompt to generate the image.
    """
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=1268&height=768&model=flux&seed=42"
    response = requests.get(url)

    if response.status_code == 200:
        return response.url
    else:
        raise RuntimeError(f"Image generation error: {response.text}")
    
