import os
from PSNetwork import PSN
import utils
#For local test
# from dotenv import load_dotenv
# load_dotenv()
#End 
NPSSO = os.getenv('PSN_NPSSO')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
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
    content = ''
    lines = []
    max_txt_width = max([ utils.txt_width(utils.truncate_name(record['name'],23)) for record in records])
    if(max_txt_width > 23):
        max_txt_width +=1
    else:
        max_txt_width = 23
    for record in records:
        truncate_name = utils.truncate_name(record['name'],23)
        if(utils.wide_char(truncate_name)> 10):
            padding = max_txt_width - utils.txt_width(truncate_name)-1
        else:
            padding = max_txt_width - utils.txt_width(truncate_name)
        line = [
            f'{truncate_name}{" "*padding}',
            record['play_duration'].ljust(11),
            utils.generate_progress_bar(record['progress'], 8),
            f'{record["progress"]:.2f}%'.rjust(6)
        ]
        content += ' '.join(line)+'\n'
    try:
        utils.update_gist(GITHUB_TOKEN, GIST_ID, content)
        print("Update Gist success with the following content")
        print(content)
    except Exception as ex:
        print("Update fail")
        print(repr(ex))

