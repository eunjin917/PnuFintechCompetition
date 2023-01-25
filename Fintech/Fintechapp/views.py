from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse # 카카오톡과 연동하기 위해선 JsonResponse로 출력
from django.views.decorators.csrf import csrf_exempt # 보안 이슈를 피하기 위한 csrf_exempt decorator 필요
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import json
import csv
import tensorflow as tf
import pandas as pd
import numpy as np
from pickle import load
from sklearn.metrics import mean_absolute_error 
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import quote
import requests
from datetime import date, timedelta
import re

from .models import Price, Predict, KakaoUser

datasize = 2  # 품목의 수 (풋고추0, 새송이1)

market_list = ['서울도매시장']

company_list = ['중앙청과', '서울청과', '동화청과', '농협가락(공)', '한국청과']

good_list = [{
    "PRDLST_NM": "풋고추",
    "SPCIES_NM": "청양",
    "GRAD": "특",
    "GRAD_NO": "11",
    }, {
    "PRDLST_NM": "새송이",
    "SPCIES_NM": "새송이(일반)",
    "GRAD": "특",
    "GRAD_NO": "11",
    },
]





### 메인 페이지 (중앙청과, 풋고추가 대표로)
def index(request):
    
    # (중앙청과, 풋고추) 정보 가져오기
    price_info = Price.objects.filter(CPR_NM=company_list[0],
                                      PRDLST_NM=good_list[0]["PRDLST_NM"], SPCIES_NM=good_list[0]["SPCIES_NM"], GRAD=good_list[0]["GRAD"])
    # 8일 간 법인별 정보 가져오기
    company_info = []    # [[0법인8일], ..., [4법인8일]]
    day8_info = []
    for company_no in range(5):    # 법인별로 풋고추 정보 가져오기
        prices = Price.objects.filter(CPR_NM=company_list[company_no],
                                      PRDLST_NM=good_list[0]["PRDLST_NM"], SPCIES_NM=good_list[0]["SPCIES_NM"], GRAD=good_list[0]["GRAD"])
        count = prices.count()
        for i in range(7, -1, -1):    # 7일전 ~ 0일전 총 8일 데이터
            day8_info.append(prices[count-1-i])
        company_info.append(day8_info)
        day8_info = []
    
    # 다음날 (풋고추) 예측값 가져오기
    next_predict = Predict.objects.last().price0
    
    # 모든 법인의 풋고추 정보 가져오기
    all_info = Price.objects.filter(PRDLST_NM=good_list[0]["PRDLST_NM"], SPCIES_NM=good_list[0]["SPCIES_NM"], GRAD=good_list[0]["GRAD"])
    y = [item.PRI_AVE for item in all_info]                # 실제 평균값 리스트
    pred = [item.PRI_PRED for item in all_info]            # 예측값 리스트
    mean_error = round(mean_absolute_error(y, pred), 2)    # 이상치 판별 기준값 설정
    
    # (중앙청과-풋고추)의 가장 최신 정보 가져오기
    price_info = Price.objects.filter(CPR_NM=company_list[0], 
                                      PRDLST_NM=good_list[0]["PRDLST_NM"], SPCIES_NM=good_list[0]["SPCIES_NM"], GRAD=good_list[0]["GRAD"])
    this_info = price_info.last()
    this_error = abs(this_info.PRI_AVE - this_info.PRI_PRED)    # (중앙청과-풋고추)의 예측값과 실제값 편차

    # 이상값 시 (실제값-예측값 편차가 기준 이상)
    is_error = False
    if this_error > mean_error:
        is_error = True
    
    return render(
        request,
        'index.html',
        {
            'price_info': price_info,        # 해당 법인만 있는 정보
            'company_info': company_info,    # 법인 전체가 있는 정보
            'this_info': this_info,          # 마지막으로 업데이트된 날짜의 정보
            'next_predict': next_predict,    # 그 다음에 업데이트될 날짜를 예측
            'mean_error' : mean_error,       # 전체 법인의 전체 기간에 대한 오차 평균
            'this_error': this_error,        # 선택된 법인1개의 오늘에 대한 오차 평균
            'is_error': is_error,            # 이상인지 여부
        }
    )
    

