# VDI-Flask
 

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/f2130696-8c7d-4f30-b7b5-c3895d9e7326)

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/f8a4156e-48e0-4310-b01e-f636da2e79cd)

<hr>

<h1>web</h1>

Aadmin login

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/60616054-4cf8-42cb-b694-a509ca67f6c2)

Useradd

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/6fdba3e1-0672-48cd-b619-0c5d17b0c142)


Userlist

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/3b8edc06-095f-4ef2-b53c-43bbcad1b92b)

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/4bb08acb-79e2-4deb-aac2-3d52b52510f7)

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/d79d7711-0259-4065-b8a6-15f6af9f78fe)



<h1>2024/6/20</h1>
<h2>因應 GOOGLE 關閉了MFA的API功能 不能透過domain方式取得QR-code</h2>


[google聲明](https://developers.google.com/chart/image?hl=zh-tw) 

[google MFA 404](https://invisioncommunity.com/forums/topic/477789-google-authenticator-has-stoped-working-as-mfa/)


這邊提供另外一種方式 [Quickchat](https://quickchart.io/documentation/qr-codes/) 

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/91527f53-bd88-4e43-8c2b-9bcc64d12243)


透過 它的QR-code API 讓程式碼取得要的Text 帶給API 寄信給使用者 即可達成同樣效果!!!


code:
```
Qr=line[1].split('chl=')
Qr='https://quickchart.io/qrtext='+Qr[1]+'&size=600'message = MIMEText( line[0]+Qr+"\n"+line[2]+line[3]+line[4]+line[5] , 'plain', 'utf-8')
```

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/21eac614-a4fc-4b85-b916-9345acd383b5)

![image](https://github.com/NickLi1014/VDI-Flask/assets/73222054/296d37cd-f794-44fc-ab5a-68b1f378d15b)


一天又平安的過去了...感謝google大神

