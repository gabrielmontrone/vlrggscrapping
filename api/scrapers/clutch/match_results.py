import requests
from selectolax.parser import HTMLParser
from utils.utils import headers
from utils.events import EVENTS

def vlr_events(event_key="current"):
    """
    Função para extrair informações de partidas do torneio atual.
    """
    event_data = EVENTS.get(event_key)  
    if not event_data:
        raise ValueError(f"Evento '{event_key}' não encontrado no EVENTS.")

    base_event_url = event_data["url"]
    matches_url = f"{base_event_url.replace('/event/', '/event/matches/')}?series_id=all"  
    
    resp = requests.get(matches_url, headers=headers)
    html = HTMLParser(resp.text)
    status = resp.status_code

    if status != 200:
        raise Exception(f"API response: {status}")

    result = []
    container = html.css_first("div.col.mod-1")  
    if not container:
        return result
    
    date_divs = container.css("div.wf-label.mod-large")
    card_divs = container.css("div.wf-card")
    
    if card_divs and not card_divs[0].css("a.wf-module-item.match-item"):
        card_divs = card_divs[1:]
    
    for date_div, card_div in zip(date_divs, card_divs):
        current_date = date_div.text().strip()

        for match_link in card_div.css("a.wf-module-item.match-item"):
            match_url = match_link.attributes.get("href", "")
            match_time = match_link.css_first("div.match-item-time").text().strip()

            teams = match_link.css("div.match-item-vs-team")
            if len(teams) < 2:
                continue

            team1 = teams[0].css_first("div.text-of").text().strip()
            team2 = teams[1].css_first("div.text-of").text().strip()

            team1_score_elem = teams[0].css_first("div.match-item-vs-team-score")
            team2_score_elem = teams[1].css_first("div.match-item-vs-team-score")

            team1_score = team1_score_elem.text().strip() if team1_score_elem else "–"
            team2_score = team2_score_elem.text().strip() if team2_score_elem else "–"

            team1_flag_elem = teams[0].css_first("span.flag")
            team2_flag_elem = teams[1].css_first("span.flag")

            team1_flag = (team1_flag_elem.attributes.get("class", "").replace("flag mod-", "")
                          if team1_flag_elem else "")
            team2_flag = (team2_flag_elem.attributes.get("class", "").replace("flag mod-", "")
                          if team2_flag_elem else "")

            round_event_elem = match_link.css_first("div.match-item-event")
            round_series_elem = match_link.css_first("div.match-item-event-series")
            if round_event_elem and round_series_elem:
                round_series = round_series_elem.text().strip()
                round_stage = round_event_elem.text().replace(round_series, "").strip()
                full_round = f"{round_stage}: {round_series}"
            else:
                full_round = round_series_elem.text().strip() if round_series_elem else "Unknown"

            result.append({
                "round": full_round,
                "team1": team1,
                "team1_flag": team1_flag,
                "team1_score": team1_score,
                "team2": team2,
                "team2_flag": team2_flag,
                "team2_score": team2_score,
                "match_date": current_date,
                "match_time": match_time,
                "match_url": match_url,
            })
    
    return {"status": status, "data": result}
