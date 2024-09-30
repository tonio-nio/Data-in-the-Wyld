
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to be scraped
url = "https://pure.itu.dk/en/organisations/computer-science/network-organisations/"

# Headers to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Requesting the page
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the 'network-nonprofiled-institutions' div
    nonprofiled_section = soup.find('div', class_='network-nonprofiled-institutions')
    
    # Check if the section exists
    if nonprofiled_section:
        # Find all the institution names within the 'grid-result-content' class in the non-profiled section
        institutions = nonprofiled_section.find_all('div', class_='grid-result-content')
        
        # List to store the institution names
        institution_names = []

        # Extract each institution name
        for institution in institutions:
            name = institution.find('h2', class_='title').text.strip()
            institution_names.append(name)
        
        # Creating a DataFrame from the list
        df = pd.DataFrame(institution_names, columns=['Institution Name'])

        # Saving the DataFrame to an Excel file
        excel_filename = 'nonprofiled_institution_list.xlsx'
        df.to_excel(excel_filename, index=False)
        
        print(f"Data has been successfully written to {excel_filename}")
    else:
        print("The 'network-nonprofiled-institutions' section was not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
'''
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Path to your chromedriver executable
service = Service('C:/Users/Mikas/Desktop/Danish Studies/Data in Wild/Prerequisites/chromedriver-win64/chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# URL of the page to be scraped
url = "https://pure.itu.dk/en/organisations/computer-science/network-organisations/"

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

# List to store the years for the institution
institution_years = []

try:
    # Wait for the page to load and find the link for the "University of Copenhagen"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid-result-content"))
    )

    # Locate the "University of Copenhagen" section using its 'popup-collaborators' class
    popup_link = driver.find_element(By.XPATH, "//a[contains(@class, 'popup-collaborators') and contains(text(), '128 shared research output')]")
    
    # Scroll to the link to ensure it's in view and then click
    ActionChains(driver).move_to_element(popup_link).perform()
    popup_link.click()

    # Wait for the popup to appear and load the content
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-container.content-popup"))
    )

    # Locate all year elements within the popup using h3.title elements
    year_elements = driver.find_elements(By.CSS_SELECTOR, "h3.title")

    # Extract the year text from each h3.title
    for year_element in year_elements:
        try:
            year_text = year_element.text.strip()
            institution_years.append(["University of Copenhagen", year_text])
        except Exception as e:
            print(f"Error extracting year details: {e}")
            continue

    print(f"Found {len(institution_years)} years for 'University of Copenhagen'.")

except Exception as e:
    print(f"Error: {e}")

# Convert the list to a DataFrame
df = pd.DataFrame(institution_years, columns=["Institution", "Year"])

# Save to Excel
excel_filename = 'C:/Users/Mikas/Desktop/copenhagen_years.xlsx'  # Update path if needed
df.to_excel(excel_filename, index=False)

# Close the browser
driver.quit()

print(f"Data has been successfully written to {excel_filename}")
'''
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Path to your chromedriver executable
service = Service('C:/Users/Mikas/Desktop/Danish Studies/Data in Wild/Prerequisites/chromedriver-win64/chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# URL of the page to be scraped
url = "https://pure.itu.dk/en/organisations/computer-science/network-organisations/"

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
    # Wait for the page to load and find the link for the "University of Copenhagen"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid-result-content"))
    )

    # Locate the "University of Copenhagen" section using its 'popup-collaborators' class
    popup_link = driver.find_element(By.XPATH, "//a[contains(@class, 'popup-collaborators') and contains(text(), '128 shared research output')]")
    
    # Scroll to the link to ensure it's in view and then click
    ActionChains(driver).move_to_element(popup_link).perform()
    popup_link.click()

    # Wait for the popup to appear and load the content
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-container.content-popup"))
    )

    print("Popup opened successfully.")

    # Locate the main container of the popup where all articles and years are listed
    popup_container = driver.find_element(By.CSS_SELECTOR, "div.dropdown-container.content-popup ul.content-popup-wrapper")

    # Locate all year elements within the popup using h3.title elements
    year_elements = popup_container.find_elements(By.CSS_SELECTOR, "li > h3.title")

    if not year_elements:
        print("No year elements found.")
    
    # Iterate over each year section to extract the year and corresponding titles
    for i, year_element in enumerate(year_elements):
        try:
            year_text = year_element.text.strip()
            print(f"Processing year: {year_text}")

            # Determine the articles corresponding to this year
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
                    research_data.append(["University of Copenhagen", year_text, title])
                    print(f"Found paper: {title}")
                except Exception as e:
                    print(f"Error processing a research paper under year {year_text}: {e}")
                    continue

        except Exception as e:
            print(f"Error extracting details for year {year_text}: {e}")
            continue

    print(f"Found {len(research_data)} research papers for 'University of Copenhagen'.")

