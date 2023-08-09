import time
import re
import xlsxwriter
# from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By

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

def main():
    url = "https://explore.skillbuilder.aws/learn/public/catalog/view/15?ctldoc-catalog-0=l-_en"
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(5)
    count = driver.find_element(By.CLASS_NAME, 'course-catalog-total-count').text
    count = get_number(count) or 0
    all_labs = []
    total_labs = 0
    while total_labs < count:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        all_labs = driver.find_elements(By.CLASS_NAME, "ui-card-title")
        total_labs = len(all_labs)
        # get all card elements and count

    lab_links = List()
    for lab_title in all_labs:
        title = lab_title.find_element(By.TAG_NAME, "a")
        print(title.get_attribute("href"))
        lab_links = lab_links.append(title.get_attribute("href"))

    labs_data = [['Title', 'Duration', 'Description', 'Link'],]
    for link in lab_links:
        # if link.startswith("/"):
        #     link = parse.urljoin(driver.curre)
        driver.get(link)
        time.sleep(5)
        course_head = driver.find_element_by_class_name("course-head-content") 
        title = course_head.find_element_by_class_name("title")
        course_info = course_head.find_element_by_class_name("course-info")
        duration = course_info.find_element(By.TAG_NAME, "*")[0].text.replace("Duration:", '')
        description = driver.find_element_by_class_name("tabs-description").text
        lab_data.append(title, duration, description, link)
        # addtional_info_tab = driver.find_element(By.XPath, "/html/body/div[2]/div/div/div/doc-layout/div/main/div/ng-component/div/course-content/div/div/div/div[1]/div[2]/tabs/div/div/header/div/div[1]/div[3]/a")
        

    create_excel_sheet("AWSSkillBuilder_Labs.xlsx", "Sheet1", labs_data)

    time.sleep(10)
    driver.find_element(By.CLASS_NAME, 'ui-card-duration')
    time.sleep(10)
    driver.quit()


    course_info = driver.find_element(By.CLASS_NAME('course-info'))
    duration = course_info.find_elements_by_tag_name("*")[1]


if __name__ == '__main__':
    main()