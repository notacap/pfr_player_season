from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import os

def scrape_data():
    # Set up Selenium WebDriver
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the page
    url = 'https://www.pro-football-reference.com/players/A/AlleKe00/gamelog/2023/'
    driver.get(url)

    # Get the page source and close the browser
    html = driver.page_source
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Update the ID to the table ID containing the data you want to scrape
    table = soup.find('table', {'id': 'stats'})
    
    # Extracting data from the table
    if table:
        rows = table.find_all('tr')
        data = []
        for row in rows:
            if row.find('th', {'scope': 'row'}) is not None:  # This skips the header row
                cols = row.find_all('td')
                data.append([ele.text.strip() for ele in cols])
        
        # Debug: Print sample data
        if data:
            print("Sample data row:", data[0])
        
        # Creating a DataFrame and specifying column headers
        # Filter out empty headers explicitly
        columns = [th.getText() for th in table.find_all('tr')[1].find_all('th') if th.getText().strip()]
        print("Extracted columns:", columns)
        
        # Check if the number of columns matches the data
        if len(columns) == len(data[0]):
            df = pd.DataFrame(data, columns=columns)
            
            # Define the output directory
            output_dir = 'C:\\Users\\PC\\Desktop\\code\\data_files'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the DataFrame to the CSV file in the specified directory
            df.to_csv(os.path.join(output_dir, 'keenanallen_receiving_2023.csv'), index=False)
        else:
            print(f"Mismatch in columns and data: {len(columns)} columns, {len(data[0])} data points per row")
    else:
        print("Table not found!")

if __name__ == '__main__':
    scrape_data()
