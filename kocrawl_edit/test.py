from travle_openAPI.Theme_based_api import ThemeOpenApi
from answerer.map_theme_answerer import MapThemeAnswerer

location = '서울'
theme = '여행코스'

URL_DATA = ThemeOpenApi().getThemeBasedAreaURL(location, theme)
result = ThemeOpenApi().getData(URL_DATA[0], URL_DATA[1])
result_msg = MapThemeAnswerer().map_theme_form(location, theme, result)

print(result_msg)