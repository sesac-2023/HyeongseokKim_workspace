#라이브러리 임포트
import datetime as dt
from bs4 import BeautifulSoup as bs
import requests
from datetime import timedelta
import json
from baseball_db import db

#이전의 경기기록 크롤링하는 클래스
class weekagoCrawler:
    def __init__(self) -> None:
        pass

    def crawl_game():
        now = dt.datetime.now()
        weekago = now  - timedelta(days=7)
        aymd, ay, am = weekago.strftime('%Y%m%d'), weekago.strftime('%Y'), weekago.strftime('%m')
        x = '4'
        result_lst = []
        for month in range(int(x.zfill(2)), int(am)+1):
            url=f'https://sports.news.naver.com/kbaseball/schedule/index?date={aymd}&month={month}&year={ay}&teamCode='
            response, soup, divs = requests.get(url), bs(response.text, 'lxml'), soup.select('#calendarWrap>div')
            for div in divs:
                mo=format(int(div.select('td')[0].text.strip().replace('.',' ').split(' ')[0]), '02')
                day=format(int(div.select('td')[0].text.strip().replace('.',' ').split(' ')[1]), '02')
                trs = div.select('tr')
                for tr in trs:
                    tds = tr.select('td')
                    if tr == trs[0]:
                        hour, playedat, form = tds[1].text.strip(), f'{ay}-{mo}-{day} {hour}:00', '%Y-%m-%d %H:%M:%S'
                        if len(tds) == 3:
                            break
                        elif tr.select('td.add_state'):
                            dt_playedat= dt.datetime.strptime(playedat, form) 
                            away = tr.select('span.team_lft')[0].text
                            asc = tr.select('td>strong>em.vs')[0].text
                            home = tr.select('span.team_rgt')[0].text 
                            hsc = tr.select('span.suspended')[0].text
                            stadium = tds[4].text.strip()
                            bc = tds[3].text.strip()
                        elif tr.find_all('img')[2]['alt'] == "경기결과":
                            dt_playedat= dt.datetime.strptime(playedat, form)
                            away = tr.select('span.team_lft')[0].text
                            asc = tr.select('strong.td_score')[0].text.split(':')[0]
                            home = tr.select('span.team_rgt')[0].text 
                            hsc = tr.select('strong.td_score')[0].text.split(':')[1]
                            stadium = tds[5].text.strip()
                            bc = tds[4].text.strip()
                        else:
                            break
                    else:
                        hour, playedat, form = tds[0].text.strip(), f'{ay}-{mo}-{day} {hour}:00', '%Y-%m-%d %H:%M:%S'
                        if len(tds) == 3:
                            break
                        elif tr.select('td.add_state'):
                            dt_playedat= dt.datetime.strptime(playedat, form)
                            away = tr.select('span.team_lft')[0].text 
                            asc = tr.select('td>strong>em.vs')[0].text
                            home = tr.select('span.team_rgt')[0].text
                            hsc = tr.select('span.suspended')[0].text
                            stadium = tds[3].text.strip()
                            bc = tds[2].text.strip()
                        elif tr.find_all('img')[2]['alt'] == "경기결과":
                            dt_playedat= dt.datetime.strptime(playedat, form)
                            away = tr.select('span.team_lft')[0].text
                            asc = tr.select('strong.td_score')[0].text.split(':')[0]
                            home = tr.select('span.team_rgt')[0].text 
                            hsc = tr.select('strong.td_score')[0].text.split(':')[1]
                            stadium = tds[4].text.strip()
                            bc = tds[3].text.strip()
                        else:
                            break
                    result_lst.append([dt_playedat, away, asc, home, hsc, stadium, bc])
        return result_lst
    
    def crawl_record():
        now = dt.datetime.now()
        weekago = now  - timedelta(days=7)
        aymd, ay, am = weekago.strftime('%Y%m%d'), weekago.strftime('%Y'), weekago.strftime('%m')
        x = '4'
        result_lst = []
        for month in range(int(x.zfill(2)), int(am)+1):
            url=f'https://sports.news.naver.com/kbaseball/schedule/index?date={aymd}&month={month}&year={ay}&teamCode='
            response, soup, divs = requests.get(url), bs(response.text, 'lxml'), soup.select('#calendarWrap>div')
            for div in divs:
                trs = div.select('tr')
                for tr in trs:
                    tds = tr.select('td')
                    if tr == trs[0]:
                        if len(tds) == 3:
                            break
                        elif tr.select('td.add_state'): 
                            win_pit_name = '' ; lose_pit_name = '' ; fin_bat_name = ''
                            win_pit_inn = '' ; lose_pit_inn = '' ; fin_bat_abs = ''
                            win_pit_hit = '' ; lose_pit_hit = '' ; fin_bat_hthr = ''
                            win_pit_bbhp = '' ; lose_pit_bbhp = '' ; fin_bat_bb = ''
                            win_pit_kk = '' ; lose_pit_kk = '' ; fin_bat_kk = ''
                            win_pit_lr = ''; lose_pit_lr = '' ; fin_bat_rbi = ''
                            win_pit_pn = '' ; lose_pit_pn = '' ; fin_bat_run = ''
                            win_pit_era = ''; lose_pit_era = '' ; fin_bat_ba = ''
                            win_pit = (win_pit_name, win_pit_inn, win_pit_hit, win_pit_bbhp, win_pit_kk, win_pit_lr, win_pit_pn, win_pit_era)
                            lose_pit = (lose_pit_name, lose_pit_inn, lose_pit_hit, lose_pit_bbhp, lose_pit_kk, lose_pit_lr, lose_pit_pn, lose_pit_era)
                            fin_bat = (fin_bat_name, fin_bat_abs, fin_bat_hthr, fin_bat_bb, fin_bat_kk, fin_bat_rbi, fin_bat_run, fin_bat_ba)
                        elif tr.find_all('img')[2]['alt'] == "경기결과":
                            if tr.select('strong.td_score')[0].text.split(':')[0] == tr.select('strong.td_score')[0].text.split(':')[1]:
                                win_pit_name = '' ; lose_pit_name = '' ; fin_bat_name = ''
                                win_pit_inn = '' ; lose_pit_inn = '' ; fin_bat_abs = ''
                                win_pit_hit = '' ; lose_pit_hit = '' ; fin_bat_hthr = ''
                                win_pit_bbhp = '' ; lose_pit_bbhp = '' ; fin_bat_bb = ''
                                win_pit_kk = '' ; lose_pit_kk = '' ; fin_bat_kk = ''
                                win_pit_lr = ''; lose_pit_lr = '' ; fin_bat_rbi = ''
                                win_pit_pn = '' ; lose_pit_pn = '' ; fin_bat_run = ''
                                win_pit_era = ''; lose_pit_era = '' ; fin_bat_ba = ''
                                win_pit = (win_pit_name, win_pit_inn, win_pit_hit, win_pit_bbhp, win_pit_kk, win_pit_lr, win_pit_pn, win_pit_era)
                                lose_pit = (lose_pit_name, lose_pit_inn, lose_pit_hit, lose_pit_bbhp, lose_pit_kk, lose_pit_lr, lose_pit_pn, lose_pit_era)
                                fin_bat = (fin_bat_name, fin_bat_abs, fin_bat_hthr, fin_bat_bb, fin_bat_kk, fin_bat_rbi, fin_bat_run, fin_bat_ba)
                            else:
                                raw_record_url = tr.select('a')[0]['href'].replace('game', 'games')
                                record_url = 'https://api-gw.sports.naver.com/schedule'+raw_record_url
                                record_rp, record = requests.get(record_url), json.loads(record_rp.text)
                                pit_record = record['result']['recordData']['pitchersBoxscore']
                                win_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '승'] or \
                                                [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '승']
                                lose_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '패'] or \
                                                [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '패']
                                for wp in win_pit_info:
                                    win_pit_name, win_pit_inn = wp['name'], wp['inn']
                                    win_pit_hit, win_pit_bbhp, win_pit_kk= str(wp['hit']), str(wp['bbhp']), str(wp['kk'])
                                    win_pit_lr = str(wp['r'])+'('+str(wp['er'])+')'
                                    win_pit_pn, win_pit_era = str(wp['bf']), str(wp['era'])
                                    win_pit = (win_pit_name, win_pit_inn, win_pit_hit, win_pit_bbhp, win_pit_kk, win_pit_lr, win_pit_pn, win_pit_era)
                                for lp in lose_pit_info:
                                    lose_pit_name, lose_pit_inn = lp['name'], lp['inn']
                                    lose_pit_hit, lose_pit_bbhp, lose_pit_kk = str(lp['hit']), str(lp['bbhp']), str(lp['kk'])
                                    lose_pit_lr = str(lp['r'])+'('+str(lp['er'])+')'
                                    lose_pit_pn, lose_pit_era = str(lp['bf']), str(lp['era'])
                                    lose_pit = (lose_pit_name, lose_pit_inn, lose_pit_hit, lose_pit_bbhp, lose_pit_kk, lose_pit_lr, lose_pit_pn, lose_pit_era)
                                bat_record, bat_score_record = record['result']['recordData']['etcRecords'], record['result']['recordData']['battersBoxscore']
                                fin_bat_name = bat_record[0]['result'].split('(')[0]
                                fin_bat_info = [bat_info for bat_info in list(bat_score_record.values())[2] if bat_info['name'] == fin_bat_name] or \
                                                [bat_info for bat_info in list(bat_score_record.values())[3] if bat_info['name'] == fin_bat_name]
                                for fb in fin_bat_info:
                                    fin_bat_abs = str(fb['ab'])
                                    fin_bat_hthr = str(fb['hit'])+'('+str(fb['hr'])+')'
                                    fin_bat_bb, fin_bat_kk = str(fb['bb']), str(fb['kk'])
                                    fin_bat_rbi, fin_bat_run, fin_bat_ba = str(fb['rbi']), str(fb['run']), fb['hra']
                                    fin_bat = (fin_bat_name, fin_bat_abs, fin_bat_hthr, fin_bat_bb, fin_bat_kk, fin_bat_rbi, fin_bat_run, fin_bat_ba)
                        else:
                            break
                    else:
                        if len(tds) == 3:
                            break
                        if tr.select('td.add_state'): 
                            win_pit_name = '' ; lose_pit_name = '' ; fin_bat_name = ''
                            win_pit_inn = '' ; lose_pit_inn = '' ; fin_bat_abs = ''
                            win_pit_hit = '' ; lose_pit_hit = '' ; fin_bat_hthr = ''
                            win_pit_bbhp = '' ; lose_pit_bbhp = '' ; fin_bat_bb = ''
                            win_pit_kk = '' ; lose_pit_kk = '' ; fin_bat_kk = ''
                            win_pit_lr = ''; lose_pit_lr = '' ; fin_bat_rbi = ''
                            win_pit_pn = '' ; lose_pit_pn = '' ; fin_bat_run = ''
                            win_pit_era = ''; lose_pit_era = '' ; fin_bat_ba = ''
                            win_pit = (win_pit_name, win_pit_inn, win_pit_hit, win_pit_bbhp, win_pit_kk, win_pit_lr, win_pit_pn, win_pit_era)
                            lose_pit = (lose_pit_name, lose_pit_inn, lose_pit_hit, lose_pit_bbhp, lose_pit_kk, lose_pit_lr, lose_pit_pn, lose_pit_era)
                            fin_bat = (fin_bat_name, fin_bat_abs, fin_bat_hthr, fin_bat_bb, fin_bat_kk, fin_bat_rbi, fin_bat_run, fin_bat_ba)
                        elif tr.find_all('img')[2]['alt'] == "경기결과":
                            if tr.select('strong.td_score')[0].text.split(':')[0] == tr.select('strong.td_score')[0].text.split(':')[1]:
                                win_pit_name = '' ; lose_pit_name = '' ; fin_bat_name = ''
                                win_pit_inn = '' ; lose_pit_inn = '' ; fin_bat_abs = ''
                                win_pit_hit = '' ; lose_pit_hit = '' ; fin_bat_hthr = ''
                                win_pit_bbhp = '' ; lose_pit_bbhp = '' ; fin_bat_bb = ''
                                win_pit_kk = '' ; lose_pit_kk = '' ; fin_bat_kk = ''
                                win_pit_lr = ''; lose_pit_lr = '' ; fin_bat_rbi = ''
                                win_pit_pn = '' ; lose_pit_pn = '' ; fin_bat_run = ''
                                win_pit_era = ''; lose_pit_era = '' ; fin_bat_ba = ''
                                win_pit = (win_pit_name, win_pit_inn, win_pit_hit, win_pit_bbhp, win_pit_kk, win_pit_lr, win_pit_pn, win_pit_era)
                                lose_pit = (lose_pit_name, lose_pit_inn, lose_pit_hit, lose_pit_bbhp, lose_pit_kk, lose_pit_lr, lose_pit_pn, lose_pit_era)
                                fin_bat = (fin_bat_name, fin_bat_abs, fin_bat_hthr, fin_bat_bb, fin_bat_kk, fin_bat_rbi, fin_bat_run, fin_bat_ba)
                            else:
                                raw_record_url = tr.select('a')[0]['href'].replace('game', 'games')
                                record_url = 'https://api-gw.sports.naver.com/schedule'+raw_record_url
                                record_rp, record = requests.get(record_url), json.loads(record_rp.text)
                                pit_record = record['result']['recordData']['pitchersBoxscore']
                                win_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '승'] or \
                                                [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '승']
                                lose_pit_info = [pit_info for pit_info in list(pit_record.values())[0] if pit_info['wls'] == '패'] or \
                                                [pit_info for pit_info in list(pit_record.values())[1] if pit_info['wls'] == '패']
                                for wp in win_pit_info:
                                    win_pit_name, win_pit_inn = wp['name'], wp['inn']
                                    win_pit_hit, win_pit_bbhp, win_pit_kk= str(wp['hit']), str(wp['bbhp']), str(wp['kk'])
                                    win_pit_lr = str(wp['r'])+'('+str(wp['er'])+')'
                                    win_pit_pn, win_pit_era = str(wp['bf']), str(wp['era'])
                                    win_pit = (win_pit_name, win_pit_inn, win_pit_hit, win_pit_bbhp, win_pit_kk, win_pit_lr, win_pit_pn, win_pit_era)
                                for lp in lose_pit_info:
                                    lose_pit_name, lose_pit_inn = lp['name'], lp['inn']
                                    lose_pit_hit, lose_pit_bbhp, lose_pit_kk = str(lp['hit']), str(lp['bbhp']), str(lp['kk'])
                                    lose_pit_lr = str(lp['r'])+'('+str(lp['er'])+')'
                                    lose_pit_pn, lose_pit_era = str(lp['bf']), str(lp['era'])
                                    lose_pit = (lose_pit_name, lose_pit_inn, lose_pit_hit, lose_pit_bbhp, lose_pit_kk, lose_pit_lr, lose_pit_pn, lose_pit_era)
                                bat_record, bat_score_record = record['result']['recordData']['etcRecords'], record['result']['recordData']['battersBoxscore']
                                fin_bat_name = bat_record[0]['result'].split('(')[0]
                                fin_bat_info = [bat_info for bat_info in list(bat_score_record.values())[2] if bat_info['name'] == fin_bat_name] or \
                                                    [bat_info for bat_info in list(bat_score_record.values())[3] if bat_info['name'] == fin_bat_name]
                                for fb in fin_bat_info:
                                    fin_bat_abs = str(fb['ab'])
                                    fin_bat_hthr = str(fb['hit'])+'('+str(fb['hr'])+')'
                                    fin_bat_bb, fin_bat_kk = str(fb['bb']), str(fb['kk'])
                                    fin_bat_rbi, fin_bat_run, fin_bat_ba = str(fb['rbi']), str(fb['run']), fb['hra']
                                    fin_bat = (fin_bat_name, fin_bat_abs, fin_bat_hthr, fin_bat_bb, fin_bat_kk, fin_bat_rbi, fin_bat_run, fin_bat_ba)
                        else:
                            break
                    result_lst.append([win_pit,lose_pit,fin_bat])
            ID_list=list(db.select_all())
            wp_ordered_lst=[] ; lp_ordered_lst=[]; fb_ordered_lst=[]
            for i in range(len(result_lst)):
                wp_ordered_lst.append(result_lst[i][0])
                lp_ordered_lst.append(result_lst[i][1])
                fb_ordered_lst.append(result_lst[i][2])
            nwp_ordered_lst=[] ; nlp_ordered_lst=[]; nfb_ordered_lst=[]
            for wo in range(len(wp_ordered_lst)):
                tem_lst_1=[ID_list[wo]+wp_ordered_lst[wo]]
                nwp_ordered_lst.append(tem_lst_1)
            for lo in range(len(lp_ordered_lst)):
                tem_lst_2=[ID_list[lo]+lp_ordered_lst[lo]]
                nlp_ordered_lst.append(tem_lst_2)
            for fo in range(len(fb_ordered_lst)):
                tem_lst_3=[ID_list[fo]+fb_ordered_lst[fo]]
                nfb_ordered_lst.append(tem_lst_3)
            wp_lst = [x for sublist in nwp_ordered_lst for x in sublist]
            lp_lst = [x for sublist in nlp_ordered_lst for x in sublist]
            fb_lst = [x for sublist in nfb_ordered_lst for x in sublist]
        return wp_lst, lp_lst, fb_lst