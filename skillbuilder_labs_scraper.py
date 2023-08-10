import time
import re
import xlsxwriter
import traceback
# from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()

def get_number(path):
  """Gets the number from the path."""
  match = re.search(r"\d+", path)
  if match:
    return int(match.group(0))
  else:
    return None

def create_excel_sheet(filename, sheet_name, data):
    """Creates an Excel sheet."""
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(sheet_name)
    for row_index, row_data in enumerate(data):
      for column_index, column_data in enumerate(row_data):
        worksheet.write(row_index, column_index, column_data)

def crawl_lab_grids():
    url = "https://explore.skillbuilder.aws/learn/public/catalog/view/15?ctldoc-catalog-0=l-_en"
    driver.get(url)
    time.sleep(5)
    count = driver.find_element(By.CLASS_NAME, 'course-catalog-total-count').text
    count = get_number(count) or 0
    all_labs = []
    total_labs = 0
    lab_links = []
    while len(lab_links) < count:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        all_labs = driver.find_elements(By.CLASS_NAME, "ui-card-title")
        lab_links = [lab.find_element(By.TAG_NAME, "a").get_attribute("href") for lab in all_labs]

    print(f"Total Count: {count}, Total Found: {len(lab_links)}")
    return lab_links

def crawl_single_page(link):
    driver.get(link)
    time.sleep(5)
    title = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/doc-layout/div/main/div/ng-component/div/course-content/div/div/div/div[1]/div[1]/div[2]/div/div[1]/h1").text
    duration = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/doc-layout/div/main/div/ng-component/div/course-content/div/div/div/div[1]/div[1]/div[2]/div/div[2]/ul/li[2]/p").text
    duration = duration.replace("Duration:", '')
    description = driver.find_element(By.ID, "panel-0").text
    print(title, duration, description)
    # lab_data.append(title, duration, description, link)

def main():
    lab_links = crawl_lab_grids()

    labs_data = [['Title', 'Duration', 'Description', 'Link'],]
    for index, link in enumerate(lab_links):
        print(f"Getting link for {index+1} of {len(lab_links)}")
        print(index + 1, ": ", link)
        crawl_single_page(link)
        print(f"Link {index + 1} of {len(lab_links)}: Completed")
    create_excel_sheet("AWSSkillBuilder_Labs.xlsx", "Sheet1", labs_data)
    
    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    main()