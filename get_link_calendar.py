from bs4 import BeautifulSoup
import requests

visited_sites = []  # Link of visited sites during the recursive query.

"""
    get_hrefs():
        Returns all href links found in a page.
        
        [Parameters]:
            url:        The URL of the page we are searching for hrefs.
            server_url: The base URL so that we are not finding links 
                        that does not belongs to the current website.
"""
def get_links(url, server_url):
    response = requests.get(url)
    data     = response.text
    soup     = BeautifulSoup(data, 'lxml')

    links    = []
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url:

            # Remove the cases where links point to nowhere
            if '#' in link_url:
                continue
            if 'javascript:void(0);' == link_url:
                continue
            if 'mailto' in link_url:
                continue

            # Append to make full link if needed
            if server_url not in link_url:
                if link_url[0] == '/':
                    link_url = server_url + link_url
                elif link_url[:4] != 'http':
                    link_url = url + link_url

            # Don't give a shit if the link repeated
            global visited_sites
            if link_url in visited_sites:
                continue
            visited_sites.append(link_url)

            # Append to array of new links
            if url in link_url and url != link_url:
                links.append(link_url)

    return links


"""
    get_google_calendar():
        Get Google Calendar's URL and title embeded in the HTML file
        of an URL.

        [Parameters]:
            url: The URL that points to a page that may or may not
                 contains a Google Calendar.
"""
def get_google_calendar(url):
    response = requests.get(url)
    data     = response.text
    soup     = BeautifulSoup(data, 'lxml')

    for link in soup.find_all('iframe'):
        calendar_url = link.get('src')
        if calendar_url and 'calendar.google.com' in calendar_url:
            headers = soup.find_all('header')
            for header in headers:
                if header.get('class') == ['blog-detail-header']:
                    try:
                        title = header.find_all('h2')[0].contents[0]
                        return title, calendar_url
                    except:
                        return None, calendar_url

    return None, None

"""
    recursive_get():
        Recursively finds and appends URLs that contains Google Calendar
        to an array starting from an URL. The result is written to a file.

        [Parameters]:
            url: The starting URL to begin with.
            output_filename: The output file where the program dumps the link into.
"""
def recursive_get(url, output_filename):
    # Open the file and clear the current content.
    calendar_file = open(output_filename, 'w')
    calendar_file.write('')

    # Get the data we need
    title, calendar_url = get_google_calendar(url)
    if title:
        calendar_file.write(title + ' ' + calendar_url + '\n')
    else:
        for each_link in get_links(url, "https://usth.edu.vn"):
            recursive_get(each_link)


recursive_get('https://usth.edu.vn/en/timetable/', 'calendar_urls.txt')
