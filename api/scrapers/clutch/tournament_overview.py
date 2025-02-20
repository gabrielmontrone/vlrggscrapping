import requests
from selectolax.parser import HTMLParser
from utils.utils import headers
from utils.events import EVENTS

def vlr_tournament_overview(event_key):
    """
    Faz o scraping das principais informações do torneio com base no event_key.
    """
    if event_key not in EVENTS:
        raise ValueError(f"Evento '{event_key}' não encontrado no EVENTS.")
    
    event_url = EVENTS[event_key]["url"]
    
    response = requests.get(event_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Falha ao acessar {event_url}. Status Code: {response.status_code}")
    
    html = HTMLParser(response.text)
    
    # Nome do torneio
    tournament_name = html.css_first("h1.wf-title").text(strip=True)
    
    # Descrição
    description_element = html.css_first("h2.event-desc-subtitle")
    tournament_description = description_element.text(strip=True) if description_element else None
    
    # Datas
    date_element = html.css_first("div.event-desc-item-value")
    tournament_dates = date_element.text(strip=True) if date_element else None
    
    # Prêmio
    prize_element = html.css("div.event-desc-item-value")[1]  # Segundo elemento é o prêmio
    tournament_prize = prize_element.text(strip=True) if prize_element else None
    
    # Localização
    location_element = html.css("div.event-desc-item-value")[2]  # Terceiro elemento é a localização
    tournament_location = location_element.text(strip=True) if location_element else None
    
    # Regiões
    regions = [a.text(strip=True) for a in html.css("div.event-desc-inner a")]

    # Extraindo times participantes
    teams = []
    for row in html.css("tr"):  
        team_link = row.css_first("a")
        if team_link and "team" in team_link.attributes["href"]:
            team_name_div = team_link.css_first("div.event-group-team.text-of")
            
            # Pegando o texto bruto e removendo a região
            team_name = team_name_div.text(strip=True) if team_name_div else ""
        
            # Se houver um div filho, ele contém a região, então removemos do nome do time
            region_div = team_name_div.css_first("div.ge-text-light")
            if region_div:
                region_text = region_div.text(strip=True)
                team_name = team_name.replace(region_text, "").strip()

            region = team_link.css_first("div.ge-text-light").text(strip=True)
            team_url = f"https://www.vlr.gg{team_link.attributes['href']}"

            players = get_team_players(team_url)

            teams.append({
                "name": team_name,
                "region": region,
                "url": team_url,
                "players": players
            })
    
    return {
        "name": tournament_name,
        "description": tournament_description,
        "dates": tournament_dates,
        "prize": tournament_prize,
        "location": tournament_location,
        "regions": regions,
        "url": event_url,
        "teams": teams
    }

def get_team_players(team_url):
    """
    Faz o scraping da página de um time para extrair os jogadores.
    """
    response = requests.get(team_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Falha ao acessar {team_url}. Status Code: {response.status_code}")
    
    html = HTMLParser(response.text)
    
    players = []
    
    # Procurar os jogadores na página
    for player_item in html.css("div.team-roster-item"):
        player = {}
        
        # Alias do jogador
        alias_element = player_item.css_first("div.team-roster-item-name-alias")
        if alias_element:
            player['nickname'] = alias_element.text(strip=True)
        
        # Nome real do jogador
        real_name_element = player_item.css_first("div.team-roster-item-name-real")
        if real_name_element:
            player['real_name'] = real_name_element.text(strip=True)
        
        # Link para o perfil do jogador (opcional)
        player_link = player_item.css_first("a")
        if player_link and "player" in player_link.attributes["href"]:
            player['profile_url'] = f"https://www.vlr.gg{player_link.attributes['href']}"
        
        # Adicionar o jogador à lista
        players.append(player)
    
    return players

