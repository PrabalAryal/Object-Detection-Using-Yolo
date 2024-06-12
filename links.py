import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd


def is_social_media(url):
    social_media_domain = [
        "twitter.com",
        "facebook.com",
        "instgram.com",
    ]  # add more if required
    for domain in social_media_domain:
        if domain in url:
            return True
    return False


def extract_all_links(url):
    try:
        # send a get request to the url
        response = requests.get(url)
        # check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # extract all the links using Beautiful Soup methods
            links = [a["href"] for a in soup.find_all("a", href=True)]
            # convert the relative url to absolute urls as soup returns relative urls
            links = [urljoin(url, link) for link in links]
            return links
        else:
            print(
                f"failed to retrieve data from {url}. Status code: {response.status_code}"
            )
            return []
    except requests.exceptions.RequestException as e:
        print(f"failed to retrieve data from {url}: {e}")
        return []


def save_links_to_csv(links, csv_filename):
    with open(csv_filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Links"])  # WRITE THE HEADER
        for link in links:
            csv_writer.writerow([link])

def extract_specific_content(url):
    try:
        response=requests.get(url)
        response.raise_for_status()

        soup=BeautifulSoup(response.text, "html.parser")
        #skip extraction from social media urls
        if is_social_media(url):
            return None,None,None,None,None,None # include the original link as None
        
        heading_element=soup.find("h1",{'style':'margin-bottom: 0.1rem;'})
        author_element=soup.find("h5",class_='text-capitalize')
        publication_date_element=soup.find("div",class_='updated-time')
        content_container=soup.find("div",class_='subscribe-wrapperx')
#assignment on difference between raise_for_status() and status_code
#