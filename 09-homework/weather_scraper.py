
# coding: utf-8

# In[1]:


import requests
import datetime


# In[2]:


response = requests.get('https://api.darksky.net/forecast/[API KEY GOES HERE]/40.730610,-73.935242')
data = response.json()


# In[3]:


temp = data['currently']['temperature']
summary = data['currently']['summary']
temp_feeling = data['currently']['apparentTemperature']
high_temp = data['daily']['data'][0]['temperatureHigh']
low_temp = data['daily']['data'][0]['temperatureLow']
rain_warning = data['currently']['precipProbability']
rain_warning_text = ""
if rain_warning < .5:
    rain_warning_text = "Risk it! Leave the umbrella at home."
else:
    rain_warning_text = "Better bring an umbrella."


# In[4]:


right_now = datetime.datetime.now()
date_string = right_now.strftime("%B %d, %Y")
subject_line = "8AM Weather forecast: "+date_string


# In[5]:


text = 'Right now it is ' + str(temp) + ' degrees out and ' + summary.lower() +'. Today will be '+ str(temp_feeling) +' with a high of '+ str(high_temp) + ' and a low of '+ str(low_temp) + '. ' + rain_warning_text


# In[6]:


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxefa60e8bb6054ec5999625c2198c091e.mailgun.org/messages",
        auth=("api", "[API KEY GOES HERE]"),
        data={"from": "<mailgun@sandboxefa60e8bb6054ec5999625c2198c091e.mailgun.org>",
              "to": ["MAX.ARVID.ANDERSON@GMAIL.COM"],
              "subject": subject_line,
              "text": text})


# In[7]:


send_simple_message()

