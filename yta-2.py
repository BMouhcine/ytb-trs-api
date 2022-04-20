import json
from youtube_transcript_api import YouTubeTranscriptApi
from flask import request
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
from flask import jsonify
from flask import Flask
import logging
import time


app = Flask(__name__)

secret_api_key = "AIzaSyB2GyWjg0KHHU-kezYgDjJGO-AhBoALwAc"
youtube_data_api_url = "https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}"

def check_music_token(text_chunk):
    return '[Musique]' not in text_chunk and '[Music]' not in text_chunk


def start_transcript(video_id):
    time.sleep(2.4)
    try:
      logging.warning("TESTING REQUESTS NOW........................................................")
      requests.get('https://www.google.com').raise_for_status()
    except:
      logging.warning('google failed')
    try:
      requests.get('https://youtube.com').raise_for_status()
    except:
      logging.warning('youtube failed')
    try:
      requests.get('https://www.youtube.com').raise_for_status()
    except:
      logging.warning('www.youtube.com failed')
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    transcript_content_string = ""
    language=""
    video_title=""
    for transcript in transcript_list:
        transcript_content = transcript.fetch()
        language = transcript.language_code
        break
    for doc in transcript_content:
        text_chunk = json.loads(json.dumps(doc))['text']
        transcript_content_string+= text_chunk + " " if check_music_token(text_chunk) else ""
    youtube_data_api_uri = youtube_data_api_url.format(video_id, secret_api_key)
    r = requests.get(url = youtube_data_api_uri)
    data = r.json()
    video_title = data['items'][0]['snippet']['title']
    return {"language": language, "transcript": transcript_content_string, "video_title": video_title}




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
