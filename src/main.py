import os
from PSNetwork import PSN
#For local test
# from dotenv import load_dotenv
# load_dotenv()
#End 
NPSSO = os.getenv('PSN_NPSSO')
GITHUB_TOKEN = os.getenv('GH_TOKEN')
GH_REPO = os.getenv('GH_REPO')
GIST_ID = os.getenv('GIST_ID')



if __name__ == '__main__':
    psn = PSN(npsso=NPSSO, language = 'en-US')
    psn.access_token, psn.refresh_token = psn.get_access_token()
    if not psn.validate_access_token:
        raise Exception("Invalid tokens")
    games = psn.game_list()
    for game in games:
        print(game)







