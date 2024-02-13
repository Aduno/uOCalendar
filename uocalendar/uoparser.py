from bs4 import BeautifulSoup
from model.course_data import CourseData

class UOParser:
  def __init__(self, html):
    self.soup = BeautifulSoup(html, 'html.parser')

  def find_by_id(self, id):
    return self.soup.find_all(id=id)
  
  def find_by_class(self, class_name):
    return self.soup.find_all(class_=class_name)

  def find_table_by_class(self, class_name):
    return self.soup.find_all('table', class_=class_name)
    
  def parse_table(self, table):
    course_data = CourseData()
    self.__parse_class_title(table, course_data)
    self.__parse_class_data(table, course_data)

    return course_data

  def __parse_class_title(self, table, course_data):
    course_title = table.find('td', class_='PAGROUPDIVIDER').text
    course_data.class_name = course_title.split(' - ')[0]
    course_data.class_code = course_title.split(' - ')[1]
  
  def __parse_class_data(self, table, course_data):
    # Go row by row collecting class type, time, and location and professor
    course_table = table.find('table', attrs={"class":"PSLEVEL3GRID", "cols": "7"})
    rows = course_table.find_all('tr')

    component = None
    for row in rows[1:]:
      cells = row.find_all('td')

      # If the component cell is empty, it is a continuation of the previous row
      if(cells[2]!=None):
        component = cells[2].text

      # Fill in the component, days & time, location, instructor, start and end date
      for cell in cells[2:]:
        print(cell)
      break

      # if len(cells) > 0:
      #   class_type = cells[0].text
      #   time = cells[1].text
    pass