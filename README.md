# USTH Calendar Scraping

### What the hell is this
Tired of searching through multiple USTH calendars to find what is your best friend studying in his class? Don't worry! With the ultimate **USTH Calendar Scraping**, you, don't have to worry about clicking through boring stuffs.

### What you need first
In order to use this, you need a *credentials.json* file and **Python3.x**. To obtain *credentials.json*, you could go to this page: <ins>https://developers.google.com/people/quickstart/python</ins>.

![alt text](img/quick-start-python-page.png "Title")

And just do step one to get the *credentials.json* file. Be sure to put that file in the same directory of our Python codes =).

You think it is done? Not so fast! Install these Python libraries first by running:
```
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

If it does not work, please try 

```
    python -m pip
```

instead of 

```
    pip
```

### Usage
**Wanna get it fast?** Here is how you do it!

*Linux*
```
    python get_link_calendar.py && python extract_from_calendar.py > {outputfilename}.csv 
```

### How it works
