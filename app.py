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
    all_comments = list(db.comments.find({},{'_id':False}))
    return jsonify({'result': all_comments})


    # 댓글수정하기
# @app.route("/",methods=["POST"])
# def editready_post():
#     name_receive = request.form['name_give']
#     comment_receive = request.form['comment_give']

    


    # return jsonify ({'msg':'가져오는중'})
    # 1. url id 값이 Undefined
    # 2. get post 요청이 백엔드 프론트 엔드가 안맞는다

# 아이디 딕셔너리값은 유튜브 참고
# @app.route("/comment/edit/<comment_id>",methods=["GET"])
# def edit_get(comment_id):
    
#     comment_one['_id'] = str(comment_one['_id'])
#     comment_one = db.comments.find_one({'_id':ObjectId(comment_id)})
    
    
    
    

#     return jsonify ({'result':comment_one })

# # 댓글목록 보여주기 (댓글목록 요청) 프론트로 보내줌
# # 댓글목록 보여주기 2 append 가 될 때 id도 같이 들어가야함.


# @app.route("/comment/edit/<comment_id>",methods=["POST"])
# def edit_post(comment_id):
#     editname_receive = request.form['editname_give']
#     editcomment_receive = request.form['editcomment_give']
    
#     doc = {
#             'name' : editname_receive,
#             'comment' : editcomment_receive
#         }


#     db.comments.update_one({'_id':comment_id },{'$set':{'name':editname_receive}},{'$set':{'comment':editcomment_receive}})


#     return jsonify ({'msg':'수정완료!'})

 

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