### 법인, 품목별 세부 페이지
def company_good(request, company_pk, good_pk):    #/company_good/c0(중앙청과)/g0(청양고추)
    
    # 해당 (법인-품목)에 대한 정보 가져오기
    price_info = Price.objects.filter(CPR_NM=company_list[company_pk],
                                      PRDLST_NM=good_list[good_pk]["PRDLST_NM"], SPCIES_NM=good_list[good_pk]["SPCIES_NM"], GRAD=good_list[good_pk]["GRAD"])
    # 8일 간 법인별 정보 가져오기
    company_info = []    # [[0법인8일], ..., [4법인8일]]
    day8_info = []
    for company_no in range(5):    # 법인별
        prices = Price.objects.filter(CPR_NM=company_list[company_no],
                                      PRDLST_NM=good_list[good_pk]["PRDLST_NM"], SPCIES_NM=good_list[good_pk]["SPCIES_NM"], GRAD=good_list[good_pk]["GRAD"])
        count = prices.count()
        for i in range(7, -1, -1):    # 7일전 ~ 0일전 총 8개
            day8_info.append(prices[count-1-i])
        company_info.append(day8_info)
        day8_info = []
    
    # 품목(풋고추, 새송이)에 따라 next_predict에 다음날 예측값 가져오기
    if good_pk == 0:
        next_predict = Predict.objects.last().price0
    elif good_pk == 1:
        next_predict = Predict.objects.last().price1
    
    # 5개 법인 전체 정보 가져오기
    all_info = Price.objects.filter(PRDLST_NM=good_list[good_pk]["PRDLST_NM"], SPCIES_NM=good_list[good_pk]["SPCIES_NM"], GRAD=good_list[good_pk]["GRAD"])
    y = [item.PRI_AVE for item in all_info]
    pred = [item.PRI_PRED for item in all_info]
    mean_error = round(mean_absolute_error(y, pred), 2)    # 이상치 판별 기준값 설정
    
    # 해당 법인에 대한 가장 최신의 정보 가져오기
    price_info = Price.objects.filter(CPR_NM=company_list[company_pk], 
                                      PRDLST_NM=good_list[good_pk]["PRDLST_NM"], SPCIES_NM=good_list[good_pk]["SPCIES_NM"], GRAD=good_list[good_pk]["GRAD"])
    this_info = price_info.last()
    this_error = abs(this_info.PRI_AVE - this_info.PRI_PRED)    # (법인-품목)의 예측값과 실제값 편차

    # 이상값 시 (실제값-예측값 편차가 기준 이상)
    is_error = False
    if this_error > mean_error:
        is_error = True
        
    print(is_error)
    
    return render(
        request,
        'index.html',
        {
            'price_info': price_info,        # 해당 법인만 있는 정보
            'company_info': company_info,    # 법인 전체가 있는 정보
            'this_info': this_info,          # 마지막으로 업데이트된 날짜의 정보
            'next_predict': next_predict,    # 그 다음에 업데이트될 날짜를 예측
            'mean_error' : mean_error,       # 전체 법인의 전체 기간에 대한 오차 평균
            'this_error': this_error,        # 선택된 법인1개의 오늘에 대한 오차 평균
            'is_error': is_error,            # 이상인지 여부
        }
    )


