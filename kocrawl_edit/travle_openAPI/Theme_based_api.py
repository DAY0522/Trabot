from travle_openAPI.base_openAPI import BaseOpenApi
from travle_openAPI.Area_based_api import AreaOpenApi 
import pprint
import random

pp = pprint.PrettyPrinter(indent = 1)

class ThemeOpenApi(BaseOpenApi):
    def __init__(self):
        # 부모 클래스의 인스턴스를 생성하여 필요한 필드를 사용할 수 있도록 한다.
        super().__init__()

        # 테마별 contentTypeId를 저장하는 딕셔너리 필드 생성
        self.theme = {"관광지": 12, "문화시설": 14, "행사": 15, "공연": 15, "축제": 15, "여행코스": 25, "레포츠": 28, "숙박": 32, "쇼핑": 32, "음식점": 39}

    def getThemeRequestURL(self, area: str, contentType: str):
        if contentType in self.theme.keys():
            # 유효한 테마가 인자값으로 전달되면 요청 url을 리턴
            return self.url_theme + f'&keyword={area}&contentTypeId={self.theme[contentType]}'

        # 유효하지 않은 테마가 인자값으로 전달되면 None을 리턴
        return None

    def getThemeBasedAreaURL(self, area: str, contentType: str):
        # AreaOpenApi 클래스의 인스턴스를 생성하여 필요한 필드를 사용할 수 있도록 함
        x = AreaOpenApi()
        # 입력받은 지역명으로 지역 코드를 출력해주는 함수를 가져와 지역 코드를 저장
        area_key = x.make_area_key(area)
        if contentType in self.theme.keys():
            return (self.url_theme_area + f'&contentTypeId={self.theme[contentType]}&areaCode={area_key}', self.theme[contentType])
        return None

    def getData(self, url, contentTypeId):
        try:
            # url이 유효하면 해당 url로 요청을 넣은 반환값을 리턴
            json_data = self.sampling_data_json(url)
            
            # 테마가 코스일 때는 코스에 포함된 모든 여행지를 출력해줘야 함
            if contentTypeId == 25:
                if len(json_data) <= 2:
                    return json_data
                return json_data[0:3]
            
            random_index = random.randint(0, len(json_data))
            return json_data[random_index]
        except:
            # 유효하지 않은 url이 인자로 들어오면 아래 문자열 리턴
            return "검색 결과 없음"

    def printData(self):
        # 테스트
        #return pp.pprint(self.getData(self.getThemeRequestURL("경기", "축제")))
        data = self.getThemeBasedAreaURL("전라북도", "여행코스")
        return pp.pprint(self.getData(data[0], data[1]))

# 테스트 코드
# x = ThemeOpenApi()
# x.printData()