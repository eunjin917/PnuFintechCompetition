# AI를 활용한 법인 별 농산물 이상 경락 가격 알림 플랫폼


핀테크융합전공 사업모델 아이디어 경진 대회에 참가해 이상 경매가격 방지를 위한 핀테크 모델 서비스를 제안하는 'AI를 활용한 법인 별 농산물 이상 경락 가격 알림 플랫폼'을 개발했다.

<img src="https://user-images.githubusercontent.com/95485737/226289340-7b90a3d8-611c-49c5-a48e-9bccd57cacb8.png">


## 프로젝트 소개

농산물 도매시장 내 도매시장법인의 불법 거래로 농가 소득 저하와 농산물 생산자의 정보 불균형문제가
발생한다. 이는 도매법인의 독과점 구조원인으로 작용하기 때문에 생산자의 도매법인 선택과정에서
경쟁구도가 필요하다. 따라서 농산물 생산자에게 합리적인 법인 선택을 위한 충분한 법인 별 경락
정보를 제공하고, 불법 거래 의심 법인을 피하기 위해 이상 경락 가격 모델을 제시한다. 또한 평균
연령이 높은 농산물 생산자를 고려해 이상 경락 가격 발생 시 알림 기능을 추가해 활발한 정보 이용을
촉진한다.

<br>

## 기술 스택

<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">


<br>

## 구현 기능
### 기능 1
#### LSTM 이용 경략 적정 가격 예측 모델 

'전국 도매시장 일별 정산 경락가격 상세정보' 공공 데이터를 이용해 가격 예측 모델을 만들었다. 
최적의 예측 모델을 찾기 위해 simpleRNN, LSTM 모델로 입력층, 유닛수, optimizer로 하이퍼파라미터 튜닝을 하며 최적화된 모델을 찾았다.

<img width='70%' src="https://user-images.githubusercontent.com/95485737/226369472-5f5b60ef-0679-4bfe-b325-4b8cfe15ed15.png">

### 기능 2
#### 선택한 법인-품목에 대한 실제 가격과 예측 가격을 그래프 통해 확인

선택한 법인-품목에 대해 실제 가격(평균가, 최저가, 최고가)과 예측 가격을 비교해 정상 범위를 벗어나면 이상 감지한다. 이를 그래프를 통해 쉽게 비교할 수 있고, 해당 품목에 대해 선 그래프와 막대 그래프로 법인 별로 비교가 가능하다.  

<img width='70%' src="https://user-images.githubusercontent.com/95485737/226368026-26d0590b-d981-4daf-ad56-48c81bad34cb.png">
<img width='70%' src="https://user-images.githubusercontent.com/95485737/226368053-c88965ef-cb38-4e7f-b148-199392b5e6c6.png">
<img width='70%' src="https://user-images.githubusercontent.com/95485737/226368064-792c48ab-d6c7-41a8-ae80-2b75187ab51c.png">

### 기능 3
#### 카카오 봇을 통한 메일 알림 기능

카카오 채널 친구추가로 원하는 품목과 법인을 선택하면, 가격 예측 모델이 이상 가격이 발생했다 판단하면 자동으로 메일로 알림을 준다.

