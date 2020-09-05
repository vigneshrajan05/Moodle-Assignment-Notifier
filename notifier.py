import win10toast as wt
import requests as r
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText




def send_mail(to_email, from_email, subject, msg1, password):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email 
    msg.set_content(msg1)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    print('Logged in!')
    server.send_message(msg)
    print('Email sent!')
    server.quit()


#user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"}

# while resizing in headless mode , the bot might not be able to find the desired element,
# so we specify the resize as the actual window size expilicitly!
CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  

# To run chrome in the background!
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
#chrome_options.binary_location = CHROME_PATH
#driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)  
driver = webdriver.Chrome(options=chrome_options)  
#driver = webdriver.Chrome()
driver.get('http://moodle.psgtech.ac.in/login/index.php')


# locating username and automating username entry
username = driver.find_element_by_xpath('//*[@id="username"]')
username.send_keys('') # Enter your Moodle Username

# locating password and automating password entry
password = driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys('') # Enter your Moodle Password

# Login button click
login = driver.find_element_by_xpath('//*[@id="loginbtn"]')
login.send_keys(Keys.ENTER)

courses = driver.find_element_by_xpath('//*[@id="course-807"]')

# Extracting name of the user
username = driver.find_element_by_css_selector('.page-header-headings')
uname = username.text
pattern = re.compile(r'^STUDENT-\d{2}[a-zA-Z]\d{3}\s([a-zA-Z\s]+)$')
match = pattern.match(uname)
user = match.group(1)

# Returns only the body part of the document including html tags
# Use body.innerHTML to exclude tags
html = driver.execute_script("return document.body.outerHTML;")
soup = bs(html, 'html.parser')
courseList = soup.findAll("div", {"class": "box coursebox"})

s = ''
body = ''
for i in courseList:
        s += str(i.find("div", {"class":"collapsibleregioninner"}))
        s += '\n'
        body += str(i)


pid_list = []
title_list = []
course_id = []
pendingCount = 0   #stores count of Pending Assignments!

# Extracting Course id's with pending assignments using regex
pattern = re.compile(r'[a-zA-Z_]+([\d]{3})[a-zA-Z_]+')
match = pattern.finditer(s)

for m in match:
    pid_list.append(m.group(1))
    pendingCount += 1


# Extracting all Course titles using regex
pattern = re.compile(r'title="([A-Z\s]+)"')
match1 = pattern.finditer(body)

for m in match1:
    title_list.append(m.group(1))
title_list.append('PROBABILITY STATISTICS AND RANDOM PROCESS')

# Extracting all Course id's using regex
pattern = re.compile(r'id="course-(\d{3})"')
matchId = pattern.finditer(body)

for m in matchId:
    course_id.append(m.group(1))
    
# Making Course id and title as a key-value pair
info = dict()
for i in range(len(course_id)):
    info[course_id[i]] = title_list[i]

arg1 = ''
for i in range(len(pid_list)):
    arg1 += str(i+1)+'.'
    arg1 += str(info[pid_list[i]])
    arg1 += '<br>'


arg = ''
arg = str(pendingCount)+' Pending Assignment(s)'



# Setting mail details
sender = # Mail id through which notification will be sent!
rec = # Mail id to which notification will be sent(receiver)!
password = # Sender Mail id's Password ('Turn on' less secure apps and 'Turn off' Two Step Verification)
subject = 'Assignment awaits :('
msg = ''


if len(pid_list) != 0:
    toast = wt.ToastNotifier()  # Toast Notifier Object for sending Desktop Push Notification
    toast.show_toast(arg, 'Assignments in '+str(arg1), duration=8, icon_path = 'imgs/stress1.ico')
    msg = '''<p>
Hey '''+str(user)+''',
You have <b>'''+str(arg)+ '''</b> in the following subject(s)<br> 
'''+str(arg1)+'''.<br>To know more details login on to
<a href="http://moodle.psgtech.ac.in/login/index.php">
moodle</a></p>'''

    
    message = MIMEText(msg, "html")  
    send_mail(rec, sender, subject, message, password)
