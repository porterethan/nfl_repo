from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
options.add_argument("--headless=new")   # run in background
options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.nfl.com/stats/player-stats/category/receiving/2025/reg/all/receivingreceptions/desc"
driver.get(url)

while True:
    try:
        load_more = driver.find_element(By.CSS_SELECTOR, "button.d3-o-load-more")
        load_more.click()
        time.sleep(2)
    except NoSuchElementException:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

data = [] 
columns = [
    "Receptions", "Yards", "Touchdowns", "20+ Yards", "40+ Yards", 
    "Long", "Rec 1", "1st %", "Rec Fum", "Rec YAC/R", "Tgts"
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
    except Exception:
        continue

driver.quit()

df = pd.DataFrame(data)

print(df)
print(f"\nTotal players scraped: {len(df)}")