### AI모델에서 학습된 데이터 가져오기 + DB에 저장
def setting_data(request): 
    # csv 파일에서 가져온 데이터를 DB Price에 정보 저장
    for i in range(datasize):
        with open("./Fintechapp/csvdata/update_data{}.csv".format(i), 'r', encoding="UTF-8") as f:
            dr = csv.DictReader(f)
            s = pd.DataFrame(dr)
        ss = []
        for j in range(len(s)):
            st = (s["DELNG_DE"][j], s["MRKT_NM"][j], s["CPR_NM"][j], s["PRDLST_NM"][j],s["SPCIES_NM"][j],
                  s["GRAD"][j], s["weight"][j], s["PRI_MAX"][j], s["PRI_MIN"][j], s["PRI_AVE"][j], s["PRI_PRED"][j])
            ss.append(st)
            Price.objects.create(DELNG_DE=ss[j][0], MRKT_NM=ss[j][1], CPR_NM=ss[j][2], PRDLST_NM=ss[j][3],
                                 SPCIES_NM=ss[j][4], GRAD=ss[j][5], weight=ss[j][6], PRI_MAX=ss[j][7], PRI_MIN=ss[j][8],
                                 PRI_AVE=ss[j][9], PRI_PRED=ss[j][10])
    
    # DB에 Predict 저장
    data = []
    x_shift_data = []  # 평균가가 shift된 입력 데이터 (input)
    x_input_data = []
    model = []
    x_sc = []
    y_sc = []
    good = []
    company = []
    ori_data = []
    for i in range(datasize):
        ori_data.append(pd.read_csv('./Fintechapp/csvdata/update_data{}.csv'.format(i)))
        model.append(tf.keras.models.load_model('./Fintechapp/ai_model/LSTM-model{}_adam.h5'.format(i)))
        x_sc.append(load(open('./Fintechapp/ai_model/x_sc{}.pkl'.format(i), 'rb')))
        y_sc.append(load(open('./Fintechapp/ai_model/y_sc{}.pkl'.format(i), 'rb')))
        data.append(ori_data[i].sort_values(by=['DELNG_DE'])[['DELNG_DE', 'PRI_AVE']])

    for i in range(datasize):
        x_shift_data.append(ori_data[i].groupby('DELNG_DE', as_index=False)['PRI_AVE'].mean())  # 날짜별 평균값 리스트
        x_shift_data[i]['PRI_AVE'] = round(x_shift_data[i]['PRI_AVE'], 2)

    for i in range(datasize):
        temp = x_shift_data[i][-10:]['PRI_AVE'].tolist()
        temp.reverse()
        x_input_data.append(np.array(temp).reshape(1, -1))

    # 다음날 예측값 가져오기 + DB에 저장
    next_predict = []  # 내일 예측가(법인전체) : 청양고추, 새송이
    for i in range(datasize):
        x_data_sc = x_sc[i].transform(x_input_data[i])
        next_predict.append(y_sc[i].inverse_transform(model[i].predict(x_data_sc))[0][0])

    Predict.objects.create(price0=next_predict[0].item(), price1=next_predict[1].item())     

    
    return render(request,'index.html')


### 스케쥴러 등록
def update(request):
    sched = BackgroundScheduler(timezone="Asia/Seoul")
    
    # 데이터 업데이트 스케쥴러
    sched.add_job(job, 'cron', second="0", id="job")
    
    # 알람 보내기 스케쥴러
    sched.add_job(alarm_bell, 'cron', second="0", id="alarm_bell")    # 매일 13시마다 실행. test는 매분마다
    # sched.add_job(alarm_bell, 'cron', hour="13", id="alarm_bell")    
    
    sched.start()
    
    return render(request,'finish.html')
    
    