except Exception as e:
    print(f"Error: {e}")

# Convert the list to a DataFrame
df = pd.DataFrame(research_data, columns=["Institution", "Year", "Title"])

# Save to Excel
excel_filename = 'C:/Users/Mikas/Desktop/copenhagen_research_papers_with_titles.xlsx'  # Update path if needed
df.to_excel(excel_filename, index=False)

# Close the browser
driver.quit()

print(f"Data has been successfully written to {excel_filename}")
'''
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm  # For progress bar
import time

# Path to your chromedriver executable
service = Service('C:/Users/Mikas/Desktop/Danish Studies/Data in Wild/Prerequisites/chromedriver-win64/chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# URL of the page to be scraped
url = "https://pure.itu.dk/en/organisations/computer-science/network-organisations/"

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
    institutions = driver.find_elements(By.CSS_SELECTOR, "a.popup-collaborators")
    total_institutions = len(institutions)
    print(f"Found {total_institutions} institutions.")

    # Initialize the progress bar
    progress_bar = tqdm(total=total_institutions, desc="Scraping Institutions", unit="institution")

    # Iterate over each institution and collect data
    for institution in institutions:
        try:
            # Get institution name and click on its link
            institution_name = institution.text.split("\n")[0]
            print(f"Processing institution: {institution_name}")
            
            ActionChains(driver).move_to_element(institution).perform()
            institution.click()

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
excel_filename = 'C:/Users/Mikas/Desktop/institutions_research_papers.xlsx'  # Update path if needed
df.to_excel(excel_filename, index=False)

# Close the browser
driver.quit()

print(f"Data has been successfully written to {excel_filename}")
'''
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

