#exampleimage generator using pollinations api

import requests
def download_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&model=flux&seed=42"
    response = requests.get(url)
    with open('generated_image.jpg', 'wb') as file:
        file.write(response.content)
    print('Image downloaded!')

download_image("Harwork is the key to success")