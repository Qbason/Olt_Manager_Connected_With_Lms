# Olt Huawei + LMS platform GUI
## PYTHON, BS3, REQUESTS, TELNET, THREAD, TKINTER

## What is it? How does it work? 
Program connects to specified olts via telnet.
Program can do commands like (depends on need):

    enable
    config
    interface gpon 0/x
    display ont info y z
    display ont optical-info y z 
    display ont info y all
    quit
Desc:  
-    x <- board number  
-    y <- port number  
-    z <- ont id  


Mainly communication to olt is used for reading information about onu like:

- Description
- Rx olt
- Tx olt
- Tx onu
- Rx onu

Program makes requests to LMS platform, searching device in system by
"Description". If this action ends successful program reads information about client like:
    
    Name
    Place
    Street
    House number
    Adres ip

This is done using BS4 libray (scraping).

In separate view we can see results in time.



**The most important functionality is:**
1. Finding group of clients by name, place, street
2. In the second view we can click on user to see descrption about him
3. Ordering clients by clicking on columns and finding the best, the worst rx/tx signal
4. Grouping by place and street then calculating the best, the worst, the average rx/tx signal and doing ordering them by user. (by clicking on specific column)

The gui is presented in Polish.

## Config file:
config.py is the place, where we can set our credentials.

## Methods to improve:
- Implementing async or threading with queue
- Finding another library instead of tkinter, which support multiproccessing
- Saving results in database and analyzing signal in long time. 

<img src="https://github.com/Qbason/Olt_Manager_Connected_With_Lms/blob/master/imgs/1.png" width="500"/>


<img src="https://github.com/Qbason/Olt_Manager_Connected_With_Lms/blob/master/imgs/2.png" width="500"/>


<img src="https://github.com/Qbason/Olt_Manager_Connected_With_Lms/blob/master/imgs/3.png" width="500"/>