### 데이터 업데이트 - 1분에 1번 실행
def job():
    print("job 실행!")
    updateCheck = 0
    update_data = []
    ori_data = []
    
    # 법인-품목 별로 오늘 데이터 있는지 API 확인
    for i in range(datasize):  # 각 품목(풋고추, 새송이)마다
        ori_data.append(pd.read_csv('./Fintechapp/csvdata/update_data{}.csv'.format(i)))    #원래 있던 csv의 데이터 
        update_data.append(ori_data[i])                                                     #업데이트될 리스트
        
        for j in range(len(company_list)):    # 각 법인마다
            marketname = market_list[0]             # 도매시장명
            coname_c = company_list[j]              # 법인명
            mclassname = good_list[i]['PRDLST_NM']  # 품목
            sclassname = good_list[i]['SPCIES_NM']  # 품목
            gradename = good_list[i]['GRAD_NO']     # 등급 번호 (특 - 11 ,상 - 12 , 보통 13)
            grade = "특"
            
            #요청할 url에 넣을 변수들
            marketname_info = "&PBLMNG_WHSAL_MRKT_NM=" + marketname
            coname_info_c = "&CPR_NM=" + coname_c
            mclassname_info = "&PRDLST_NM=" + mclassname
            sclassname_info = "&SPCIES_NM=" + sclassname
            gradename_info = "&GRAD_CD=" + gradename

            df_data = []
            today = date.today().strftime("%Y%m%d")
            url = "http://211.237.50.150:7080/openapi/d60c7fa3f4501f62dbd2ca000625a2d12b764928e9a2cd513dfacb4d628991c5/json/Grid_20180118000000000581_1/1/1000?"
            date_info = "&DELNG_DE=" + today      # 오늘 날짜
            url = url + date_info + mclassname_info + sclassname_info + marketname_info + coname_info_c + gradename_info
            url_encoded_n = quote(url, safe=':/=?&')
            response = requests.get(url_encoded_n)
            contents = response.text
            data = json.loads(contents)
            stat = data['Grid_20180118000000000581_1']['row']
            if stat == []:          # 오늘 데이터가 업데이트 되지 않아 데이터가 없는 경우
                print("no data")   
                continue
            else:                   # 오늘 데이터가 업데이트 돼 df_data에 추가
                df_data.append(stat)   

                
            df = pd.DataFrame()
            for k in range(len(df_data)):
                df_data[k] = pd.DataFrame(df_data[k])
                df = pd.concat([df, df_data[k]], ignore_index=True)
            data = df[['DELNG_DE', 'PBLMNG_WHSAL_MRKT_NM', 'CPR_NM', 'PRDLST_NM', 'SPCIES_NM', 'GRAD', 'DELNGBUNDLE_QY','PRICE']]
            data['DELNGBUNDLE_QY'] = data['DELNGBUNDLE_QY'].astype('float')
            data['PRICE'] = round(data['PRICE'] / data['DELNGBUNDLE_QY'], 2)
            data['DELNG_DE'] = pd.to_datetime(data['DELNG_DE'], format='%Y%m%d')
            data['DELNGBUNDLE_QY'] = 1
            new_data = data
            new_data['PRI_MAX'] = data.groupby('DELNG_DE', as_index=False)['PRICE'].transform('max')
            new_data['PRI_MIN'] = data.groupby('DELNG_DE', as_index=False)['PRICE'].transform('min')
            new_data['PRI_AVE'] = data.groupby('DELNG_DE', as_index=False)['PRICE'].transform('mean')
            new_data = data.groupby('DELNG_DE', as_index=False).mean()  # 날짜별로 바꾸기
            new_data['MRKT_NM'] = marketname
            new_data['CPR_NM'] = coname_c
            new_data['PRDLST_NM'] = mclassname
            new_data['SPCIES_NM'] = sclassname
            new_data['GRAD'] = grade
            new_data['weight'] = "1KG"
            new_data['DELNG_DE'] = (date.today()).isoformat()
            
            if i == 0:
                next_predict = Predict.objects.last().price0
            elif i == 1:
                next_predict = Predict.objects.last().price1
            
            new_data = new_data[['DELNG_DE', 'MRKT_NM', 'CPR_NM', 'PRDLST_NM', 'SPCIES_NM', 'GRAD', 'weight', 'PRI_MAX', 'PRI_MIN',
                 'PRI_AVE', 'PRI_PRED']]
            DB_input_data = new_data.values.tolist()[0]
            
            # DB에 오늘에 해당하는 법인-품목이 하나도 저장 안 됐다면 : 더 진행 못하도록 설정
            if not Price.objects.filter(CPR_NM=company_list[j],PRDLST_NM=good_list[i]["PRDLST_NM"],DELNG_DE=(date.today()).isoformat()).count() :
                Price.objects.create(DELNG_DE=DB_input_data[0], MRKT_NM=DB_input_data[1], CPR_NM=DB_input_data[2], PRDLST_NM=DB_input_data[3],
                                     SPCIES_NM=DB_input_data[4], GRAD=DB_input_data[5], weight=DB_input_data[6], PRI_MAX=DB_input_data[7], PRI_MIN=DB_input_data[8],
                                     PRI_AVE=DB_input_data[9], PRI_PRED=DB_input_data[10])    
                update_data[i] = pd.concat([update_data[i], new_data], ignore_index=True)
                updateCheck = 1

        # DB에 저장된 법인-품목이 있으면, 중복된 데이터는 지우기
        if updateCheck:
            update_data[i] = update_data[i].drop(['Unnamed: 0'], axis=1)
            update_data[i] = update_data[i].drop_duplicates(['DELNG_DE', 'MRKT_NM', 'CPR_NM', 'PRDLST_NM', 'SPCIES_NM'])
            update_data[i].to_csv('./Fintechapp/csvdata/update_data{}.csv'.format(i))
    
    # DB에 저장된 법인-품목이 있으면, # DB에 Predict 저장
    if updateCheck:
        data = []
        x_shift_data = []  # 평균가가 shift된 입력 데이터 (input)
        x_input_data = []
        model = []
        x_sc = []
        y_sc = []
        good = []
        company = []
        for i in range(datasize):
            ori_data.append(pd.read_csv('./Fintechapp/csvdata/update_data{}.csv'.format(i)))
            model.append(tf.keras.models.load_model('./Fintechapp/ai_model/LSTM-model{}_adam.h5'.format(i)))
            x_sc.append(load(open('./Fintechapp/ai_model/x_sc{}.pkl'.format(i), 'rb')))
            y_sc.append(load(open('./Fintechapp/ai_model/y_sc{}.pkl'.format(i), 'rb')))
            data.append(ori_data[i].sort_values(by=['DELNG_DE'])[['DELNG_DE', 'PRI_AVE']])

        for i in range(datasize):
            x_shift_data.append(ori_data[i].groupby('DELNG_DE', as_index=False)['PRI_AVE'].mean())  # 날짜별 평균값 리스트
            x_shift_data[i]['PRI_AVE'] = round(x_shift_data[i]['PRI_AVE'], 2)

        for i in range(datasize):
            temp = x_shift_data[i][-10:]['PRI_AVE'].tolist()
            temp.reverse()
            x_input_data.append(np.array(temp).reshape(1, -1))

        # 다음날 예측값 가져오기 + DB에 저장
        next_predict = []  # 내일 예측가(법인전체) : 청양고추, 새송이
        for i in range(datasize):
            x_data_sc = x_sc[i].transform(x_input_data[i])
            next_predict.append(y_sc[i].inverse_transform(model[i].predict(x_data_sc))[0][0])

        Predict.objects.create(price0=next_predict[0].item(), price1=next_predict[1].item())
    

