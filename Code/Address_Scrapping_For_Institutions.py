## ADDRESS SCRAPING FOR EACH INSTITUTION
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

# Load the Excel file
file_path = 'Institution_Papers.xlsx'
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
output_file = 'Institution_Addresses.xlsx'
institutions_df.to_excel(output_file, index=False)
print(f"Data for all institutions saved to {output_file}")