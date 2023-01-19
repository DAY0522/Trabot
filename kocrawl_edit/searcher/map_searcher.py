"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""
from random import randint

from kocrawl.searcher.base_searcher import BaseSearcher
from kocrawl.travle_openAPI.Area_based_api import AreaOpenApi

class MapSearcher(AreaOpenApi):

    def __init__(self):
        self.data_dict = {
            # 데이터를 담을 딕셔너리 구조를 정의합니다.
            'name': [], 'tel': [],
            'context': [], 'category': [],
            'address': [], 'thumUrl': []
        }

    def _make_area(self, location: str) -> str:
        """
        데이터를 출력하기 위해 query 들어가야 할 지역명을 구분
        (1. area, 2. area + sigungu, 3. sigungu 세 가지 방식으로 구분해야 함)

        :param location: Trabot이 인식한 장소
        :return: (area, sub_area) 형태의 튜플
        """
        print(location)

        location = location.split()
        if len(location) >= 2:
            area = location[0]
            sigungu = location[1]
            type = 2
        elif self.is_sigunguCode(location):  # sub_area로 들어온 경우
            area = None
            sigungu = location[0]
            type = 3
        else: # area로 들어온 경우
            area = location[0]
            sigungu = None
            type = 1
        return (area, sigungu, type)

    def is_sigunguCode(self, location: list) -> str:
        """
        sigungu인지 구분하는 함수

        :param: area or sigungu
        :return: 0 or 1
        str에 시, 군, 구가 있으면 즉 sub_area면 True
                         없으면 즉     area면 False
        """
        last = location[0][-1]
        if last=='시' or last=='군':
            return True
        elif last=='구' and location[0] != "대구":
            return True
        return False

    def search_travle_by_area(self, location: str, travel: str) -> dict:
        """
        openAPI를 이용해 지역별 여형지를 찾는 함수.

        :param location: 지역
        :param travel: 여행지
        :return: 사용할 내용만 json에서 뽑아서 dictionary로 만듬.
        """
    
        print('search 함수 시작')
        area, sigungu, type = self._make_area(location)
        print(area, sigungu, type)
        if type==1: # area만 있는 경우
            self.data_dict = AreaOpenApi().search_landmark_by_area(area)
            print("area만 있는 경우 입니다.")
        elif type==2: # area+sigungu 인 경우
            print('type2 입니다.')
            self.data_dict = AreaOpenApi().search_landmark(area, sigungu)
        else: # sigungu만 있는 경우
            self.data_dict = AreaOpenApi().search_landmark_by_sigungu(sigungu)
            print("sigungu만 있습니다. 예외처리가 필요합니다.")

        return self.data_dict
