from bb_modules.first_baseball_crawler import twodaysagoCrawler as tc
from bb_modules.update_baseball_crawler import yesterCrawler as yc
from bb_modules.baseball_db import db
import datetime as dt
from datetime import timedelta
import time

if __name__ == "__main__":
    now = dt.datetime.now()
    def bb_twodaysago():
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

    def bb_yester():
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
        bb_twodaysago() and bb_yester()
        print(f'업데이트 시간:{now}')
        time.sleep(1800)