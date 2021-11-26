import json
from youtube_transcript_api import YouTubeTranscriptApi
from flask import request
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests

from flask import Flask
app = Flask(__name__)
#CORS(app)
secret_api_key = "AIzaSyB2GyWjg0KHHU-kezYgDjJGO-AhBoALwAc"
youtube_data_api_url = "https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}"
#from flask_cors import CORS
from flask import jsonify


def start_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr', 'en'])
    transcript = ""
    for doc in transcript_list:
        text_chunk = json.loads(json.dumps(doc))['text']
        transcript+= text_chunk + " " if text_chunk!="[Musique]" else ""
    
    youtube_data_api_uri = youtube_data_api_url.format(video_id, secret_api_key)
    r = requests.get(url = youtube_data_api_uri)
  
    data = r.json()
    video_title = data['items'][0]['snippet']['title']
    return {"transcript": transcript, "video_title": video_title}




@app.route("/",  methods = ['POST'])
def launch_transcription():
    url = request.form['uri']
    parsed_url = urlparse(url)
    url_params = list(parse_qs(parsed_url.query).keys())
    video_id = parse_qs(parsed_url.query)['v'][0] if('v' in url_params) else url.split('embed/')[-1]
    print(video_id)
    #video_id = list(request.form.to_dict())[0]

    return start_transcript(video_id)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
