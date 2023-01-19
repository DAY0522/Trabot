from Area_based_api import AreaOpenApi
from kocrawl.answerer.map_answerer import MapAnswerer
from kocrawl.searcher.map_searcher import MapSearcher


location = '수원시'
place = '관광지'
result_dict, result_img = AreaOpenApi().search_landmark_by_sigungu(location)
print(result_dict)
print(location, place)
result_msg = MapAnswerer().map_form(location, place, result_dict)
print(result_msg)