import requests
from bs4 import BeautifulSoup
from utils import extract_text_from_pdf, parse_exam_results

SCHOOLS = {
    "Eton College": "https://www.etoncollege.com/about-us/exam-results/",
    "Harrow School": "https://www.harrowschool.org.uk/academic/examination-results",
    "Winchester College": "https://www.winchestercollege.org/academic/results",
    "Cheltenham Ladies’ College": "https://www.cheltladiescollege.org/information/results/",
    "Westminster School": "https://www.westminster.org.uk/exam-results/"
}

def fetch_results_for_school(name):
    url = SCHOOLS.get(name)
    if not url:
        return {}

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        pdf_links = [a["href"] for a in soup.find_all("a", href=True) if ".pdf" in a["href"]]
        results = {}

        for link in pdf_links[:1]:
            if not link.startswith("http"):
                link = url.rstrip("/") + "/" + link.lstrip("/")
            text = extract_text_from_pdf(link)
            parsed = parse_exam_results(text)
            results[link] = parsed

        if not results:
            fallback = []
            for p in soup.find_all(["p", "li"]):
                text = p.get_text(strip=True)
                if any(word in text.lower() for word in ["gcse", "a-level", "ib"]):
                    fallback.append(text)
            results["Web Page Content"] = fallback or ["No relevant content found."]

        return results

    except Exception as e:
        return {"Error": str(e)}
