"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""
from kocrawl.answerer.base_answerer import BaseAnswerer

class MapAnswerer(BaseAnswerer):

    def map_form(self, location: str, place: str, result) -> str:
        """
        여행지 출력 포맷
        
        :param location: 지역
        :param place: 장소
        :param result: 데이터 딕셔너리
        :return: 출력 메시지
        """

        print('map_form 내부입니다.')
        msg = self.map_init.format(location=location, place=place)
        msg += '{location} 근처의 '

        msg = self._add_msg_from_dict(result, 'contenttypeid', msg, '{contenttypeid}에 관련한 ')
        msg = self._add_msg_from_dict(result, 'title', msg, '{title}에 가보시는 건 어떤가요?')
        msg = self._add_msg_from_dict(result, 'addr1', msg, '주소는 {addr1}입니다.')
        ## 여기에 여행지 상세정보 url첨부
        ## https://apis.data.go.kr/B551011/KorService/detailCommon?serviceKey=7ut0kiJb%2FugaTORVPbk2lljMu0y9IY4HoAzWysfXZIKqVl%2FDJ7zsr6Ca3b7nwotssH2lFdHHms7yUOl2RTCgcA%3D%3D&MobileOS=ETC&MobileApp=AppTest&_type=json&contentId=126508&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y
        ## 지역 아이디만 알아도 가능, 보내는 링크에 /detail/{contentId}를 첨부
        msg = msg.format(place=place, location=location, contenttypeid=result['contenttypeid'], title=result['title'],
                         addr1=result['addr1'])

        return msg