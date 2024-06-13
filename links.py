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
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # skip extraction from social media urls
        if is_social_media(url):
            return (
                None,
                None,
                None,
                None,
                None,
                None,
            )  # include the original link as None

        heading_element = soup.find("h1", {"style": "margin-bottom: 0.1rem;"})
        author_element = soup.find("h5", class_="text-capitalize")
        publication_date_element = soup.find("div", class_="updated-time")
        content_container = soup.find("div", class_="subscribe-wrapperx")
        # determine the category based on the url
        url_parts = urlparse(url).path.split("/")
        category = next((part for part in url_parts if part), "Category not found")
        heading = (
            heading_element.text.strip() if heading_element else "Heading not found"
        )
        author = author_element.text.strip() if author_element else "Author not found"
        publication_date_raw = (
            publication_date_element.text.strip()
            if publication_date_element
            else "Date not found"
        )
        publication_date = publication_date_raw.replace("Published on:", "").strip()
        content = (
            content_container.get_text(separator=" ", strip=True)
            if content_container
            else "Content not found"
        )
        return heading, author, publication_date, content, category, url
    except requests.exceptions.RequestException as e:
        print(f"failed to retrieve data from {url}: {e}")
        return None, None, None, None, None, url


def save_to_csv(data, csv_file_path):
    with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            [
                "Heading",
                "Author",
                "Publication Date",
                "Source",
                "Content",
                "Category",
                "URL",
            ]
        )
        csv_writer.writerow(data)


def main():
    csv_file_path = "kathmandupost.csv"
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            [
                "Heading",
                "Author",
                "Publication Date",
                "Source",
                "Content",
                "Category",
            ]
        )
    url = "https://kathmandupost.com"
    links = extract_all_links(url)
    csv_filename = "data_links.csv"
    save_links_to_csv(links, csv_filename)

    print(f"all links saveds to {'data_links.csv'}")
    link = pd.read_csv("data_links.csv")
    for url in links:
        if not urlparse(url).scheme:
            url = urljoin("https://", url)
        if urlparse(url).netloc and not is_social_media(url):
            heading, author, publication_date, content, category, link = (
                extract_specific_content(url)
            )
            if heading is not None and author is not None and content is not None:
                data_to_save = [
                    heading,
                    author,
                    publication_date,
                    "Kathmandu-Post",
                    content,
                    link,
                    category,
                ]
                print(
                    f"Data for {url}: \nHeading: {heading}\nAuthor{author}\nPublication Date: {publication_date}\SOurce: Kathmandu-Post \nContent: {content}\nLink{link}\nCategory: {category}"
                )
                save_to_csv(data_to_save, csv_file_path)
                print(f"Data saved for {url}")
            else:
                print(f"Data not found in {url}")


if __name__ == "__main__":
    main()
