import requests
from selectolax.parser import HTMLParser
from utils.utils import headers
from api.scrapers.clutch.match_results import vlr_events

import re

def _clean_text(text):
    """
    Remove caracteres indesejados como quebras de linha e tabulações e normaliza espaços extras.
    """
    text = text.replace("\n", " ").replace("\t", " ").strip()
    return re.sub(r'\s+', ' ', text) 

def get_player_stats(item, stat_keys):
    """
    Extrai informações principais de um jogador a partir de um elemento HTML (overview).
    """
    username = item.css_first("div.text-of").text().strip()
    team = item.css_first("div.ge-text-light").text().strip()

    player_overview_stats = {
        "username": username,
        "team": team,
        "ratio": None,
        "acs": None,
        "kill": None,
        "death": None,
        "assist": None,
        "kill_death_diff": None,
        "kast": None,
        "adr": None,
        "headshot": None,
        "firstkill": None,
        "firstdeath": None,
        "fk_diff": None,
    }

    stats_td = item.css("td.mod-stat")
    for i, td in enumerate(stats_td):
        if i < len(stat_keys):  
            span_both = td.css_first("span.side.mod-both")
            if span_both:
                player_overview_stats[stat_keys[i]] = span_both.text().strip()

    return player_overview_stats

def vlr_check_match_urls(event_key):
    """
    Obtém detalhes das partidas de um evento com base na chave do evento
    """
    event_data = vlr_events(event_key)  

    match_urls = [match["match_url"] for match in event_data["data"]]
    
    result = []

    for match_url in match_urls:
        base_url = f"https://www.vlr.gg{match_url}"  

        resp = requests.get(f"{base_url}?game=all&tab=overview", headers=headers)
        status = resp.status_code
        html_overview = HTMLParser(resp.text)

        players_team_1 = []
        players_team_2 = []
        team_1_name = None

        round_info = None
        match_header_series = html_overview.css_first("div.match-header-event-series")
        if match_header_series:
            round_info = _clean_text(match_header_series.text(strip=True).replace("Main Event: ", ""))

        stat_keys = ["ratio", "acs", "kill", "death", "assist", "kill_death_diff", "kast", "adr", "headshot", "firstkill", "firstdeath", "fk_diff"]

        overview_data = []
        for item in html_overview.css('div.vm-stats-game[data-game-id="all"] tbody tr'):
            player_overview_stats = get_player_stats(item, stat_keys)
            overview_data.append(player_overview_stats)

        for overview in overview_data:
            username = overview["username"]
            player_data = {
                "overview": overview,
            }

            if team_1_name is None:
                team_1_name = overview["team"]

            if overview["team"] == team_1_name:
                players_team_1.append(player_data)
            else:
                players_team_2.append(player_data)

        result.append({
            "url": base_url,
            "round": round_info,
            "status": "success" if status == 200 else "failed",
            "players team 1": players_team_1,
            "players team 2": players_team_2,
        })

    data = {"status": status, "data": result}

    if status != 200:
        raise Exception(f"API response: {status}")
        
    return data
