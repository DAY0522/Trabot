"""
@auther Hyunwoong
@since 7/1/2020
@see https://github.com/gusdnd852
"""
import sys
sys.path.append('C:/Users/ekdud/Documents/Trabot/trabot')

from flask import render_template, request, jsonify

from kochat.app import KochatApi
from kochat.data import Dataset
from kochat.loss import CRFLoss, CosFace, CenterLoss, COCOLoss, CrossEntropyLoss
from kochat.model import intent, embed, entity
from kochat.proc import DistanceClassifier, GensimEmbedder, EntityRecognizer, SoftmaxClassifier
import requests

from scenario import dust, weather, travel, restaurant
# 에러 나면 이걸로 실행해보세요!


dataset = Dataset(ood=True)
emb = GensimEmbedder(model=embed.FastText())

clf = DistanceClassifier(
    model=intent.CNN(dataset.intent_dict),
    loss=CenterLoss(dataset.intent_dict),
)

rcn = EntityRecognizer(
    model=entity.LSTM(dataset.entity_dict),
    loss=CRFLoss(dataset.entity_dict)
)

kochat = KochatApi(
    dataset=dataset,
    embed_processor=(emb, False),
    intent_classifier=(clf, False),
    entity_recognizer=(rcn, False),
    scenarios=[
        weather, dust, travel, restaurant
    ]
)

@kochat.app.route('/')
def index():
    return render_template("index2.html")

@kochat.app.route('/detail')
def detail():
    return render_template("detail.html")

@kochat.app.route('/get/detail', methods=['POST'])
def getDetail():
    contentId = request.get_json()["contentId"]
    response = requests.get(f'https://apis.data.go.kr/B551011/KorService/detailCommon?serviceKey=7ut0kiJb%2FugaTORVPbk2lljMu0y9IY4HoAzWysfXZIKqVl%2FDJ7zsr6Ca3b7nwotssH2lFdHHms7yUOl2RTCgcA%3D%3D&MobileOS=ETC&MobileApp=AppTest&_type=json&contentId={contentId}&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y',verify=False)
    jsonData = response.json()['response']['body']['items']['item'][0]

    return jsonify({
        'title': jsonData['title'],
        'addr1': jsonData['addr1'],
        'tel': jsonData['tel'],
        'overview': jsonData['overview'],
        'img': jsonData['firstimage']
    })

if __name__ == '__main__':
    kochat.app.template_folder = kochat.root_dir + 'templates'
    kochat.app.static_folder = kochat.root_dir + 'static'
    kochat.app.run(port=8080, host='127.0.0.1')
