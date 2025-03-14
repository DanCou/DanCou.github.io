from bs4 import BeautifulSoup
import requests

# URL of the webpage to scrape
url = "https://www.parislenezenlair.fr/se-balader/les-solutions/solutions/216-solution-n-29-de-convention-a-montparnasse.html"

# Fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the articleBody div
article_body = soup.find("div", itemprop="articleBody")

# Lists to store extracted texts
paragraph_texts = []
italic_texts = []

if article_body:
    paragraphs = article_body.find_all("p")
    
    for p in soup.find_all("p"):
        # Extract the text excluding <em> content
        main_text = p.get_text(" ", strip=True)
        
        # Extract <em> content separately
        em_texts = [em.get_text(strip=True) for em in p.find_all("em")]

        # Remove <em> content from main text
        for em_text in em_texts:
            main_text = main_text.replace(em_text, "").strip()

        # Append to respective lists
        paragraph_texts.append(main_text)
        italic_texts.extend(em_texts)  # Extend in case multiple <em> tags exist

    # Print results
    print("Paragraph Texts:", paragraph_texts)
    print("Italic Texts:", italic_texts)

else:
    print("No article body found!")

for t,i in zip(paragraph_texts, italic_texts):
    print(t)
    print()
    print(i)
    print("---")


