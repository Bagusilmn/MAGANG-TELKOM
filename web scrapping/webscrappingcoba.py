
from bs4 import BeautifulSoup 
import requests 
import pandas as pd
import time

ROOT = "https://get-information-schools.service.gov.uk"
TEMPLATE = f"{ROOT}/Establishments/Search?tok=8TjW1JHQ&startIndex={{startIndex}}&Count=3702"

# get urls for all 75 search pages
def get_index_pages():
    return [TEMPLATE.format(startIndex=startIndex) for startIndex in range(0, 3750, 50)]

pages = get_index_pages()


# retrieve url of each school page from search pages
def get_school_pages(index_page):

    resp = requests.get(index_page)
    html = BeautifulSoup(resp.content, 'html.parser')
    school_links = html.find_all('a', class_="bold-small")

    output = []

    for school in school_links:
        details = {}

        name = school.contents[0]
        page_link = school.get('href')

        details["name"] = name
        details["link"] = f"{ROOT}{page_link}"

        output.append(details)
    
    return output

schools = []
for index_page in pages:
    schools = schools + get_school_pages(index_page)
    print(f"trying {index_page}")
    time.sleep(1)
    

# get school's website domain
def get_school_details(url):

    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    html_summary = html.find(id = "details-summary")

    return html_summary

def find_website(html):

    if not html:
        return None

    cols = html.find_all("dt")

    for col in cols:
        if col.get_text() == "Website:":
            tag = col.find_next_sibling("dd")
            # TODO: Change me
            try: 
                website = tag.find("a").get('href')
            except AttributeError:
                website = None 
            return website

for school in schools:
    print(f"trying school: {school['name']}")
    url = school["link"]
    
    details = get_school_details(url)
    website = find_website(details)

    school["website"] = website
    
    time.sleep(1)


# save as csv
schools_df = pd.DataFrame(schools)

schools_df.to_csv("school-page-links.csv")