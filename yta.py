import json
from youtube_transcript_api import YouTubeTranscriptApi
from flask import request


video_id="QNwCP5SaOfU"

def start_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr'])
    transcript = ""
    for doc in transcript_list:
        text_chunk = json.loads(json.dumps(doc))['text']
        transcript+= text_chunk + " " if text_chunk!="[Musique]" else ""
    return transcript


from flask import Flask
app = Flask(__name__)

@app.route("/",  methods = ['POST'])
def launch_transcription():
    video_id = request.form['uri']
    return start_transcript(video_id)

if __name__ == "__main__":
  app.run()
