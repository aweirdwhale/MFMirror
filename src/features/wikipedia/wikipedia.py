import requests

class Wikipedia:
    def __init__(self, subject):
        self.subject = subject
        self.url = 'https://fr.wikipedia.org/w/api.php'
        self.params = {
            'action': 'query',
            'format': 'json',
            'titles': self.subject,
            'prop': 'extracts|pageimages',
            'exintro': True,
            'explaintext': True,
        }
        self.recherche = []

    def fetch_data(self):
        response = requests.get(self.url, params=self.params)
        return response.json()

    def get_page_info(self):
        data = self.fetch_data()
        page = next(iter(data['query']['pages'].values()), None)
        return page

    def print_page_info(self):
        try:
            page = self.get_page_info()
            if page:
                # print to '\n' to get the first paragraph only
                print(page['extract'].split('\n')[0])
                # print image url
                image_link = page.get("thumbnail", {}).get("source")
                self.recherche.append(page['extract'].split('\n')[0])
                if image_link:
                    # replace 50px by 500px to get a bigger image
                    image_link = image_link.replace("50px", "500px")
                    print(f"{image_link}")
                    self.recherche.append(image_link)
                else:
                    print("No image available.")
                    self.recherche.append("503")
            else:
                print("Page not found.")
                self.recherche.append("404")
        except Exception as e:
            print(f"Error: {e}")
            self.recherche.append(f"404")


if __name__ == '__main__':
    subject = 'Ada Lovelace'
    wikipedia_fetcher = Wikipedia(subject)
    wikipedia_fetcher.print_page_info()
    print(wikipedia_fetcher.recherche)