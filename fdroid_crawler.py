import math
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import extract_package_name, get_count, get_property_from_csv, transform_string, load_categories_from_csv, save_category_to_csv, save_app_info_to_csv


android_apps_csv_file = 'android_apps.csv'
categories_csv_file = 'android_apps_categories.csv'

apps_folder = "android_apks"

os.makedirs(apps_folder, exist_ok=True)

service = Service(executable_path="/usr/bin/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--remote-debugging-port=9222")
# options.add_experimental_option("detach", True)
# options.add_argument("--start-maximized")
# options.add_argument("--lang=en")
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
options.add_argument("--no-sandbox")

download_dir = f"/home/researchuser/dev/android-auto-scrapper/{apps_folder}"
options.add_experimental_option("prefs", {"download.default_directory":  download_dir})

driver = webdriver.Chrome(options=options, service=service)
# current_link = driver.current_url

def crawl_app_store():
    try:
        driver.get("https://f-droid.org/en/packages/")

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "h3"))
        )

        category_names = driver.find_elements(By.TAG_NAME, "h3")
        # categories_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Show all")

        downloaded_categories = load_categories_from_csv(categories_csv_file)

        # driver.back()
        # driver.current_url
        # driver.refresh()
        # driver.find(By.XPATH, "//*[contains(text(), 'Show all')]")

        for i in range(len(category_names)):
            category_names = driver.find_elements(By.TAG_NAME, "h3")
            category = category_names[i].text.strip()
            print(category)
            categories_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Show all")
            total_apps = get_count(categories_links[i].text)
            apps_per_page = 30
            total_pages = math.floor(total_apps / apps_per_page) + 1

            if category in ["Donate", "", "News", "Last Updated", "Latest Apps"]:
                continue

            if category in downloaded_categories:
                continue

            for page in range(1, total_pages + 1):

                category_url = f"https://f-droid.org/en/categories/{transform_string(category)}"

                if page > 1:
                    category_url = f"https://f-droid.org/en/categories/{transform_string(category)}/{page}"

                driver.get(category_url)

                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "post-link"))
                )

                current_page_apps = driver.find_elements(By.CLASS_NAME, "post-link")
                
                try:
                    for j in range(len(current_page_apps)):
                        current_page_links = driver.find_elements(By.CLASS_NAME, "post-link")
                        app_element = current_page_links[j]
                        app_link = app_element.get_attribute("href")

                        if 'index.html' not in app_link:
                            continue

                        app_element.click()

                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Download APK"))
                        )

                        android_app_link = get_property_from_csv(android_apps_csv_file, "link")

                        if app_link not in android_app_link:
                            title = driver.find_element(By.CLASS_NAME, "package-name").text
                            description = driver.find_element(By.CLASS_NAME, "package-summary").text
                            download_btn = driver.find_element(By.PARTIAL_LINK_TEXT, "Download APK")
                            download_url = download_btn.get_attribute("href")
                            issue_tracker = "N/A"
                            try:
                                issue_tracker = driver.find_element(By.LINK_TEXT, "Issue Tracker").get_attribute("href")
                            except Exception as ex:
                                print("link to issue tracker not available")
                            source_code = "N/A"
                            try:
                                source_code = driver.find_element(By.LINK_TEXT, "Source Code").get_attribute("href")
                            except Exception as ex:
                                print("link to source code not available")
                            metadata = driver.find_element(By.LINK_TEXT, "Build Metadata").get_attribute("href")

                            app_info = {
                                'title': title,
                                'description': description,
                                'package_name': extract_package_name(app_link),
                                'category': category,
                                'link': app_link,
                                'issue_tracker': issue_tracker,
                                'source_code': source_code,
                                'metadata': metadata,
                                'download_url': download_url,
                            }

                            print(app_info)
                            print()

                            # simulate download (click the button)
                            download_btn.click()
                            time.sleep(10)

                            save_app_info_to_csv(android_apps_csv_file, app_info)

                            # if len(android_app_link) == 6:
                            #     break # back to previous page (i.e. category apps page)
                            # else:
                            # driver.back()
                            # WebDriverWait(driver, 10).until(
                            #     EC.presence_of_all_elements_located((By.CLASS_NAME, "post-link"))
                            # )
                        # else:
                        driver.back()
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "post-link"))
                        )
                except Exception as e:
                    print(f"An error occurred: {e}")

            downloaded_categories.add(category)
            save_category_to_csv(categories_csv_file, downloaded_categories)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # close the browser
        driver.quit()


start_time = time.time()
crawl_app_store()
end_time = time.time()

print(f"Total time taken: {end_time - start_time} seconds")