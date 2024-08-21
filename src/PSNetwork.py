import requests
from HttpRequester import HttpRequester
class PSN:

    def _init__(self, npsso:str=None, access_token:str = None, refresh_token:str = None, language_str = 'en-US'):
        self.npsso = npsso
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.language_str = language_str
        self.auth_endpoint = 'https://ca.account.sony.com/api/authz/v3/'
        self.api_endpoint = 'https://m.np.playstation.com/api/'
        self.profile_endpoint = 'https://us-prof.np.community.playstation.net/'
        self.user_name = None
        self.account_id = None

    def validate_access_token(self) -> bool:
        if not self.access_token:
            return False
        params = {
            'fields': 'npId,onlineId,accountId,avatarUrls,plus'
        }    

        base_addr = self.get_base_address('userProfile')
        requseter = HttpRequester(base_addr, False)
        header = self.compose_header({})
        resp = requseter.get('userProfile/v1/users/me/profile2', params = params, header= header)
        if(resp.status_code == 200):
            record = resp.json()['profile']
            self.user_name = record['onlineId']
            self.account_id = record['accountId']
            return True
        else:
            return False
        
    def refresh_access_token(self) -> tuple[str, str]:
        if not self.refresh_token:
            return None, None
        params = {
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
            'scope': 'psn:mobile.v2.core psn:clientapp',
            'token_format': 'jwt'
        }

        header =  {
            'Authorization': 'Basic MDk1MTUxNTktNzIzNy00MzcwLTliNDAtMzgwNmU2N2MwODkxOnVjUGprYTV0bnRCMktxc1A=',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        header = self.compose_header(header)

        base_addr = self.get_base_address('oauth')
        requseter = HttpRequester(base_addr, False)
        resp = requseter.post('oauth/token', params,header)
        if resp.status_code != 200:
            return None, None
        record = resp.json()
        return record['access_token'], record['refresh_token']
    

    def get_access_token(self) -> tuple[str, str]:
        if not self.npsso:
            raise Exception('You should get the npsso from https://ca.account.sony.com/api/v1/ssocookie')
        params = {
            'access_type': 'offline',
            'client_id': '09515159-7237-4370-9b40-3806e67c0891',
            'redirect_uri': 'com.scee.psxandroid.scecompcall://redirect',
            'response_type': 'code',
            'scope': 'psn:mobile.v2.core psn:clientapp',
        }
        cookie = {'npsso': self.npsso}
        base_addr = self.get_base_address('oauth')
        header = self.compose_header({})
        requester = HttpRequester(base_addr, False)
        resp = requester.get('oauth/authorize', params = params, header = header, allow_redirects = False)
        if(resp.status_code != 200):
            raise Exception('You should get the npsso from https://ca.account.sony.com/api/v1/ssocookie')
        code = resp.headers['Location'].split('code=')[1].split('&')[0]

        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'com.scee.psxandroid.scecompcall://redirect',
            'token_format': 'jwt'
        }

        header = self.compose_header({
            'Authorization': 'Basic MDk1MTUxNTktNzIzNy00MzcwLTliNDAtMzgwNmU2N2MwODkxOnVjUGprYTV0bnRCMktxc1A=',
            'Content-Type': 'application/x-www-form-urlencoded',
        })

        resp = requester.post('oauth/token', params = data, hearder=header)
        if resp.status_code != 200:
            raise Exception("Fail to get Token")
        record = resp.json()
        return record['access_token'], record['refresh_token']

    def game_list(self, offset=0, limit=200):
        base_addr = self.get_base_address('game')
        requester = HttpRequester(base_addr, False)
        params = {
            'limit': limit,
            'offset': offset
        }
        resp = requester.get('gamelist/v2/users/me/titles', params = params)
        if(resp.status_code != 200):
            return None
        record = resp.json()
        games = record['titles']
        next_offset = record['nextOffset']
        if(next_offset):
            games += self.game_list(next_offset)
        return games
    
    def trophy_list(self, offset=0, limit=500):
        base_addr = self.get_base_address('trophy')
        params = {
            'limit':limit,
            'offset': offset,
            'accountId': 'me'
        }
        requester = HttpRequester(base_addr, False)
        resp = requester.get('trophy/v1/users/me/trophyTitles', params = params)
        if(resp.status_code != 200):
            return None
        record =resp.json()
        trophies = resp['trophyTitles']
        next_offset = resp['nextOffset']
        if(next_offset):
            trophies += self.trophy_list(next_offset)
        return trophies
    
    def trophy_progress(self, game_id):
        params = {
            'accountId': 'me',
            'npTitleIds': game_id
        }

        base_addr = self.get_base_address('trophy')
        requester = HttpRequester(base_addr, False)
        resp = requester.get('trophy/v1/users/me/titles/trophyTitles', params = params)
        if(resp.status_code != 200):
            return None
        record = resp.json()
        for title in record['titles']:
            if(title['npTitleId'] == game_id and title['trophyTitles']):
                return title['trophyTitles'][0]
        return None


    # def get_endpoint(self,api) 
    #     if api.startswitch('oauth/'):
    #         return f'{self.auth_endpoint}{api}'        
    #     elif api.startswith('userProfile/'):
    #         return f'{self.profile_endpoint}{api}'
    #     else:
    #         return f'{self.api_endpoint}{api}'

    def get_base_address(self, api) -> str:
        if api.startswitch('oauth/'):
            return self.auth_endpoint    
        elif api.startswith('userProfile/'):
            return self.profile_endpoint
        else:
            return self.api_endpoint
        
    def compose_header(self, header) -> dict:
        if not 'Authorization' in header and self.access_token:
             header['Authorization'] = f'Bearer {self.access_token}'
        if not 'Content-Type' in header:
            header['Content-Type']  = 'application/json'
        if not 'Accept-Language' in header:
            header['Accept-Language'] = self.language_str
        if not 'User-Agent' in header:
            header['User-Agent'] = 'PlayStation/21090100 CFNetwork/1126 Darwin/19.5.0'
        return header