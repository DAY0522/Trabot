from kocrawl.answerer.base_answerer import BaseAnswerer

class MapThemeAnswerer(BaseAnswerer):
    def map_theme_form(self, location: str, theme: str, result) -> str:
        msg = self.map_init_theme.format(location=location, theme=theme)
        msg2 = self.map_init_theme.format(location=location, theme=theme)

        if theme == "여행코스":
            for i in range(len(result)): # 여행 코스는 최대 3개까지 출력
                msg2 += str(i+1)+'번 째 여행지입니다!\n'
                msg2 = self._add_msg_from_dict(result[i], 'title', msg2, '{title}에 가보시는 건 어떤가요?')
                msg2 = self._add_msg_from_dict(result[i], 'addr1', msg2, '주소는 {addr1}입니다.')
                msg2 += '\n'
                msg2 = msg2.format(theme=theme, location=location, title=result[i]['title'], addr1=result[i]['addr1'])    
            return msg2

        # 나머지는 하나씩만 출력
        msg = self._add_msg_from_dict(result, 'title', msg, '{title}에 가보시는 건 어떤가요?')
        msg = self._add_msg_from_dict(result, 'addr1', msg, '주소는 {addr1}입니다.')
        msg = msg.format(theme=theme, location=location, title=result['title'], addr1=result['addr1'])
        ## 여기에 여행지 상세정보 url첨부
        ## https://apis.data.go.kr/B551011/KorService/detailCommon?serviceKey=7ut0kiJb%2FugaTORVPbk2lljMu0y9IY4HoAzWysfXZIKqVl%2FDJ7zsr6Ca3b7nwotssH2lFdHHms7yUOl2RTCgcA%3D%3D&MobileOS=ETC&MobileApp=AppTest&_type=json&contentId=126508&defaultYN=Y&firstImageYN=Y&areacodeYN=Y&catcodeYN=Y&addrinfoYN=Y&mapinfoYN=Y&overviewYN=Y
        ## 지역 아이디만 알아도 가능, 보내는 링크에 /detail/{contentId}를 첨부
        return msg