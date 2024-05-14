
import requests
from bs4 import BeautifulSoup
import csv

def get_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []

    for product in soup.find_all('div', {'data-component-type': 's-search-result'}):
        try:
            name = product.find('span', {'class': 'a-size-medium'}).text.strip()
        except AttributeError:
            name = "Not Available"

        try:
            price = product.find('span', {'class': 'a-price'}).find('span', {'class': 'a-offscreen'}).text
        except AttributeError:
            price = "Not Available"

        try:
            rating = product.find('span', {'class': 'a-icon-alt'}).text.split()[0]
        except AttributeError:
            rating = "Not Available"

        products.append({'Name': name, 'Price': price, 'Rating': rating})

    return products

def save_to_csv(products):
    with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Price', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def main():
    url = 'https://www.amazon.com/s?k=laptop'
    products = get_product_info(url)
    save_to_csv(products)
    print("Product information saved to products.csv")

if __name__ == "__main__":
    main()
