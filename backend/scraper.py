import requests
from bs4 import BeautifulSoup
from models import Title, session
from urllib.parse import urljoin

BASE_URL = "https://app.leg.wa.gov/rcw/"

def scrape(url):
    try:
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"error: {e}")
        return None

homepage = scrape(BASE_URL)

'''
heading: Section name
section_id: Section ID
section_url: Citation/URL to section
content_paragraph: Content of the section

'''

### Scrape URLS only titles 1 2 and 3 ###
titles = homepage.find("h3", string="RCWs by Title").find_next_sibling("table").find_all("a", href=lambda x: x and "default.aspx?Cite=" in x)
filtered = [a for a in titles if a.get_text(strip=True) in {"Title 1","Title 2","Title 3"}]

for t in filtered:
    title_url = urljoin(BASE_URL, t["href"])
    chapter_page = scrape(title_url)
    chapters = chapter_page.find("h3", string="Chapters").find_next_sibling("table").find_all("a", href=lambda x: x and "default.aspx?cite=" in x)

    for c in chapters:
        chapter_url = c["href"]
        section_page = scrape(chapter_url)
        sections = section_page.find_all("a", string="HTML", href=lambda x: x and "default.aspx?cite=" in x and "=true" not in x)

        for s in sections:
            section_url = s["href"]
            content = scrape(section_url)
            section_id = section_url[section_url.find("=")+1:]
            heading = content.find_all("h3")[1].get_text(strip=True)

            content_paragraph = content.find("div", style=lambda x: x and "text-indent:0.5in;" in x).get_text(strip=True)

### Store into database ###
            db = session()
            title = Title(id = section_id, title = heading, content = content_paragraph, citation = section_url)
            db.add(title)
            print(f"Inserting {section_id} – {heading}")
            db.commit()
            print("done")
            db.close()



