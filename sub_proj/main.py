from bb_modules.first_baseball_crawler import twodaysagoCrawler as tc
from bb_modules.update_baseball_crawler import yesterCrawler as yc
from bb_modules.baseball_db import db
import datetime as dt
from datetime import timedelta
import time

now = dt.datetime.now()
if __name__ == "__main__": #main.py를 실행할 때 작동하는 코드들
    def bb_twodaysago(): #이틀전까지 쌓인 경기에 대한 정보들을 모두 데이터베이스에 저장하는 함수(최초 1회 실행)
        tdsago = now  - timedelta(days=2)
        tda=tdsago.strftime('%Y-%m-%d')
        count = db.select_count(tda)
        if count != 0:
            pass
        else:
            cg = tc.crawl_game()
            cg_lst = [tuple(x) for x in cg]
            db.insert_many('TB_game', ['PlayedAt', 'AwayTeam', 'AwayScore', 'HomeTeam', 'HomeScore', 'Stadium', 'Broadcast'], cg_lst)   
            crw, crl, crf=tc.crawl_record()
            db.insert_many('TB_winpitcher', ['GameID', 'Name', 'Inning', 'Hit', 'BBHP', 'StrikeOut', 'Lose_Run', 'PitchingNumber', 'Era'], crw)
            db.insert_many('TB_losepitcher', ['GameID', 'Name', 'Inning', 'Hit', 'BBHP', 'StrikeOut', 'Lose_Run', 'PitchingNumber', 'Era'], crl)
            db.insert_many('TB_batter', ['GameID', 'Name', 'AtBats', 'Hit_Homerun', 'BB', 'StrikeOut', 'RBI', 'Run', 'BA'], crf)
        return

    def bb_yester(): #하루 전 경기에 대한 정보들을 모두 데이터베이스에 저장하는 함수(매일 업데이트 됨)
        yester = now  - timedelta(days=1)
        yt=yester.strftime('%Y-%m-%d')
        count = db.select_count(yt)
        if count != 0:
            pass
        else:
            cyg = yc.crawl_ytgame()
            cyg_lst = [tuple(x) for x in cyg]
            db.insert_many('TB_game', ['PlayedAt', 'AwayTeam', 'AwayScore', 'HomeTeam', 'HomeScore', 'Stadium', 'Broadcast'], cyg_lst)
            ncrw, ncrl, ncrf=yc.crawl_ytrecord()
            db.insert_many('TB_winpitcher', ['GameID', 'Name', 'Inning', 'Hit', 'BBHP', 'StrikeOut', 'Lose_Run', 'PitchingNumber', 'Era'], ncrw)
            db.insert_many('TB_losepitcher', ['GameID', 'Name', 'Inning', 'Hit', 'BBHP', 'StrikeOut', 'Lose_Run', 'PitchingNumber', 'Era'], ncrl)
            db.insert_many('TB_batter', ['GameID', 'Name', 'AtBats', 'Hit_Homerun', 'BB', 'StrikeOut', 'RBI', 'Run', 'BA'], ncrf)
        return
               
    while True:
        cur_time = time.localtime() #현재시간
        cur_time_udt = time.strftime('%c', cur_time) # 현재시간을 '요일 월 일 시:분:초 년도'의 형태로 변환
        if cur_time.tm_min == 0: #현재시각이 정시면 실행
            bb_twodaysago() and bb_yester() #위에서 정의한 코드 실행
            print(f'업데이트 시간:{cur_time_udt}') #변환된 시간으로 업데이트 시간 출력
        time.sleep(60)  # 1분마다 체크
