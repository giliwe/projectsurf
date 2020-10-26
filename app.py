import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests

load_dotenv()
app = Flask(__name__)
TOKEN = os.environ.get('API_KEY')

@app.route('/')
def index():
    surfboard_type = request.args.get('type')
    surfboard_color = request.args.get('color')
    search_phrase = f'surfboard%20{surfboard_type}%20{surfboard_color}'
    url = f'https://api.pexels.com/v1/search?query={search_phrase}'
    header = {'Authorization': TOKEN}
    resp = requests.get(url, headers=header)
    resp_json = resp.json()
    num_of_photos =  resp_json.get('per_page', 0)
    if num_of_photos != 0:
      photos_details = [
        {
          'image': photo.get('src')['large'],
          'photographer_name': photo.get('photographer'),
          'photographer_url': photo.get('photographer_url')
        }
        for photo in resp_json.get('photos')[:num_of_photos]
      ]
      return render_template(
          'index.html',
          photos=photos_details
      )
    else:
      return render_template('index.html')


if __name__ == '__main__':
    app.run(threaded=True, port=5000)