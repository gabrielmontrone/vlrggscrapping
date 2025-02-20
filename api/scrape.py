from utils.events import EVENTS

from api.scrapers import (
    check_health,
    vlr_live_score,
    vlr_match_results,
    vlr_news,
    vlr_rankings,
    vlr_stats,
    vlr_upcoming_matches,
    vlr_events,
    vlr_check_match_urls,
    vlr_tournament_overview,
    vlr_players_details,
)


class Vlr:
    @staticmethod
    def vlr_news():
        return vlr_news()

    @staticmethod
    def vlr_rankings(region):
        return vlr_rankings(region)

    @staticmethod
    def vlr_stats(region: str, timespan: str):
        return vlr_stats(region, timespan)

    @staticmethod
    def vlr_upcoming_matches():
        return vlr_upcoming_matches()

    @staticmethod
    def vlr_live_score():
        return vlr_live_score()

    @staticmethod
    def vlr_match_results():
        return vlr_match_results()

    @staticmethod
    def check_health():
        return check_health()

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
