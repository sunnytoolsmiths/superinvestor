import requests
from bs4 import BeautifulSoup

url = 'https://valuesider.com/guru/warren-buffett-berkshire-hathaway/portfolio?sells_page=1&page=1'
response = requests.get(url)
content = response.text

soup = BeautifulSoup(content,'lxml')

#print(soup.prettify())

table = soup.find('div',class_='guru_table_body')
rows = table.find_all('div',class_='guru_table_row row')
for row in rows:
    ticker = row.find('div', class_ = 'guru_table_column scroll-fix text-center').text.strip()
    stock = row.find ('div', class_ = 'guru_table_column long_text_ellipsis').text.strip()
    percent_portfolio = row.find_all('div', class_ = 'guru_table_column text-center')[1].text.strip()
    shares_and_reported_price = row.find_all('div', class_ ='guru_table_column')
    shares = shares_and_reported_price[4].text.strip()
    reported_price = shares_and_reported_price[5].text.strip()
    percent_difference_current_price = row.find ('span', class_ = 'pl-1 pr-2').text.strip()
    current_price = shares_and_reported_price[6].find_all('span')[-1].text
    value = shares_and_reported_price[7].text.strip()
    percent_activity = row.find('span', class_ = 'normal')
    if percent_activity:
        percent_activity = percent_activity.text.strip()
    else:
        percent_activity = '0'  # Default to '0' if percent_activity is empty
    percent_change_to_portfolio = row.find('div', class_='guru_table_column is_change text-center activity_status_-1')
    if percent_change_to_portfolio:
        percent_change_to_portfolio = percent_change_to_portfolio.text.strip()
    else:
        percent_change_to_portfolio = '0'  # Default to '0' if percent_activity is empty
    print(ticker, stock, percent_portfolio, shares, reported_price, percent_difference_current_price,current_price, value, percent_activity, percent_change_to_portfolio)
