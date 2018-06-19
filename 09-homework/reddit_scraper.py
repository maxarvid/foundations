
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import time


# Let's scrape the frontpage of Reddit and completely ignore their API.

# In[2]:


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get("https://old.reddit.com", headers=headers)


# In[3]:


soup_doc = BeautifulSoup(response.content, 'html.parser')


# In[4]:


#print(soup_doc.prettify())


# In[5]:


front_page_posts = []
for post in soup_doc.findAll(class_='thing'):
    data = {}
    data['title'] = post.findAll(class_='title')[1].string
    data['url'] = post.findAll(class_='title')[1].get('href')
    data['rank'] = post.find(class_='rank').string
    data['subreddit'] = post.find(class_='subreddit').string
    data['author'] = post.find(class_='author').string
    data['author_url'] = post.find(class_='author').get('href')
    data['upvotes'] = post.findAll(class_='score')[1].get('title')
    data['time'] = post.find('time').get('datetime')
    front_page_posts.append(data)


# In[6]:


front_page_posts


# In[7]:


#Preparation for the email briefing I am sending to myself.
import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%Y-%m-%d-%-I%p")


# In[8]:


#Let's save as a csv.
df = pd.DataFrame(front_page_posts)
df.to_csv('briefing'+date_string+'.csv', index=False)


# In[9]:


#Keeping the subject line and text of the email flexible by assigning variables.
subject_line = "Here is your "+right_now.strftime('%-I%p')+" briefing."
text = "Hey pal, gonna populate this later, let's see if this works first"


# In[10]:


#And attach that csv to an email.
def send_email():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxefa60e8bb6054ec5999625c2198c091e.mailgun.org/messages",
        auth=("api", "[API KEY GOES HERE]"),
        files=[("attachment", open('briefing'+date_string+'.csv'))],
        data={"from": "<mailgun@sandboxefa60e8bb6054ec5999625c2198c091e.mailgun.org>",
              "to": ["MAX.ARVID.ANDERSON@GMAIL.COM"],
              "subject": subject_line,
              "text": text})


# In[11]:


send_email()

