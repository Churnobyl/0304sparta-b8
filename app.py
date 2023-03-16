from flask import Flask, render_template, request, jsonify  # 웹개발 라이브러리
from pymongo import MongoClient  # DB 라이브러리
from ytmusicapi import YTMusic
app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.caexhck.mongodb.net/?retryWrites=true&w=majority')
db = client.brain  # DB명

#Youtube 크롤링 API
from ytmusicapi import YTMusic
ytmusic = YTMusic('headers_auth.json')

@app.route('/')
def home():
    return render_template('index.html')

# 머리 클릭 시 p태그 이름에 따라 DB 조회해서 data 가져오는 함수(POST)
@app.route("/brain", methods=["POST"])
def brain_get():
    name_receive = request.form['name_give']
    
    all_data = list(db.data.find({"name": name_receive}, {'_id':False}))
    
    cache = ytmusic.get_song(all_data[0]['favorite_music'])['videoDetails']
    music = cache['title']
    artist = cache['author']
    
    all_data[0]['music'] = music
    all_data[0]['artist'] = artist
    
    return jsonify({'result': all_data})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)