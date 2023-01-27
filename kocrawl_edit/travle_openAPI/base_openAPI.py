import pandas as pd
import requests
import json

# warning message 제거
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class BaseOpenApi():
    def __init__(self):
        # 본인이 openAPI 사이트에서 발급받은 인증키 입력
        self.serviceKey = '7ut0kiJb%2FugaTORVPbk2lljMu0y9IY4HoAzWysfXZIKqVl%2FDJ7zsr6Ca3b7nwotssH2lFdHHms7yUOl2RTCgcA%3D%3D'

        self.url_base = 'https://apis.data.go.kr/B551011/KorService/areaCode?MobileOS=ETC&MobileApp=AppTest&_type=json&numOfRows=20&serviceKey=' + self.serviceKey
        self.url_area = 'http://apis.data.go.kr/B551011/KorService/areaCode?serviceKey='+ self.serviceKey +'&numOfRows=100&MobileOS=ETC&MobileApp=AppTest&_type=json&areaCode={area}'
        self.url_travle = 'https://apis.data.go.kr/B551011/KorService/areaBasedList?MobileOS=ETC&MobileApp=AppTest&_type=json&numOfRows=50000&serviceKey=' + self.serviceKey + '&areaCode={area}&sigunguCode={sigungu}'
        self.url_travle_by_area = 'https://apis.data.go.kr/B551011/KorService/areaBasedList?MobileOS=ETC&MobileApp=AppTest&_type=json&numOfRows=50000&serviceKey=' + self.serviceKey + '&areaCode={area}'
        self.url_img = 'http://apis.data.go.kr/B551011/KorService/detailImage?serviceKey=' + self.serviceKey + '&numOfRows=10&MobileOS=ETC&MobileApp=AppTest&contentId={contentId}&subImageYN=Y&_type=json'
        self.url_location = 'https://apis.data.go.kr/B551011/KorService/locationBasedList?serviceKey='+ self.serviceKey +'&numOfRows=10000&MobileOS=ETC&MobileApp=AppTest&_type=json&mapX={longitude}&mapY={latitude}&radius=3000'
        self.url_theme = 'https://apis.data.go.kr/B551011/KorService/searchKeyword?serviceKey='+self.serviceKey+'&MobileOS=ETC&MobileApp=AppTest&_type=json'
        self.url_theme_area = 'https://apis.data.go.kr/B551011/KorService/areaBasedList?serviceKey='+self.serviceKey+'&MobileOS=ETC&MobileApp=AppTest&_type=json'

        self.areaCode_by_sigungu = {'강남구': '서울', '강동구': '서울', '강북구': '서울', '강서구': '서울', '관악구': '서울', '관악구': '서울',
                        '광진구': '서울', '구로구': '서울','금천구': '서울','노원구': '서울','도봉구': '서울','동대문구': '서울','동작구': '서울',
                        '마포구': '서울','서대문구': '서울','서초구': '서울','성동구': '서울','성북구': '서울','송파구': '서울','양천구': '서울',
                        '영등포구': '서울','용산구': '서울','은평구': '서울','종로구': '서울','중구': '서울','중랑구': '서울',
                        '가평군':'경기도','고양시':'경기도','과천시':'경기도','광명시':'경기도','광주시':'경기도','구리시':'경기도',
                        '군포시':'경기도','김포시':'경기도','남양주시':'경기도','동두천시':'경기도','부천시':'경기도','성남시':'경기도',
                        '수원시':'경기도','시흥시':'경기도','안산시':'경기도','안성시':'경기도','안양시':'경기도','양주시':'경기도',
                        '양평군':'경기도','여주시':'경기도','연천군':'경기도','오산시':'경기도','용인시':'경기도','의왕시':'경기도',
                        '의정부시':'경기도','이천시':'경기도','파주시':'경기도','평택시':'경기도','포천시':'경기도','하남시':'경기도','화성시':'경기도',
                        '강릉시':'강원도','고성군':'강원도','동해시':'강원도','삼척시':'강원도','속초시':'강원도','양구군':'강원도',
                        '양양군':'강원도','영월군':'강원도','원주시':'강원도','인제군':'강원도','정선군':'강원도','철원군':'강원도',
                        '춘천시':'강원도','태백시':'강원도','평창군':'강원도','홍천군':'강원도','화천군':'강원도','횡성군':'강원도',
                        '괴산군':'충청북도','단양군':'충청북도','보은군':'충청북도','영동군':'충청북도','옥천군':'충청북도','음성군':'충청북도',
                        '제천시':'충청북도','진천군':'충청북도','청원군':'충청북도','청주시':'충청북도','충주시':'충청북도','증평군':'충청북도',
                        '공주시':'충청남도','금산군':'충청남도','논산시':'충청남도','당진시':'충청남도','보령시':'충청남도','부여군':'충청남도',
                        '서산시':'충청남도','서천군':'충청남도','아산시':'충청남도','예산군':'충청남도','천안시':'충청남도','청양군':'충청남도',
                        '태안군':'충청남도','홍성군':'충청남도','계룡시':'충청남도',
                        '경산시':'경상북도','경주시':'경상북도','고령군':'경상북도','구미시':'경상북도','군위군':'경상북도','김천시':'경상북도',
                        '문경시':'경상북도','봉화군':'경상북도','상주시':'경상북도','성주군':'경상북도','안동시':'경상북도','영덕군':'경상북도',
                        '영양군':'경상북도','영주시':'경상북도','영천시':'경상북도','예천군':'경상북도','울릉군':'경상북도','울진군':'경상북도',
                        '의성군':'경상북도','청도군':'경상북도','청송군':'경상북도','칠곡군':'경상북도','포항시':'경상북도',
                        '거제시':'경상남도','거창군':'경상남도','고성군':'경상남도','김해시':'경상남도','남해군':'경상남도','마산시':'경상남도',
                        '밀양시':'경상남도','사천시':'경상남도','산청군':'경상남도','양산시':'경상남도','의령군':'경상남도','진주시':'경상남도','합천군':'경상남도',
                        '진해시':'경상남도','창녕군':'경상남도','창원시':'경상남도','통영시':'경상남도','하동군':'경상남도','함안군':'경상남도','함양군':'경상남도',
                        '고창군':'전라북도','군산시':'전라북도','김제시':'전라북도','남원시':'전라북도','무주군':'전라북도','부안군':'전라북도','정읍시':'전라북도',
                        '순창군':'전라북도','완주군':'전라북도','익산시':'전라북도','임실군':'전라북도','장수군':'전라북도','전주시':'전라북도','진안군':'전라북도',
                        '강진군':'전라남도','고흥군':'전라남도','곡성군':'전라남도','광양시':'전라남도','구례군':'전라남도','나주시':'전라남도','담양군':'전라남도',
                        '목포시':'전라남도','무안군':'전라남도','보성군':'전라남도','순천시':'전라남도','신안군':'전라남도','여수시':'전라남도','영광군':'전라남도',
                        '완도군':'전라남도','장성군':'전라남도','장흥군':'전라남도','진도군':'전라남도','함평군':'전라남도','해남군':'전라남도','화순군':'전라남도'
                        }

    def sampling_data_df(self, url): # url에 있는 필요한 정보를 불러오는 함수
        # url 불러오기
        response = requests.get(url, verify=False)
        # verify=False는 requests.exceptions.SSLError: HTTPSConnectionPool(host='apis.data.go.kr', port=443) 에러를 방지하기 위함.
        # 넣었는데도 에러가 발생한다면 사용중인 와이파이를 바꿔보자.


        #데이터 값 출력해보기
        Data = response.text # str

        # apiData를 json으로 변경
        json_Data = json.loads(Data) # json type으로 변경
        apiData = json_Data["response"]["body"]["items"]["item"] # 필요 부분만 가져옴

        df_data = pd.json_normalize(apiData) # Dataframe으로 변경
        return df_data

    def sampling_data_json(self,url): # url에 있는 필요한 정보를 불러오는 함수
        # url 불러오기
        response = requests.get(url, verify=False)
        # verify=False는 requests.exceptions.SSLError: HTTPSConnectionPool(host='apis.data.go.kr', port=443) 에러를 방지하기 위함.
        # 넣었는데도 에러가 발생한다면 사용중인 와이파이를 바꿔보자.

        #데이터 값 출력해보기
        data = response.text # str

        # apiData를 json으로 변경
        json_data = json.loads(data) # json type으로 변경
        api_data = json_data["response"]["body"]["items"]["item"]

        return api_data

    def get_contentid(self, landmark):
        return landmark['contentid']

    def get_landmark_img(self, landmark: json):
        """ 입력한 landmark에서 img 파일을 불러오는 함수

        Args:
            landmark (json): 특정 여행지에 대한 정보

        Returns:
            _type_: landmark's img url
        """
        contentid = self.get_contentid(landmark)
        url_img = self.url_img.format(contentId=contentid)

        try:
            json_img = self.sampling_data_json(self.url_img)
        except:
            print("no image of the landmark.")
            return False

        # 이미지 정보를 2개 가져옴.
        # 2개보다 적을 경우를 대비해 전체 json 길이와 2 중 작은 값을 가져옴.
        max_img = min(len(json_img), 2)

        img_landmark = list()
        for i in range(max_img):
            img_landmark.append(json_img[i]['originimgurl']) # img url 저장

        return img_landmark

