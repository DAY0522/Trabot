import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from random import randint

from travle_openAPI.Theme_based_api import ThemeOpenApi 

class MapThemeSearcher(ThemeOpenApi):

    def search_travel_by_theme(self, location: str, theme: str) -> dict:
        """
        openAPI를 이용해 테마별 여행지를 찾는 함수

        :param locatino: 지역
        :param theme: 테마
        :return 사용할 내용만 json에서 뽑아서 dictionary로 만듬
        """
        data = ThemeOpenApi().getThemeBasedAreaURL(location, theme)
        themeURL = data[0]
        contentTypeId = data[1]
        self.data_dict = ThemeOpenApi().getData(themeURL, contentTypeId)
        return (self.data_dict, contentTypeId)