###  :baseball:2023시즌 KBO프로야구 경기결과 업데이트 프로젝트:baseball:

## 프로젝트 소개
스포츠 중계방송사별로 매일 프로야구 경기가 끝나자마자 모든 경기의 승리투수, 패전투수, 
결승타를 친 수훈선수에 대한 기록을 리뷰를 해주는 프로그램이 있는 것처럼 
모든 경기 결과와 경기에 대한 승리투수, 패전투수, 결승타자 기록을 DB에 업데이트하는 코드를 구현하고자 했다.

## 사용 url
```
f"https://sports.news.naver.com/kbaseball/schedule/index?date={}&month={}&year={}&teamCode="

```
이외에도 fetch를 통해 json파일을 읽어와서 경기기록을 크롤링했다.

## 기술스택
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
<br>
<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
<br>
<img src="https://img.shields.io/badge/mariaDB-003545?style=for-the-badge&logo=mariaDB&logoColor=white">
<br>
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> 

## 구현 로직
# MySQL(MariaDB)
1. ERD cloud를 통해 데이터베이스위의 경기결과, 승리투수, 패전투수, 결승타자 정보를 기록하는
테이블에 들어갈 칼럼들을 구성하고 테이블의 관계를 설정한다.
2. MariaDB에 BASEBALL데이터베이스를 만들고 사용한다.
3. 2번의 데이터베이스 위에 ERD cloud에서 구성한 테이블을 만든다.
# 파이썬
1. 데이터베이스에 있는 경기결과 테이블에 이틀전 경기기록이 있으면 패스하고,
없으면 이틀전까지의 경기결과와 승리투수, 패전투수, 결승타자의 기록을 
크롤링하여 각 정보에 해당하는 데이터 베이스 테이블에 넣는다.
2. 1번과 같은 원리로 어제 경기기록을 확인하고 기록이 있으면 패스하고,
없으면 어제 경기결과와 승리투수, 패전투수, 결승타자의 기록을 
크롤링하여 각 정보에 해당하는 데이터 베이스 테이블에 넣는다.
3. 스케쥴 모듈을 활용하여 매일 오전 1시에 1번과 2번을 실행하는 함수를 만들고,
오전 1시 2분에 코드실행종료하는 함수를 만든다.
4. while문을 이용해 위 코드가 계속 실행되도록 한다.
