import random
from kocrawl.travle_openAPI.base_openAPI import BaseOpenApi

class AreaOpenApi(BaseOpenApi):
    def make_area_key(self, area: str): 
        """ openAPI에 저장된 데이터에 접속해 사용자가 입력한 지역(area)의 고유번호를 반환.

        Args:
            area (str): 여행지를 검색하려는 지역명(ex. 서울, 부산, 대구 등)
        """
        
        area_url = self.url_base # 지역이 담긴 api 주소 반환
        print(area_url)
        df_area = self.sampling_data_df(area_url) # 지역에 대한 데이터 샘플링

        # 입력한 지역에 대한 고유 번호 출력
        df_area = df_area.loc[df_area['name']==area]
        df_area_dict = df_area.to_dict()['code']
        
        for k, _ in df_area_dict.items(): # 더 효율적으로 짤 수 있을 거 같다.
            area_key = df_area_dict[k]
        
        return area_key 

    def make_sigungu_key(self, area: str, sigungu: str): 
        """ openAPI에 저장된 데이터에 접속해 사용자가 입력한 시군구(sigungu)의 고유번호를 반환.

        Args:
            area (str): 여행지를 검색하려는 지역명(ex. 서울, 부산, 대구 등)
            sigungu (str): 여행지를 검색하려는 시군구명(ex. 관악구, 동대문구, 영등포구 등)
        """
        area_key = self.make_area_key(area) # 지역의 고유키 구하기
        sisgungu_url = self.url_area.format(area=area_key) # 시군구가 담긴 api 주소 반환
        print(sisgungu_url)
        df_sigungu = self.sampling_data_df(sisgungu_url)

        # 입력한 지역에 대한 고유 번호 출력
        df_sigungu = df_sigungu.loc[df_sigungu['name']==sigungu]
        df_sigungu_dict = df_sigungu.to_dict()['code']
        
        for k, _ in df_sigungu_dict.items(): # 해당 코드 개선하자.
            sigungu_key = df_sigungu_dict[k]
        
        return (area_key, sigungu_key)

    def search_landmark(self, area: str, sigungu: str):
        """ 사용자가 입력한 지역, 시군구에 대한 여행지 중 하나를 반환
        (일단 랜덤으로 반환하도록 설정)

        Args:
            area (str): 여행지를 검색하려는 지역명(ex. 서울, 부산, 대구 등)
            sigungu (str): 여행지를 검색하려는 시군구명(ex. 관악구, 동대문구, 영등포구 등)
        """
        
        print('search_landmark 함수 내부')
        key = self.make_sigungu_key(area, sigungu) # 알고 싶은 여행지의 지역 ket, 시군구 key 호출
        print('key 추출')
        url_landmark = self.url_travle.format(area=key[0], sigungu=key[1]) # 지역/시군구에 대한 여행지 url 생성
        json_landmark = self.sampling_data_json(url_landmark)
        index_landmark = random.randint(0, len(json_landmark)) # 출력할 landmark의 index를 랜덤으로 호출
        
        json_landmark = json_landmark[index_landmark] # 여행지 정보를 json type으로 변경
        img_landmark = self.get_landmark_img(json_landmark) # 여행지에 대한 img url 반환

        return json_landmark, img_landmark

    def search_landmark_by_area(self, area: str):
        """ 사용자가 입력한 지역에 대한 여행지 중 하나를 반환
        (일단 랜덤으로 반환하도록 설정)

        Args:
            area (str): 여행지를 검색하려는 지역명(ex. 서울, 부산, 대구 등)
        """

        print('search_landmark 함수 내부')
        key = self.make_area_key(area)  # 알고 싶은 여행지의 지역 ket, 시군구 key 호출
        print('key 추출')
        url_landmark = self.url_travle_by_area.format(area=key[0])  # 지역/시군구에 대한 여행지 url 생성
        json_landmark = self.sampling_data_json(url_landmark)
        index_landmark = random.randint(0, len(json_landmark))  # 출력할 landmark의 index를 랜덤으로 호출

        json_landmark = json_landmark[index_landmark]  # 여행지 정보를 json type으로 변경
        img_landmark = self.get_landmark_img(json_landmark)  # 여행지에 대한 img url 반환

        return json_landmark, img_landmark

    def search_landmark_by_sigungu(self, sigungu: str):
        """ 사용자가 입력한 시군구에 대한 여행지 중 하나를 반환
        지역이 없을 시 API 호출이 불가능하므로, 지역을 찾아는 과정이 별도로 필요
        (일단 랜덤으로 반환하도록 설정)

        Args:
            sigungu (str): 여행지를 검색하려는 시군구명(ex. 관악구, 동대문구, 영등포구 등)
        """

        area = self.areaCode_by_sigungu[sigungu]
        key = self.make_sigungu_key(area, sigungu)  # 알고 싶은 여행지의 지역 ket, 시군구 key 호출
        print('key 추출')
        url_landmark = self.url_travle.format(area=key[0], sigungu=key[1])  # 지역/시군구에 대한 여행지 url 생성
        json_landmark = self.sampling_data_json(url_landmark)
        index_landmark = random.randint(0, len(json_landmark))  # 출력할 landmark의 index를 랜덤으로 호출

        json_landmark = json_landmark[index_landmark]  # 여행지 정보를 json type으로 변경
        img_landmark = self.get_landmark_img(json_landmark)  # 여행지에 대한 img url 반환

        return json_landmark, img_landmark