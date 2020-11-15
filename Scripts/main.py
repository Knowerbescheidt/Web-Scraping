import requests
from bs4 import BeautifulSoup
import pandas as pd


def extraction_of_tags(numb_of_pages):
    """
    Creates the list of tags for the url: http://books.toscrape.com/catalogue/page-{pagenumb}.html
    ---------------
    Parameters: 
        numb_of_pages (numb): number of pages you want included. 
        
    Returns: 
        product_tags (List): A List containing tag elements from the bs4 package. 
    """
    product_tags = []
    for page in range(1, numb_of_pages):  
        url = 'http://books.toscrape.com/catalogue/page-{pagenumb}.html'.format(pagenumb= page)
        req = requests.get(url)
        text_webpage = req.text
        soup = BeautifulSoup(text_webpage)
        for product_tag in soup.find_all('article'):
            product_tags.append(product_tag)
    return product_tags


def analyzing_tags(prod_tag_list):
    """
    Extracts information from the provided list of tags
    ---------------
    Parameters: 
        prod_tag_list (list): The tags which inherits the information. 
        
    Returns: 
        products (Dictionary): A Dictionary containing key: title, price, rating and availability. 
    """
    products = []
    for tag in prod_tag_list:
        product_info = {}
        
        # get book title
        img_tag = tag.find_all('img')
        title = img_tag[0].attrs['alt']
        product_info['title'] = title

        # get book price
        p_tags = tag.find_all('p')
        price_tag = [tag for tag in p_tags if tag.attrs['class'][0]=='price_color']
        price = price_tag[0].getText()
        product_info['price'] = price[1:]

        # get rating
        rating_tag = [tag for tag in p_tags if 'rating' in tag.attrs['class'][0]]
        rating = rating_tag[0].attrs['class'][1]
        product_info['rating'] = rating

        # get availability
        availability_tag = [tag for tag in p_tags if 'availability' in tag.attrs['class']]
        availability_clean = availability_tag[0].getText().replace('\n',' ').strip()
        product_info['available'] = availability_clean
        products.append(product_info)
    
    return products

def transform(product_dict):
    """
    Transforms the data that is provided in a defined way and returns a dataframe
    ---------------
    Parameters: 
        product_dict (Dictionary): The data to be transformed. 
        
    Returns: 
        df_data: A pandas Dataframe. 
    """
    df_data = pd.Dataframe(product_dict)
    # place for further options
    return df_data


if __name__ == "__main__":
    # extract tags
    prod_tag_list = extraction_of_tags(numb_of_pages=50)
    # analyse tags
    product_data = analyzing_tags(prod_tag_list)
    # transform data & write csv
    data_df = transform(product_data)