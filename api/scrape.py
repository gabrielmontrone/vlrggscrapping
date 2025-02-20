from utils.events import EVENTS

from api.scrapers import (
    vlr_events,
    vlr_check_match_urls,
    vlr_tournament_overview,
    vlr_players_details,
)


class Vlr:
    @staticmethod
    def vlr_events(event_key="current"):
        return vlr_events(event_key)

    @staticmethod
    def vlr_check_match_urls(event_key="current"):
        return vlr_check_match_urls(event_key)
    
    @staticmethod
    def vlr_tournament_overview(event_key="current"):
        return vlr_tournament_overview(event_key)
    
    @staticmethod
    def vlr_players_details(profile_url):
        return vlr_players_details(profile_url)

if __name__ == "__main__":
    print(Vlr.vlr_live_score())
