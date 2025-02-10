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
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found at: {file_path}")
            
        df = pd.read_excel(file_path)
        
        # Strip column names to remove extra spaces
        df.columns = df.columns.str.strip()

        print("Columns in the Excel file:", df.columns)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def add_games_to_store(games):
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("file:///C:/Users/pc/Game-Project-Store/Library-Project-main/frontend/index.html")
        
        # Wait for the login page to load
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys("asik")
        password_field.send_keys("123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(2)  # Wait for login to process

        # Handle unexpected login alert
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"Login Alert: {alert.text}")
            alert.accept()  # Close the alert
            print("Login failed. Please check credentials.")
            return
        except:
            print("Login successful!")

        # Wait for main page to load
        time.sleep(2)

        # Wait for game input fields
        title_field = wait.until(EC.element_to_be_clickable((By.ID, "game-title")))
        genre_field = driver.find_element(By.ID, "game-genre")
        price_field = driver.find_element(By.ID, "game-price")
        quantity_field = driver.find_element(By.ID, "game-quantity")
        add_button = driver.find_element(By.XPATH, "//button[text()='Add Game']")

        # Add each game from the Excel file
        for index, game in games.iterrows():
            try:
                # Clear fields
                title_field.clear()
                genre_field.clear()
                price_field.clear()
                quantity_field.clear()

                # Enter game data
                title_field.send_keys(game["Title"])
                genre_field.send_keys(game["Genre"])
                price_field.send_keys(str(game["Price"]))
                quantity_field.send_keys(str(game["Quantity"]))

                # Click Add Game button
                add_button.click()

                time.sleep(2)  # Wait for game to be added
                print(f"Successfully added game: {game['Title']}")

            except Exception as e:
                print(f"Error adding game {game.get('Title', 'Unknown')}: {e}")
                continue

        print("Finished processing all games!")
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = r"C:/Users/pc/Documents/games.xlsx"
    games = read_games_from_excel(file_path)
    
    if games is not None and not games.empty:
        add_games_to_store(games)
    else:
        print("No games data found.")
