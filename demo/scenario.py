"""
@auther Hyunwoong
@since 7/1/2020
@see https://github.com/gusdnd852
"""

from kochat.app import Scenario
from kocrawl.map import MapCrawler

travel = Scenario(
    intent='travel',
    api=MapCrawler().request,
    scenario={
        'LOCATION': [],
        'PLACE': ['관광지']
    }
)

