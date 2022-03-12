import requests
from bs4 import BeautifulSoup as bs


def scraper():
    page_number = 47
    while page_number != 1:
        url = 'https://wall.alphacoders.com/tag/kitten-wallpapers?quickload=1401&page=' + str(page_number)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/84.0.4316.21'
        }
        result = requests.get(url, headers=headers)
        html_soup = bs(result.text, 'html.parser')
        img_div = html_soup.find_all('img', class_='img-responsive')

        images_url = []
        for image in img_div:
            cleaned_url = image['src']
            images_url.append(cleaned_url)
            # print(len(images_url))
        page_number -= 1
        print(page_number)

        with open("images_url.txt", "a") as file:
            print("\n".join(map(str, images_url)), file=file)


def main():
    scraper()


if __name__ == '__main__':
    main()
