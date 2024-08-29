import time

import requests
from bs4 import BeautifulSoup

# Step 1: Retrieve the list of investors
base_url = 'https://valuesider.com/'
index_url = 'https://valuesider.com/value-investors'  # This URL needs to be the page where all investors are listed
response = requests.get(index_url)
soup = BeautifulSoup(response.text, 'lxml')

# Finding all links to investor pages (assuming they are contained in 'a' tags within a specific class)
investor_links = [a['href'] for a in soup.select('.guru_table_column.long_text_ellipsis a')]

# Print out the found links to debug and confirm
print(f"Found {len(investor_links)} investor links.")
for link in investor_links:
    print(link)

investor_file = open('investor_file.csv','a')
investor_file.write('investor_name,investor_company,ticker,stock,percent_portfolio,shares,reported_price,percent_difference_current_price,current_price,value,percent_activity,percent_change_to_portfolio\n')


# step 2: Iterate over each investor's page
for investor_url in investor_links:
    time.sleep(1)
    i = 1
    guru_done = False
    while not guru_done:

        url = f'{investor_url}?sells_page=1&page={i}'
        bad_response = True
        while bad_response:
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                    bad_response = False
            else:
                print('bad response: ', response.status_code)
                time.sleep(60)

        content = response.text

        soup = BeautifulSoup(content,'lxml')

        breadcrumb = soup.find('div', class_='breadcrumb-content d-flex flex-column align-items-center text-center')


        name = breadcrumb.find('h2', class_='tag-h2 text-white text-uppercase').text.strip()
        # Extract Berkshire Hathaway
        company = breadcrumb.find('div', class_='tag-h4 text-white text-uppercase').text.strip()
        print(f"{name}, {company}")

        table = soup.find('div',class_='guru_table_body')
        rows = table.find_all('div',class_='guru_table_row row')
        if len(rows) == 0:
            break
        for row in rows:
            ticker = row.find('div', class_ = 'guru_table_column scroll-fix text-center').text.strip()
            stock = row.find ('div', class_ = 'guru_table_column long_text_ellipsis').text.strip()
            percent_portfolio = row.find_all('div', class_ = 'guru_table_column text-center')[1].text.strip()
            shares_and_reported_price = row.find_all('div', class_ ='guru_table_column')
            shares = shares_and_reported_price[4].text.strip()
            reported_price = shares_and_reported_price[5].text.strip()

            percent_difference_current_price = row.find('span', class_='pl-1 pr-2')
            if percent_difference_current_price is None:
                percent_difference_current_price = '0'
            else:
                percent_difference_current_price = percent_difference_current_price.text.strip()

            current_price = shares_and_reported_price[6].find_all('span')
            if not current_price:
                current_price = '0'
            else:
                current_price = current_price[-1].text
            value = shares_and_reported_price[7].text.strip()
            percent_activity = row.find('span', class_='normal')
            if percent_activity:
                percent_activity = percent_activity.text.strip()
            else:
                percent_activity = '0'  # Default to '0' if percent_activity is empty
            percent_change_to_portfolio = row.find('div', class_='guru_table_column is_change text-center activity_status_-1')
            if percent_change_to_portfolio:
                percent_change_to_portfolio = percent_change_to_portfolio.text.strip()
            else:
                percent_change_to_portfolio = '0'  # Default to '0' if percent_activity is empty
            print(ticker, stock, percent_portfolio, shares, reported_price, percent_difference_current_price,
                  current_price, value, percent_activity, percent_change_to_portfolio)
            investor_file.write(
                f'{name},{company},{ticker},{stock},{percent_portfolio},{shares},{reported_price},{percent_difference_current_price},{current_price},{value},{percent_activity},{percent_change_to_portfolio}\n')
        print(f'Pge {i} done')

        i += 1

investor_file.close()