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
    if surfboard_type == 'Type' and not surfboard_color:
      return render_template('index.html')
    search_phrase = f'surfboard%20{surfboard_type}%20{surfboard_color}'
    url = f'https://api.pexels.com/v1/search?query={search_phrase}'
    header = {'Authorization': TOKEN}
    resp = requests.get(url, headers=header)
    resp_json = resp.json()
    photos_details = [
      {
        'image': photo['src']['large'],
        'photographer_name': photo['photographer'],
        'photographer_url': photo['photographer_url']
      }
      for photo in resp_json['photos'][:15]
    ]
    return render_template(
        'index.html',
        photos=photos_details
    )

if __name__ == '__main__':
    app.run(threaded=True, port=5000)