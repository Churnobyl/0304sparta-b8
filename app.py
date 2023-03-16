from bson.json_util import dumps
from bson.objectid import ObjectId
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



@app.route("/",methods=["POST"])
def comment_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
            'name' : name_receive,
            'comment' : comment_receive
        }

    db.comments.insert_one(doc)

    
    return jsonify ({'msg':'저장완료!'})


@app.route("/comment",methods=["GET"])
def comment_get():
    all_comments = list(db.comments.find())
    
    return jsonify({'result':dumps(all_comments)})
    

@app.route("/comment/edit/<comment_id>",methods=["GET"])
def edit_get(comment_id):
    

    comment_one = db.comments.find_one({'_id':ObjectId(comment_id)})
    comment_one['_id'] = str(comment_one['_id'])
    
    print(comment_one)
    
    
    
    return jsonify ({'result':dumps([comment_one]) })
    


@app.route("/comment/edit/<comment_id>",methods=["POST"])
def edit_post(comment_id):
    editname_receive = request.form['editname_give']
    editcomment_receive = request.form['editcomment_give']

    
   
    doc = {
            'name' : editname_receive,
            'comment' : editcomment_receive
            
        }
    
   
    
    edit_done = db.comments.update_one({'_id':ObjectId(comment_id) },{'$set':doc})
    edit_done['_id'] = str(edit_done['_id'])

    

    return jsonify ( {'msg':'수정완료!'} , {'result':dumps[edit_done]} )



 

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

