from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_nfl_stats():
    try:
        options = Options() #Options are customizable Selenium features windowsize, display, etc. 
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Navigate to NFL stats page
        url = "https://www.nfl.com/stats/player-stats/category/receiving/2025/reg/all/receivingreceptions/desc"
        driver.get(url)
        time.sleep(3)  # Wait for initial page load
        
        # Click "Load More" button until all data is loaded
        max_clicks = 20  # Prevent infinite loops
        clicks = 0
        while clicks < max_clicks:
            try:
                load_more = driver.find_element(By.CSS_SELECTOR, "button.d3-o-load-more")
                load_more.click()
                time.sleep(2)
                clicks += 1
            except NoSuchElementException:
                # Button not found, try scrolling
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break  # No more content to load
        
        # Scrape the data
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        data = []
        columns = [
            "Receptions", "Yards", "Touchdowns", "20+ Yards", "40+ Yards",
            "Long", "Rec 1st", "1st %", "Rec Fum", "Rec YAC/R", "Tgts"
        ]
        
        for row in rows:
            try:
                name_el = row.find_element(By.CLASS_NAME, "d3-o-player-fullname")
                name = name_el.text.strip()
                
                cells = row.find_elements(By.TAG_NAME, "td")
                stats = [c.text.strip() for c in cells[1:] if c.text.strip() != ""]
                
                player_data = {"Name": name}
                for col, val in zip(columns, stats):
                    player_data[col] = val
                
                data.append(player_data)
            except Exception as e:
                continue
        
        driver.quit()
        
        return {
            "success": True,
            "data": data,
            "total_players": len(data)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": []
        }
