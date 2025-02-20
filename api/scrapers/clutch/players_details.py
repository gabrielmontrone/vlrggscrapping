import requests
import logging
from bs4 import BeautifulSoup  

# Configura o logger para exibir mensagens de depuração
logging.basicConfig(level=logging.DEBUG)


def get_profile_urls_from_tournament():
    """Faz uma requisição ao endpoint do torneio para obter os profile_urls"""
    url = "http://localhost:3001/tournament-overview"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  
        profile_urls = []

        # Itera sobre os times e jogadores, extraindo os profile_urls
        for team in data.get('teams', []):  
            for player in team.get('players', []):  
                profile_urls.append(player.get('profile_url'))  
        
        return profile_urls  
    else:
        print(f"Erro ao acessar o torneio: {response.status_code}")
        return []


def vlr_players_details(profile_url: str):
    """Obtém os agentes e porcentagem de uso a partir da página de perfil"""
    
    # Log de depuração para verificar o profile_url recebido
    logging.debug(f"Received profile_url: {profile_url}")
    
    if not profile_url:
        logging.error("Profile URL is missing.")
        return []

    response = requests.get(profile_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        agents_data = []

        # Encontra a tabela de agentes
        agents_table = soup.find('div', class_='wf-card mod-table mod-dark')
        if not agents_table:
            return []

        # Itera pelas linhas da tabela (pulando o cabeçalho)
        for row in agents_table.select('tbody tr'):
            cells = row.find_all('td')
            
            # Extrai o nome do agente da imagem
            img_tag = row.find('img')
            if not img_tag:
                continue
                
            agent_name = img_tag['src'].split('/')[-1].split('.')[0].capitalize()

            # Extrai a porcentagem da segunda célula com classe 'mod-right'
            usage_cell = cells[1] if len(cells) > 1 else None
            if usage_cell:
                span = usage_cell.find('span')
                if span:
                    # Extrai apenas a porcentagem do texto (ex: "(8) 73%" -> "73%")
                    usage_text = span.get_text(strip=True).split()[-1]
                    agents_data.append({
                        'agent': agent_name,
                        'usage_percent': usage_text
                    })

        # Ordena por maior porcentagem e remove duplicatas mantendo a maior
        unique_agents = {}
        for agent in agents_data:
            current_agent = agent['agent']
            current_percent = float(agent['usage_percent'].rstrip('%'))
            
            # Mantém apenas a maior porcentagem se houver duplicatas
            if current_agent not in unique_agents or current_percent > unique_agents[current_agent]['usage_percent']:
                unique_agents[current_agent] = {
                    'usage_percent': current_percent,
                    'usage_display': agent['usage_percent']
                }

        # Retorna lista formatada com porcentagem
        return [
            {
                'name': agent,
                'usage_percent': f"{data['usage_percent']:.0f}%",
                'usage_raw': data['usage_percent']
            }
            for agent, data in unique_agents.items()
        ]
    else:
        logging.error(f"Falha ao acessar {profile_url}")
        return []
