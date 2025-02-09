import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    chrome_options = Options()
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

def read_games_from_excel(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found at: {file_path}")
            
        df = pd.read_excel(file_path)
        
        # Clean up column names by stripping any extra spaces
        df.columns = df.columns.str.strip()

        # Print the columns to verify what is being read
        print("Columns in the Excel file:", df.columns)

        # Verify required columns exist
        required_columns = ["כותרת", "ז'אנר", "מחיר", "כמות"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def add_games_to_store(games):
    if not games:
        print("No games data to process")
        return
        
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    try:
        # Open the Game Store Management System page
        driver.get("http://127.0.0.1:5500/Library-Project-main/frontend/index.html")
        
        # Wait for the login page to load
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys("ben")
        password_field.send_keys("123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for the main page to load
        time.sleep(2)

        # Add each game from the Excel file
        for game in games:
            try:
                # Wait for elements to be present and interactable
                title_field = wait.until(EC.element_to_be_clickable((By.ID, "game-title")))
                genre_field = driver.find_element(By.ID, "game-genre")
                price_field = driver.find_element(By.ID, "game-price")
                quantity_field = driver.find_element(By.ID, "game-quantity")

                # Clear fields before entering new data
                title_field.clear()
                genre_field.clear()
                price_field.clear()
                quantity_field.clear()

                # Enter game data
                title_field.send_keys(game["כותרת"])
                genre_field.send_keys(game["ז'אנר"])
                price_field.send_keys(str(game["מחיר"]))
                quantity_field.send_keys(str(game["כמות"]))

                # Click Add Game button
                add_button = driver.find_element(By.XPATH, "//button[text()='Add Game']")
                add_button.click()

                # Wait for the game to be added
                time.sleep(2)
                print(f"Successfully added game: {game['כותרת']}")

            except Exception as e:
                print(f"Error adding game {game.get('כותרת', 'Unknown')}: {e}")
                continue

        print("Finished processing all games!")
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    # Use raw string for file path to handle backslashes correctly
    file_path = r"C:\Users\pc\Documents\games.xlsx"  # Update to your actual file path
    games = read_games_from_excel(file_path)
    add_games_to_store(games)
