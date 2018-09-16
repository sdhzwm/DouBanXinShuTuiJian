import requests
from bs4 import BeautifulSoup
import csv


# 请求访问网址
def get_books():
    URL = 'https://book.douban.com/latest'
    try:
        r = requests.get(URL, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.92 Safari/537.36'})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('fail')


# 解析数据
def get_info(text):
    soup = BeautifulSoup(text, 'html.parser')
    # 得到图书列表
    books_left = soup.find('ul', {'class': 'cover-col-4 clearfix'})
    books_left = books_left.find_all('li')
    books_right = soup.find('ul', {'class': 'cover-col-4 pl20 clearfix'})
    books_right = books_right.find_all('li')
    return books_left, books_right


# 对每本图书进行相同的操作，得到信息
img_urls = []
titles = []
ratings = []
authors = []
details = []


def get_left(books_left):
    for book in books_left:
        # 图书封面图片url地址
        img_url = book.find_all('a')[0].find('img').get('src')
        img_urls.append(img_url)
        # 图书标题
        title = book.find_all('a')[1].get_text()
        titles.append(title)
        # 评价星级
        rating = book.find('p', {'class': 'rating'}).get_text()
        rating = rating.replace('\n', '').replace(' ', '')
        ratings.append(rating)
        # 作者及出版信息
        author = book.find('p', {'class': 'color-gray'}).get_text()
        author = author.replace('\n', '').replace(' ', '')
        authors.append(author)
        # 图书简介
        detail = book.find('p', {'class': 'detail'}).get_text()
        datail = detail.replace('\n', '').replace(' ', '')
        detail = detail[1:-1].strip()
        details.append(detail)


def get_right(books_right):
    for book_right in books_right:
        # 图书封面图片url地址
        img_url = book_right.find('a').find('img').get('src')
        img_urls.append(img_url)
        # 图书标题
        title = book_right.find_all('a')[1].get_text()
        titles.append(title)
        # 评价星级
        rating = book_right.find('p', {'class': 'rating'}).get_text()
        rating = rating.replace('\n', '').replace(' ', '')
        ratings.append(rating)
        # 作者及出版信息
        author = book_right.find('p', {'class': 'color-gray'}).get_text()
        author = author.replace('\n', '').replace(' ', '')
        authors.append(author)
        # 图书简介
        detail = book_right.find_all('p')[-1].get_text()
        datail = detail.replace('\n', '').replace(' ', '')
        detail=detail[1:-1].strip()
        details.append(detail)


# 执行
def run():
    text = get_books()
    books_left, books_right = get_info(text)
    get_left(books_left)
    get_right(books_right)


# 保存
def save(img_urls, titles, ratings, authors, details):
    with open('books.csv', 'w', encoding='utf-8') as f:
        head = (('img_urls', 'titles', 'ratings', 'authors', 'details'))
        result = []
        f_csv = csv.writer(f)
        f_csv.writerow(head)
        for i in range(len(titles)):
            f_csv.writerow((img_urls[i], titles[i], ratings[i], authors[i],details[i]))


if __name__ == '__main__':
    run()
    save(img_urls, titles, ratings, authors, details)
