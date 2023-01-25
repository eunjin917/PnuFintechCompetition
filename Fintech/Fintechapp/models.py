from django.db import models

class Price(models.Model):
    DELNG_DE = models.CharField(max_length=30)
    MRKT_NM = models.CharField(max_length=30)
    CPR_NM = models.CharField(max_length=30)
    PRDLST_NM = models.CharField(max_length=30)
    SPCIES_NM = models.CharField(max_length=30)
    GRAD = models.CharField(max_length=30)
    weight = models.CharField(max_length=30)
    PRI_MAX = models.DecimalField(max_digits=10, decimal_places=2)
    PRI_MIN = models.DecimalField(max_digits=10, decimal_places=2)
    PRI_AVE = models.DecimalField(max_digits=10, decimal_places=2)
    PRI_PRED = models.DecimalField(max_digits=10, decimal_places=2)

class Predict(models.Model):
    price0 = models.DecimalField(max_digits=10, decimal_places=2)# 청양고추
    price1 = models.DecimalField(max_digits=10, decimal_places=2)# 새송이

class KakaoUser(models.Model):
    
    user_email = models.EmailField(unique=True)
    
    alarm_0_0 = models.BooleanField(default=False)    # 중앙청과 - 청양고추
    alarm_1_0 = models.BooleanField(default=False)    # 서울청과 - 청양고추
    alarm_2_0 = models.BooleanField(default=False)    # 동화청과 - 청양고추
    alarm_3_0 = models.BooleanField(default=False)    # 농협가락(공) - 청양고추
    alarm_4_0 = models.BooleanField(default=False)    # 한국청과 - 청양고추
    
    alarm_0_1 = models.BooleanField(default=False)    # 중앙청과 - 새송이
    alarm_1_1 = models.BooleanField(default=False)    # 서울청과 - 새송이
    alarm_2_1 = models.BooleanField(default=False)    # 동화청과 - 새송이
    alarm_3_1 = models.BooleanField(default=False)    # 농협가락(공) - 새송이
    alarm_4_1 = models.BooleanField(default=False)    # 한국청과 - 새송이
    
    
    def __str__(self):
        return self.user_email