'''
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

# Load the Excel file
file_path = 'nonprofiled_institution_list.xlsx'
institutions_df = pd.read_excel(file_path)

# Check the first few rows of the dataframe to understand its structure
print(institutions_df.head())

# Function to get address or headquarters for an institution
def get_institution_info(institution_name):
    # Replace spaces with '+' for the URL
    formatted_name = institution_name.replace(" ", "+")
    search_url = f"https://www.google.com/search?q={formatted_name}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'  # Request the page in English
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for the presence of the Knowledge Graph panel
        info_panel = soup.find('div', {'class': 'kp-wholepage'})
        
        # Default to None if no address is found
        address = None
        
        if info_panel:
            # Extract text content with known data-attribute identifiers
            potential_fields = info_panel.find_all('div', {'data-attrid': ['kc:/location/location:address', 'kc:/organization/organization:headquarters']})
            
            for field in potential_fields:
                # Checking the <font> tag for addresses as seen in the images
                font_tag = field.find('font', {'style': 'vertical-align: inherit;'})
                if font_tag:
                    address = font_tag.get_text(separator=' ').strip()
                else:
                    # Fallback to the full field text content
                    address = field.get_text(separator=' ').strip()
                
                if address:
                    break

        return address if address else "No address found"
    
    except Exception as e:
        print(f"Error fetching data for {institution_name}: {e}")
        return None

# Add columns for address
institutions_df['Address'] = None

# Loop through all institutions and get the address with progress bar
for index, row in tqdm(institutions_df.iterrows(), total=len(institutions_df), desc="Processing Institutions"):
    institution_name = row['Institution Name']  # Adjusted to the correct column name
    address = get_institution_info(institution_name)
    institutions_df.at[index, 'Address'] = address
    
    # Sleep to avoid too frequent requests
    time.sleep(2)  # Increase delay to 2 seconds to be more cautious

# Save the updated dataframe back to an Excel file
output_file = 'institution_with_addresses_all.xlsx'
institutions_df.to_excel(output_file, index=False)
print(f"Data for all institutions saved to {output_file}")
'''

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

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
service = Service('C:/Users/Mikas/Desktop/Danish Studies/Data in Wild/Prerequisites/chromedriver-win64/chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# URL of the page to be scraped
url = "https://pure.itu.dk/en/organisations/computer-science/network-organisations/"

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
excel_filename = 'C:/Users/Mikas/Desktop/institutions_research_papers.xlsx'  # Update path if needed
df.to_excel(excel_filename, index=False)

# Close the browser
driver.quit()

print(f"Data has been successfully written to {excel_filename}")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
## ADDRESS SCRAPING FOR EACH INSTITUTION

# Load the Excel file
file_path = 'nonprofiled_institution_list.xlsx'
institutions_df = pd.read_excel(file_path)

# Check the first few rows of the dataframe to understand its structure
print(institutions_df.head())

# Function to get address or headquarters for an institution
def get_institution_info(institution_name):
    # Replace spaces with '+' for the URL
    formatted_name = institution_name.replace(" ", "+")
    search_url = f"https://www.google.com/search?q={formatted_name}&hl=en"  # Add &hl=en to force English

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'  # Request the page in English
    }

    def get_address_from_info_panel(panel):
        # Try extracting address or headquarters data
        potential_fields = panel.find_all('div', {'data-attrid': ['kc:/location/location:address', 'kc:/organization/organization:headquarters']})
        for field in potential_fields:
            font_tag = field.find('font', {'style': 'vertical-align: inherit;'})
            if font_tag:
                return font_tag.get_text(separator=' ').strip()
            else:
                # Fallback to the full field text content
                return field.get_text(separator=' ').strip()
        return None

    def get_address_from_google_maps(soup):
        # Try to find the Google Maps link if present
        maps_link = soup.find('a', href=True, text="Directions")
        if maps_link:
            # Google Maps link contains address in the query parameter, let's parse it
            try:
                map_href = maps_link['href']
                # Extract address from query parameters
                address = map_href.split('/place/')[1].split('/')[0]
                return address.replace('+', ' ')
            except Exception as e:
                print(f"Failed to extract address from Google Maps link for {institution_name}: {e}")
                return None
        return None

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for the presence of the Knowledge Graph panel
        info_panel = soup.find('div', {'class': 'kp-wholepage'})
        
        # Default to None if no address is found
        address = None
        
        if info_panel:
            # Try to get the address from the info panel
            address = get_address_from_info_panel(info_panel)
        
        # If no address is found in the info panel, try to get it from Google Maps link
        if not address:
            address = get_address_from_google_maps(soup)

        return address if address else "No address found"
    
    except Exception as e:
        print(f"Error fetching data for {institution_name}: {e}")
        return None

# Add columns for address
institutions_df['Address'] = None

# Loop through all institutions and get the address with progress bar
for index, row in tqdm(institutions_df.iterrows(), total=len(institutions_df), desc="Processing Institutions"):
    institution_name = row['Institution Name']  # Adjusted to the correct column name
    address = get_institution_info(institution_name)
    institutions_df.at[index, 'Address'] = address
    
    # Sleep to avoid too frequent requests
    time.sleep(2)  # Increase delay to 2 seconds to be more cautious

# Save the updated dataframe back to an Excel file
output_file = 'institution_with_addresses_all_updated.xlsx'
institutions_df.to_excel(output_file, index=False)
print(f"Data for all institutions saved to {output_file}")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------