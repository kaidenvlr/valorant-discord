import requests
from bs4 import BeautifulSoup
import discord


def tracker_current_season(name: str, tag: str):
    url = f"https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview"
    site = requests.get(url)
    print("curr_season", site.status_code)

    if site.status_code == 200:
        soup = BeautifulSoup(site.text, "html.parser")

        result = {"status_code": "ok"}
        labels = ['current_rank', 'max_rank', 'adr', 'kd', 'hs', 'winrate']
        i = 0
        containers = soup.findAll('div', class_="rating-content")
        if containers == []:
            result['status_code'] = 410
        else:
            for rank in containers:
                result[labels[i]] = {
                    'img': rank.find('img')['src'],
                    'value': rank.find('div', class_='value').text.strip()
                }
                i += 1

            for stat in soup.findAll('div', class_="stat align-left giant expandable"):
                result[labels[i]] = stat.find('span', class_="value").text
                i += 1
        return result

    elif site.status_code == 403:
        return {"status_code": 403}

    elif site.status_code == 451:
        return {"status_code": 404}

    else:
        return {"status_code": 1000}


def tracker_all_seasons(name: str, tag: str):
    url = f"https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview?season=all"
    site = requests.get(url)

    if site.status_code == 200:
        soup = BeautifulSoup(site.text, "html.parser")

        result = {"status_code": "ok"}
        labels = ['current_rank', 'max_rank', 'adr', 'kd', 'hs', 'winrate']
        i = 0
        containers = soup.findAll('div', class_="rating-content")
        print(containers)
        if containers == []:
            result['status_code'] = 410
        else:
            for rank in containers:
                result[labels[i]] = {
                    'img': rank.find('img')['src'],
                    'value': rank.find('div', class_='value').text.strip()
                }
                i += 1

            for stat in soup.findAll('div', class_="stat align-left giant expandable"):
                result[labels[i]] = stat.find('span', class_="value").text
                i += 1

        return result

    elif site.status_code == 403:
        return {"status_code": 403}

    elif site.status_code == 451:
        return {"status_code": 404}

    elif site.status_code == 404:
        return {"status_code": 404}

    else:
        return {"status_code": 1000}


def tracker_embed(nickname: str, tag: str):
    response_current_season = tracker_current_season(nickname, tag)
    response_all_seasons = tracker_all_seasons(nickname, tag)
    result = {}
    if response_current_season['status_code'] == 'ok' and response_all_seasons['status_code'] == 'ok':
        result['status'] = 'ok'

        current_season = discord.Embed(
            title=f"???????????????????? {nickname}#{tag} ???? ???????? ??????",
            description=f"?????????????? ????????: {response_current_season['current_rank']['value']}\n"
                        f"????: {response_current_season['kd']}\n"
                        f"?????????????? ???????? ???? ??????????: {response_current_season['adr']}\n"
                        f"?????????????? ????????????????: {response_current_season['hs']}\n"
                        f"??????????????: {response_current_season['winrate']}"
        )
        current_season.set_thumbnail(url=response_current_season['current_rank']['img'])

        all_seasons = discord.Embed(
            title=f"???????????????????? {nickname}#{tag} ???? ?????? ??????????",
            description=f"???????????????????????? ????????: {response_current_season['max_rank']['value']}\n"
                        f"????: {response_all_seasons['kd']}\n"
                        f"?????????????? ???????? ???? ??????????: {response_all_seasons['adr']}\n"
                        f"?????????????? ????????????????: {response_all_seasons['hs']}\n"
                        f"??????????????: {response_all_seasons['winrate']}"
        )
        all_seasons.set_thumbnail(url=response_current_season['max_rank']['img'])

        embeds = [
            current_season,
            all_seasons
        ]

        result['embeds'] = embeds
    elif response_current_season['status_code'] == 404 or response_all_seasons['status_code'] == 404:
        result['status'] = 'error'
        result['embed'] = discord.Embed(title="", description="???? ???? ???????????????????????????????? ?? tracker.gg")
    elif response_current_season['status_code'] == 403 or response_all_seasons['status_code'] == 403:
        result['status'] = 'error'
        result['embed'] = discord.Embed(title="", description="???????????? ???????????????? ????????????")
    else:
        result['status'] = 'error'
        result['embed'] = discord.Embed(title="", description="???????????????? ?????????????????????? ????????????, ???????????????????? ??????????????")

    return result