### 카카오봇에서 user가 원하는 (법인-품목) 알람 설정
@csrf_exempt
def alarm_setting(request):
    if request.method == "POST":
        # [봇시스템 -> 웹서버] 받은 json을 decode 후, 파이썬 객체로 변환
        answer = ((request.body).decode('utf-8'))
        return_json_str = json.loads(answer)
        
        i = return_json_str['action']['clientExtra']['company']                     # user가 선택한 법인
        j = return_json_str['action']['clientExtra']['class']                       # user가 선택한 품목
        user_email = return_json_str['action']['detailParams']['email']['value']    # user의 email
        
        # 이메일 유효성 검사
        email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        result = email.match(user_email)
        
        text = ""
        if result is None:
            text = "올바른 이메일이 아닙니다. 처음으로 돌아갑니다."
        else:        # 해당 이메일을 가진 user에서 알림받을 (법인, 품목) 체크
            text = "알림 설정 완료!"
            try:    # 기존 회원
                thisuser = KakaoUser.objects.get(user_email = user_email)
                fn_checkbox(thisuser, int(i), int(j))
            except:    # 신규 회원
                thisuser = KakaoUser.objects.create(user_email = user_email)
                fn_checkbox(thisuser, int(i), int(j))
        
        # [웹서버 -> 봇서버] 보낼 json
        context = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": text
                        }
                    }
                ]
            }
        }
    
        return JsonResponse(context)
    return render(request, 'finish.html')
    
    
