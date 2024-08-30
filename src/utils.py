import math
import unicodedata
from HttpRequester import HttpRequester
def truncate_name(name, length):
    if(len(name) > length):
        return f'{name[:length-3]}...'
    else:
        return name

def generate_progress_bar(perc, size):
    syms = '░█'
    progress_bar = math.ceil((perc * size) / 100)
    if(progress_bar >= size):
        return syms[1] * size
    else:
        return syms[1] * progress_bar + syms[0] * (size-progress_bar)
   

def wide_char(txt:str):
    return sum(unicodedata.east_asian_width(x) == 'W' for x in txt)

def txt_width(txt:str):
    return len(txt) + wide_char(txt)

def list_gist(token:str):
    requester = HttpRequester('https://api.github.com/gists/', False)
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    resp = requester.get('public',header= headers)
    print(resp.json())
    
def update_gist(token:str, gist_id:str, content:str):
    # url = f'https://api.github.com/gists/{gist_id}'
    requester = HttpRequester('https://api.github.com/gists/', False)
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    resp = requester.get(gist_id,header= headers)
    if(resp.status_code != 200):
        raise Exception(f'Failed to get gist:{gist_id}, status code:{resp.status_code} response text:{resp.text}')
    gist = resp.json()
    file_name = list(gist['files'].keys())[0]
    data = {
        'files': {
            file_name: {
                # 'filename': 'playstation-box',
                'content': content
            }
        }
    }
    resp = requester.patch(gist_id, data, headers)
    if(resp.status_code != 200):
         raise Exception(f'Failed to update gist: {gist_id}, status code: {resp.status_code} response text: {resp.text}')
    