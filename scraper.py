from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def get_apartments(city_url="https://www.apartments.com/charlottesville-va/"):
    # === Setup Chrome in non-headless mode (for debugging) ===
    options = Options()
    # Uncomment for background scraping once stable
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"❌ Chrome driver setup failed: {e}")
        return pd.DataFrame()

    print(f"🔍 Scraping: {city_url}")
    driver.get(city_url)
    try:
        print("⏳ Waiting for listings to load...")
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.mortar-wrapper"))
        )
    except:
        print("❌ Listings did not load in time.")
        driver.quit()
        return pd.DataFrame()

    # ✅ Scroll to load more listings
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    listings = driver.find_elements(By.CSS_SELECTOR, "li.mortar-wrapper")
    print(f"✅ Found {len(listings)} listings")

    results = []

    for idx, listing in enumerate(listings):
        try:
            if "Sponsored" in listing.text:
                print(f"Skipping sponsored listing #{idx+1}")
                continue

            full_info = listing.text
            lines = full_info.split("\n")

            # Extract key details
            try:
                title = listing.find_element(By.CSS_SELECTOR, "span.title").text
            except:
                title = lines[0] if lines else "N/A"

            try:
                address = listing.find_element(By.CLASS_NAME, "property-address").text
            except:
                address = "N/A"

            price = next((l for l in lines if "$" in l), "N/A")
            beds = next((l for l in lines if "Bed" in l or "Studio" in l), "N/A")

            try:
                link = listing.find_element(By.CSS_SELECTOR, "a.property-link").get_attribute("href")
            except:
                link = "N/A"

            results.append({
                "title": title,
                "address": address,
                "price": price,
                "beds": beds,
                "link": link
            })

        except Exception as e:
            print(f"⚠️ Skipping listing #{idx+1} due to error: {e}")
            continue

    driver.quit()
    return pd.DataFrame(results)

# ✅ Test directly if needed
if __name__ == "__main__":
    df = get_apartments()
    print("\n📊 Final Listings:")
    print(df.head())