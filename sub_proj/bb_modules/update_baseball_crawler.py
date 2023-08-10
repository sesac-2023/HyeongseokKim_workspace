#라이브러리 임포트
import datetime as dt
from bs4 import BeautifulSoup as bs
import requests
from datetime import timedelta
import json
from bb_modules.baseball_db import db

#어제 경기기록 크롤링하는 클래스
class yesterCrawler:
    def __init__(self) -> None:
        pass

    def crawl_ytgame(): #하루 전 경기결과를 크롤링해주는 함수
        now = dt.datetime.now()
        yester = now  - timedelta(days=1)
        yymd, yy, yd, ym = yester.strftime('%Y%m%d'), yester.strftime('%Y'), yester.strftime('%d'), yester.strftime('%m')
        result_lst = []
        url=f'https://sports.news.naver.com/kbaseball/schedule/index?date={yymd}&month={ym}&year={yy}&teamCode='
        response = requests.get(url); soup = bs(response.text, 'lxml'); divs = soup.select('#calendarWrap>div')
        for div in divs:
            mo=format(int(div.select('td')[0].text.strip().replace('.',' ').split(' ')[0]), '02')
            day=format(int(div.select('td')[0].text.strip().replace('.',' ').split(' ')[1]), '02')
            playeddate, yesterdate, form1=f'{yy}-{mo}-{day}', f'{yy}-{ym}-{yd}', '%Y-%m-%d'
            dt_playeddate, dt_yesterdate = dt.datetime.strptime(playeddate, form1), dt.datetime.strptime(yesterdate, form1)
            if dt_playeddate == dt_yesterdate:
                trs = div.select('tr')
                for tr in trs:
                    tds = tr.select('td')
                    if len(tds) == 3:
                            break
                    else:
                        if tr == trs[0]:
                            hour = tds[1].text.strip()
                            playedat, form2 = f'{yy}-{mo}-{day} {hour}:00', '%Y-%m-%d %H:%M:%S'
                            if tr.select('td.add_state'):
                                dt_playedat= dt.datetime.strptime(playedat, form2) 
                                away, asc = tr.select('span.team_lft')[0].text, tr.select('td>strong>em.vs')[0].text
                                home, hsc = tr.select('span.team_rgt')[0].text, tr.select('span.suspended')[0].text
                                stadium, bc = tds[4].text.strip(), tds[3].text.strip()
                            elif tr.find_all('img')[2]['alt'] == "경기결과":
                                dt_playedat= dt.datetime.strptime(playedat, form2)
                                away, asc= tr.select('span.team_lft')[0].text, tr.select('strong.td_score')[0].text.split(':')[0]
                                home, hsc = tr.select('span.team_rgt')[0].text, tr.select('strong.td_score')[0].text.split(':')[1]
                                stadium, bc = tds[5].text.strip(), tds[4].text.strip()
                            else:
                                break
                        else:
                            hour = tds[0].text.strip()
                            playedat, form2 = f'{yy}-{mo}-{day} {hour}:00', '%Y-%m-%d %H:%M:%S'
                            if len(tds) == 3:
                                break
                            elif tr.select('td.add_state'):
                                dt_playedat= dt.datetime.strptime(playedat, form2)
                                away, asc = tr.select('span.team_lft')[0].text, tr.select('td>strong>em.vs')[0].text
                                home, hsc = tr.select('span.team_rgt')[0].text, tr.select('span.suspended')[0].text
                                stadium, bc = tds[3].text.strip(), tds[2].text.strip()
                            elif tr.find_all('img')[2]['alt'] == "경기결과":
                                dt_playedat= dt.datetime.strptime(playedat, form2)
                                away, asc= tr.select('span.team_lft')[0].text, tr.select('strong.td_score')[0].text.split(':')[0]
                                home, hsc = tr.select('span.team_rgt')[0].text, tr.select('strong.td_score')[0].text.split(':')[1]
                                stadium, bc = tds[4].text.strip(), tds[3].text.strip()
                            else:
                                break
                                                    
                        result_lst.append([dt_playedat, away, asc, home, hsc, stadium, bc])
        return result_lst
    
    def crawl_ytrecord(): #하루 전 경기들의 승리투수, 패전투수, 결승타자 기록들을 크롤링해주는 함수
        now = dt.datetime.now()
        yester = now  - timedelta(days=1)
        yymd, yy, yd, ym = yester.strftime('%Y%m%d'), yester.strftime('%Y'), yester.strftime('%d'), yester.strftime('%m')
        result_lst = []
        url=f'https://sports.news.naver.com/kbaseball/schedule/index?date={yymd}&month={ym}&year={yy}&teamCode='
        response = requests.get(url); soup = bs(response.text, 'lxml'); divs = soup.select('#calendarWrap>div')
        for div in divs:
            mo=format(int(div.select('td')[0].text.strip().replace('.',' ').split(' ')[0]), '02')
            day=format(int(div.select('td')[0].text.strip().replace('.',' ').split(' ')[1]), '02')
            playeddate, yesterdate, form=f'{yy}-{mo}-{day}', f'{yy}-{ym}-{yd}', '%Y-%m-%d'
            dt_playeddate, dt_yesterdate = dt.datetime.strptime(playeddate, form), dt.datetime.strptime(yesterdate, form)
            if dt_playeddate == dt_yesterdate:
                trs = div.select('tr')
                for tr in trs:
                    tds = tr.select('td')
                    if len(tds) == 3:
                            break
                    else:
                        if tr == trs[0]:
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
                                    record_rp = requests.get(record_url); record = json.loads(record_rp.text)
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
                                    record_rp = requests.get(record_url); record = json.loads(record_rp.text)
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
            SortedID_list = sorted(ID_list, key=lambda x: x[0])
            wp_ordered_lst=[] ; lp_ordered_lst=[]; fb_ordered_lst=[]
            for i in range(len(result_lst)):
                wp_ordered_lst.append(result_lst[i][0])
                lp_ordered_lst.append(result_lst[i][1])
                fb_ordered_lst.append(result_lst[i][2])
            nwp_ordered_lst=[] ; nlp_ordered_lst=[]; nfb_ordered_lst=[]
            for wo in range(len(wp_ordered_lst)):
                tem_lst_1=[SortedID_list[wo]+wp_ordered_lst[wo]]
                nwp_ordered_lst.append(tem_lst_1)
            for lo in range(len(lp_ordered_lst)):
                tem_lst_2=[SortedID_list[lo]+lp_ordered_lst[lo]]
                nlp_ordered_lst.append(tem_lst_2)
            for fo in range(len(fb_ordered_lst)):
                tem_lst_3=[SortedID_list[fo]+fb_ordered_lst[fo]]
                nfb_ordered_lst.append(tem_lst_3)
            nwp_lst = [x for sublist in nwp_ordered_lst for x in sublist]
            nlp_lst = [x for sublist in nlp_ordered_lst for x in sublist]
            nfb_lst = [x for sublist in nfb_ordered_lst for x in sublist]
        return nwp_lst, nlp_lst, nfb_lst