import pandas as pd
import requests
import json

# warning message 제거
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class BaseOpenApi():
    def __init__(self):
        # 본인이 openAPI 사이트에서 발급받은 인증키 입력
        self.serviceKey = 'ZxyV5bLf9U6/gs8S4NAqISFHJorbjd/Xrg1annceTQicObKR5EGo7ZCP9qmr7d9rH2H9WnhFR/HwGSGWEJbcbw=='

        self.url_base = 'https://apis.data.go.kr/B551011/KorService/areaCode?MobileOS=ETC&MobileApp=AppTest&_type=json&numOfRows=20&serviceKey=' + self.serviceKey
        self.url_area = 'http://apis.data.go.kr/B551011/KorService/areaCode?serviceKey='+ self.serviceKey +'&numOfRows=100&MobileOS=ETC&MobileApp=AppTest&_type=json&areaCode={area}'
        self.url_sigungu = 'https://apis.data.go.kr/B551011/KorService/areaBasedList?MobileOS=ETC&MobileApp=AppTest&_type=json&numOfRows=50000&serviceKey=' + self.serviceKey + '&areaCode={area}&sigunguCode={sigungu}'
        self.url_img = 'http://apis.data.go.kr/B551011/KorService/detailImage?serviceKey=' + self.serviceKey + '&numOfRows=10&MobileOS=ETC&MobileApp=AppTest&contentId={contentId}&subImageYN=Y&_type=json'
        self.url_location = 'https://apis.data.go.kr/B551011/KorService/locationBasedList?serviceKey='+ self.serviceKey +'&numOfRows=10000&MobileOS=ETC&MobileApp=AppTest&_type=json&mapX={longitude}&mapY={latitude}&radius=3000'


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