### 이상 발생 시 알림 메일 발송 기능
def alarm_bell():
    print("alarm 실행!")
    
    for i, good in enumerate(good_list):    # 각 품목 별로
        # 5개 법인 전체 정보 가져오기
        all_info = Price.objects.filter(PRDLST_NM=good["PRDLST_NM"], SPCIES_NM=good["SPCIES_NM"], GRAD=good["GRAD"])
        
        y = [item.PRI_AVE for item in all_info]                # 실제 평균값 리스트
        pred = [item.PRI_PRED for item in all_info]            # 예측값 리스트
        mean_error = round(mean_absolute_error(y, pred), 2)    # 전체 법인의 전체 기간
        
        # 해당 법인에 대한 가장 최신의 정보 가져오기
        for j, company in enumerate(company_list):
            price_info = Price.objects.filter(CPR_NM=company, PRDLST_NM=good["PRDLST_NM"], SPCIES_NM=good["SPCIES_NM"], GRAD=good["GRAD"])
            this_info = price_info.last()
            this_error = abs(this_info.PRI_AVE - this_info.PRI_PRED)    # (법인-품목)의 예측값과 실제값 편차
            
            
            # 이상값 시 (실제값-예측값 편차가 기준 이상일 때)
            if this_error > mean_error :
                # 알림설정한 사용자가 있으면 메일 전송
                users = fn_search(i, j)
                if users is not None:
                    subject = this_info.DELNG_DE + " " + this_info.CPR_NM + " " + this_info.PRDLST_NM + "-" + this_info.SPCIES_NM + " " + this_info.GRAD + " 이상 발생 알림"
                    message = render_to_string('mail.html', {
                        'this_info': this_info,    # 마지막으로 업데이트된 날짜의 정보
                        'company_no': i,
                        'class_no': j,
                        'this_error': this_error,
                        'mean_error': mean_error,
                    })
                    email = EmailMessage(subject, message, to=[user.user_email for user in users])
                    email.content_subtype = "html"
                    email.send()
                    print(company, good, "전송 완료")

    
    
# user마다 알림 설정한 (법인-품목)에 대해 
# KakaoUser DB에 체크박스 설정하기
# fn_checkbox(user, 0, 0): 해당 user의 (중앙청과-풋고추) 알림 check(true)
def fn_checkbox(thisuser, i, j):
    if i==0 and j==0:
        thisuser.alarm_0_0 = True
    elif i==1 and j==0:
        thisuser.alarm_1_0 = True
    elif i==2 and j==0:
        thisuser.alarm_2_0 = True
    elif i==3 and j==0:
        thisuser.alarm_3_0 = True
    elif i==4 and j==0:
        thisuser.alarm_4_0 = True
    
    elif i==0 and j==1:
        thisuser.alarm_0_1 = True
    elif i==1 and j==1:
        thisuser.alarm_1_1 = True
    elif i==2 and j==1:
        thisuser.alarm_2_1 = True
    elif i==3 and j==1:
        thisuser.alarm_3_1 = True
    elif i==4 and j==1:
        thisuser.alarm_4_1 = True
    thisuser.save()
        

# 특정 (법인-품목) 알림 설정한 user 찾기
# fn_search(0, 0) : (중앙청과-풋고추) 알림 설정한 user들 return
def fn_search(i, j):
    if i==0 and j==0:
        return KakaoUser.objects.filter(alarm_0_0=True)
    elif i==1 and j==0:
        return KakaoUser.objects.filter(alarm_1_0=True)
    elif i==2 and j==0:
        return KakaoUser.objects.filter(alarm_2_0=True)
    elif i==3 and j==0:
        return KakaoUser.objects.filter(alarm_3_0=True)
    elif i==4 and j==0:
        return KakaoUser.objects.filter(alarm_4_0=True)
    
    elif i==0 and j==1:
        return KakaoUser.objects.filter(alarm_0_1=True)
    elif i==1 and j==1:
        return KakaoUser.objects.filter(alarm_1_1=True)
    elif i==2 and j==1:
        return KakaoUser.objects.filter(alarm_2_1=True)
    elif i==3 and j==1:
        return KakaoUser.objects.filter(alarm_3_1=True)
    elif i==4 and j==1:
        return KakaoUser.objects.filter(alarm_4_1=True)