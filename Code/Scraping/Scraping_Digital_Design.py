# Scraping ITU webpage 
# Getting institutions with whom ITU has a collaboration by different areas (Digital Design, Computer Science and Business IT)
# Getting ITU artciles of different areas and different institutions and different years
# Scrapping Digital Design page

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm  # For progress bar
import time

## ITU WEBPAGE SCRAPING

# Path to your chromedriver executable
service = Service('C:/Users/Mikas/Desktop/Danish Studies/Data in Wild/Prerequisites/chromedriver-win64/chromedriver.exe') # needs to be modified personaly

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# URL of the page to be scraped
url = "https://pure.itu.dk/en/organisations/digital-design/network-organisations/"

# Load the webpage
driver.get(url)

# Maximize window (optional)
driver.maximize_window()

# Handle cookie banner if it appears
try:
    # Wait for the cookie banner to appear and click the accept button if available
    cookie_accept = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_accept.click()
    print("Cookie banner dismissed.")
except:
    print("No cookie banner to dismiss.")

# List to store the research data
research_data = []

try:
    # Wait for the page to load and find all the institutions on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid-result-content"))
    )

    # Find all institution elements
    institutions = driver.find_elements(By.CSS_SELECTOR, "div.grid-result-item")
    total_institutions = len(institutions)
    print(f"Found {total_institutions} institutions.")

    # Initialize the progress bar
    progress_bar = tqdm(total=total_institutions, desc="Scraping Institutions", unit="institution")

    # Iterate over each institution and collect data
    for institution in institutions:
        try:
            # Get institution name from h2.title within the div.grid-result-content
            institution_name = institution.find_element(By.CSS_SELECTOR, "h2.title span").text.strip()
            print(f"Processing institution: {institution_name}")
            
            # Click on the popup link for this institution
            popup_link = institution.find_element(By.CSS_SELECTOR, "a.popup-collaborators")
            ActionChains(driver).move_to_element(popup_link).perform()
            popup_link.click()

            # Wait for the popup to appear and load the content
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-container.content-popup"))
            )

            # Locate the main container of the popup where all articles and years are listed
            popup_container = driver.find_element(By.CSS_SELECTOR, "div.dropdown-container.content-popup ul.content-popup-wrapper")

            # Locate all year elements within the popup using h3.title elements
            year_elements = popup_container.find_elements(By.CSS_SELECTOR, "li > h3.title")

            # Iterate over each year section to extract the year and corresponding titles
            for year_element in year_elements:
                try:
                    year_text = year_element.text.strip()
                    print(f"  Year: {year_text}")

                    # Get the current year element and its next siblings until the next year or end of the container
                    current_year_li = year_element.find_element(By.XPATH, "..")
                    next_sibling = current_year_li.find_elements(By.XPATH, "./following-sibling::li")

                    for sibling in next_sibling:
                        # Check if the sibling is another year title; if so, break the loop
                        if sibling.find_elements(By.CSS_SELECTOR, "h3.title"):
                            break

                        # Now we are in the article list for this year
                        try:
                            # Extract the article title
                            title_element = sibling.find_element(By.CSS_SELECTOR, "h2.title span")
                            title = title_element.text.strip()
                            research_data.append([institution_name, year_text, title])
                            print(f"    Found paper: {title}")
                        except Exception as e:
                            print(f"    Error processing a research paper under year {year_text}: {e}")
                            continue

                except Exception as e:
                    print(f"  Error extracting details for year {year_text}: {e}")
                    continue

            # Close the popup by clicking outside or pressing escape
            ActionChains(driver).move_by_offset(-10, -10).click().perform()
            time.sleep(1)  # Small delay to ensure popup closes before next iteration

            # Update the progress bar
            progress_bar.update(1)

        except Exception as e:
            print(f"Error processing institution {institution_name}: {e}")
            continue

    progress_bar.close()
    print(f"Found {len(research_data)} research papers across all institutions.")

except Exception as e:
    print(f"Error: {e}")

# Convert the list to a DataFrame
df = pd.DataFrame(research_data, columns=["Institution", "Year", "Title"])

# Save to Excel
excel_filename = 'institutions_years_papers_Digital_Design.xlsx'  # Update path if needed
df.to_excel(excel_filename, index=False)

# Close the browser
driver.quit()

print(f"Data has been successfully written to {excel_filename}")