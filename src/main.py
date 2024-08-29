import os
from PSNetwork import PSN
#For local test
from dotenv import load_dotenv
load_dotenv()
#End 
NPSSO = os.getenv('PSN_NPSSO')
GITHUB_TOKEN = os.getenv('GH_TOKEN')
GIST_ID = os.getenv('GIST_ID')



if __name__ == '__main__':
    psn = PSN(npsso=NPSSO, language_str = 'en-US')
    psn.access_token, psn.refresh_token = psn.get_access_token()
    if not psn.validate_access_token:
        raise Exception("Invalid tokens")
    games = psn.game_list()
    records = []
    for game in games:
        if(game['concept']['localizedName']['metadata']['zh-Hant'] != None):
            name = game['concept']['localizedName']['metadata']['zh-Hant']
        else:
            name = game['name']
        duration = game['playDuration']
        trophy =  psn.trophy_progress(game['titleId'])
        if(trophy is None):
            continue
        else:
            hours = PSN.get_duration_in_hours(duration)
            record = {
                'name': name,
                'hours': hours,
                'play_duration': f'{hours} hours',
                'total_trophies': sum(trophy['definedTrophies'].values()),
                'earned_trophies': sum(trophy['earnedTrophies'].values())
            }
            record['progress'] = round((record['earned_trophies'] / record['total_trophies']) * 100,2)
            records.append(record)
    records.sort(key = lambda x: x['hours'], reverse= True)
    print(records)




