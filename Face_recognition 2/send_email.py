#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import smtplib
import email
import smtplib  
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# In[ ]:





# In[ ]:


#pip install secure-smtplib


# In[ ]:





# In[3]:




def sendeMail(data):
    fromaddr = "smartbus446@gmail.com" # or your email id
    toaddr = "gauravbarua008@gmail.com" #or your email id
    mail = MIMEMultipart()
    mail['From'] = fromaddr
    mail['To'] = toaddr
    mail['Subject'] = "IMPORTANT!"
    body = "Unauthorized Access Detected!! Unknown Person Found!! Sending Live Images!"
    mail.attach(MIMEText(body, 'plain'))
    print (data)
    dat='%s'%data
    print (dat)
    attachment = open(data, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "esovguubqyjkedmy")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
def sendeMail_txt(data):
    fromaddr = "from@gmail.com" # or your email id
    toaddr = "to@gmail.com" #or your email id
    mail = MIMEMultipart()
    mail['From'] = fromaddr
    mail['To'] = toaddr
    mail['Subject'] = "Info text"
    body = data
    mail.attach(MIMEText(body, 'plain'))
    print ('data in email ',data)
    
    
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "pass")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
#sendeMail("recognition/output")


# In[ ]:




