# 기본적으로 개발을 진행할 때에는 기능단위로 프로젝트 구조를 설정한 뒤 개발을 진행한다.
# 메인으로 실행하는 파일 하나가 있으며, 이 파일에 다른 폴더, 파일들에서 작성한 함수, 클래스, 변수들을 가져와
# 실행하는 식으로 구성하는 것이 좋다. (기능의 분리, 코드 관리의 효율화)

import datetime as dt
from bs4 import BeautifulSoup as bs
import json
import requests

# __name__ == '__main__' 부분은 import해서 사용할 때는 실행되지 않고, 
# 해당 파일을 직접 실행할 때만 실행되는 부분이다.
# 따라서, 해당 파일을 직접 실행하게되면, __name__은 '__main__'이 된다.

def bb_record():
    now = dt.datetime.now()
    ny = now.strftime('%Y')
    nd = now.strftime('%Y%m%d')
    nm = now.strftime('%m')
    print(f'업데이트 시간:{now}')
    x = '4'
    result_lst = []
    for month in range(int(x.zfill(2)), int(nm)+1):
        url=f'https://sports.news.naver.com/kbaseball/schedule/index?date={nd}&month={month}&year={ny}&teamCode='
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        divs = soup.select('#calendarWrap>div')
        for div in divs:
            date=div.select('td')[0].text.strip()
            trs = div.select('tr')
            for tr in trs:
                tds = tr.select('td')
                if tr == trs[0]:
                    hour = tds[1].text.strip()
                    if len(tds) == 3:
                        break
                    elif tr.select('td.add_state'): 
                        away = tr.select('span.team_lft')[0].text
                        asc = tr.select('td>strong>em.vs')[0].text
                        home = tr.select('span.team_rgt')[0].text 
                        hsc = tr.select('span.suspended')[0].text
                        stadium = tds[4].text.strip()
                        bc = tds[3].text.strip()
                        win_pit = ''
                        lose_pit = ''
                        fin_bat = ''
                    elif tr.find_all('img')[2]['alt'] == "전력":
                        away = tr.select('span.team_lft')[0].text 
                        asc = ''
                        home = tr.select('span.team_rgt')[0].text
                        hsc = ''
                        stadium = tds[5].text.strip()
                        bc = tds[4].text.strip()
                        win_pit = ''
                        lose_pit = ''
                        fin_bat = ''
                    elif tr.find_all('img')[2]['alt'] == "경기영상":
                        away = tr.select('span.team_lft')[0].text 
                        asc = ''
                        home = tr.select('span.team_rgt')[0].text
                        hsc = ''
                        stadium = tds[4].text.strip()
                        bc = tds[3].text.strip()
                        win_pit = ''
                        lose_pit = ''
                        fin_bat = ''
                    else:
                        away = tr.select('span.team_lft')[0].text
                        asc = tr.select('strong.td_score')[0].text.split(':')[0]
                        home = tr.select('span.team_rgt')[0].text 
                        hsc = tr.select('strong.td_score')[0].text.split(':')[1]
                        stadium = tds[5].text.strip()
                        bc = tds[4].text.strip()
                        raw_record_url = tr.select('a')[0]['href'].replace('game', 'games')
                        record_url = 'https://api-gw.sports.naver.com/schedule'+raw_record_url
                        record_rp = requests.get(record_url)
                        record = json.loads(record_rp.text)
                        pit_record = record['result']['recordData']['pitchersBoxscore']
                        bat_record = record['result']['recordData']['etcRecords']
                        fin_bat_name = bat_record[0]['result'].split('(')[0]
                        bat_score_record = record['result']['recordData']['battersBoxscore']
                        win_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '승'] or \
                                        [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '승']
                        lose_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '패'] or \
                                        [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '패']
                        fin_bat_info = [bat_info for bat_info in list(bat_score_record.values())[2] if bat_info['name'] == fin_bat_name] or \
                                        [bat_info for bat_info in list(bat_score_record.values())[3] if bat_info['name'] == fin_bat_name]
                        for wp in win_pit_info:
                            win_pit_name = wp['name'] + '(' + wp['wls'] + ')'
                            win_pit_inn = wp['inn']
                            win_pit_hit = str(wp['hit']).replace('0','무')
                            win_pit_ball = str(wp['bbhp']).replace('0','무')
                            win_pit_k = wp['kk']
                            win_pit_loss = str(wp['r']).replace('0','무')
                            win_pit_er = str(wp['er']).replace('0','무')
                            win_pit_nb = wp['bf']
                            win_pit_era = wp['era']
                            win_pit = {win_pit_name : [f'{win_pit_inn}이닝, {win_pit_hit}피안타, {win_pit_ball}사사구, {win_pit_k}탈삼진, {win_pit_loss}실점({win_pit_er}자책), 투구수{win_pit_nb}개, 평균자책{win_pit_era}']}
                        for lp in lose_pit_info:
                            lose_pit_name = lp['name'] + '(' + lp['wls'] + ')'
                            lose_pit_inn = lp['inn']
                            lose_pit_hit = str(lp['hit']).replace('0','무')
                            lose_pit_ball = str(lp['bbhp']).replace('0','무')
                            lose_pit_k = lp['kk']
                            lose_pit_loss = str(lp['r']).replace('0','무')
                            lose_pit_er = str(lp['er']).replace('0','무')
                            lose_pit_nb = lp['bf']
                            lose_pit_era = lp['era']
                            lose_pit = {lose_pit_name : [f'{lose_pit_inn}이닝, {lose_pit_hit}피안타, {lose_pit_ball}사사구, {lose_pit_k}탈삼진, {lose_pit_loss}실점({lose_pit_er}자책), 투구수 {lose_pit_nb}개, 평균자책 {lose_pit_era}']}
                        for fb in fin_bat_info:
                            fin_bat_nao = fin_bat_name + '(' + str(fb['batOrder']) +'번타자' + ')'
                            fin_bat_pa = fb['ab']
                            fin_bat_hit = fb['hit']
                            fin_bat_hr = fb['hr']
                            fin_bat_ball = fb['bb']
                            fin_bat_k = fb['kk']
                            fin_bat_hp = fb['rbi']
                            fin_bat_pt = fb['run']
                            fin_bat_avg = fb['hra']
                            fin_bat = {fin_bat_nao : [f'{fin_bat_pa}타수, {fin_bat_hit}안타({fin_bat_hr}홈런), {fin_bat_ball}볼넷, {fin_bat_k}삼진, {fin_bat_hp}타점, {fin_bat_pt}득점, 시즌타율 {fin_bat_avg}']}
                else:
                    hour = tds[0].text.strip()
                    if len(tds) == 3:
                        break
                    elif tr.select('td.add_state'):
                        away = tr.select('span.team_lft')[0].text 
                        asc = tr.select('td>strong>em.vs')[0].text
                        home = tr.select('span.team_rgt')[0].text
                        hsc = tr.select('span.suspended')[0].text
                        stadium = tds[3].text.strip()
                        bc = tds[2].text.strip()
                        win_pit = ''
                        lose_pit = ''
                        fin_bat = ''
                    elif tr.find_all('img')[2]['alt'] == "전력":
                        away = tr.select('span.team_lft')[0].text 
                        asc = ''
                        home = tr.select('span.team_rgt')[0].text
                        hsc = ''
                        stadium = tds[4].text.strip()
                        bc = tds[3].text.strip()
                        win_pit = ''
                        lose_pit = ''
                        fin_bat = ''
                    elif tr.find_all('img')[2]['alt'] == "경기영상":
                        away = tr.select('span.team_lft')[0].text 
                        asc = ''
                        home = tr.select('span.team_rgt')[0].text
                        hsc = ''
                        stadium = tds[4].text.strip()
                        bc = tds[3].text.strip()
                        win_pit = ''
                        lose_pit = ''
                        fin_bat = ''
                    else:
                        away = tr.select('span.team_lft')[0].text
                        asc = tr.select('strong.td_score')[0].text.split(':')[0]
                        home = tr.select('span.team_rgt')[0].text 
                        hsc = tr.select('strong.td_score')[0].text.split(':')[1]
                        stadium = tds[4].text.strip()
                        bc = tds[3].text.strip()
                        raw_record_url = tr.select('a')[0]['href'].replace('game', 'games')
                        record_url = 'https://api-gw.sports.naver.com/schedule'+raw_record_url
                        record_rp = requests.get(record_url)
                        record = json.loads(record_rp.text)
                        pit_record = record['result']['recordData']['pitchersBoxscore']
                        bat_record = record['result']['recordData']['etcRecords']
                        fin_bat_name = bat_record[0]['result'].split('(')[0]
                        bat_score_record = record['result']['recordData']['battersBoxscore']
                        win_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '승'] or \
                                            [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '승']
                        lose_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '패'] or \
                                            [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '패']
                        fin_bat_info = [bat_info for bat_info in list(bat_score_record.values())[2] if bat_info['name'] == fin_bat_name] or \
                                                                    [bat_info for bat_info in list(bat_score_record.values())[3] if bat_info['name'] == fin_bat_name]
                        for wp in win_pit_info:
                            win_pit_name = wp['name'] + '(' + wp['wls'] + ')'
                            win_pit_inn = wp['inn']
                            win_pit_hit = str(wp['hit']).replace('0','무')
                            win_pit_ball = str(wp['bbhp']).replace('0','무')
                            win_pit_k = wp['kk']
                            win_pit_loss = str(wp['r']).replace('0','무')
                            win_pit_er = str(wp['er']).replace('0','무')
                            win_pit_nb = wp['bf']
                            win_pit_era = wp['era']
                            win_pit={win_pit_name : [f'{win_pit_inn}이닝, {win_pit_hit}피안타, {win_pit_ball}사사구, {win_pit_k}탈삼진, {win_pit_loss}실점({win_pit_er}자책), 투구수{win_pit_nb}개, 평균자책{win_pit_era}']}
                        for lp in lose_pit_info:
                            lose_pit_name = lp['name'] + '(' + lp['wls'] + ')'
                            lose_pit_inn = lp['inn']
                            lose_pit_hit = str(lp['hit']).replace('0','무')
                            lose_pit_ball = str(lp['bbhp']).replace('0','무')
                            lose_pit_k = lp['kk']
                            lose_pit_loss = str(lp['r']).replace('0','무')
                            lose_pit_er = str(lp['er']).replace('0','무')
                            lose_pit_nb = lp['bf']
                            lose_pit_era = lp['era']
                            lose_pit = {lose_pit_name : [f'{lose_pit_inn}이닝, {lose_pit_hit}피안타, {lose_pit_ball}사사구, {lose_pit_k}탈삼진, {lose_pit_loss}실점({lose_pit_er}자책), 투구수 {lose_pit_nb}개, 평균자책 {lose_pit_era}']}
                        for fb in fin_bat_info:
                            fin_bat_nao = fin_bat_name + '(' + str(fb['batOrder']) +'번타자' + ')'
                            fin_bat_pa = fb['ab']
                            fin_bat_hit = fb['hit']
                            fin_bat_hr = fb['hr']
                            fin_bat_ball = fb['bb']
                            fin_bat_k = fb['kk']
                            fin_bat_hp = fb['rbi']
                            fin_bat_pt = fb['run']
                            fin_bat_avg = fb['hra']
                            fin_bat = {fin_bat_nao : [f'{fin_bat_pa}타수, {fin_bat_hit}안타({fin_bat_hr}홈런), {fin_bat_ball}볼넷, {fin_bat_k}삼진, {fin_bat_hp}타점, {fin_bat_pt}득점, 시즌타율 {fin_bat_avg}']}
                                        
                result_lst.append([date, hour, away, asc, home, hsc, stadium, bc, win_pit, lose_pit, fin_bat])
    return result_lst
print(bb_record())