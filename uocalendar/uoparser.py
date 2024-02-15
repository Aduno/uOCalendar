from bs4 import BeautifulSoup
from model.course import Course
from model.course_section import CourseSection
class UOParser:
  def __init__(self, html):
    self.soup = BeautifulSoup(html, 'html.parser')
    # Selecting only relavent part of the soup to make it easier to work with and to reduce the amount of data to process
    self.soup = self.soup.select('table[id*="ACE_STDNT_ENRL"]')[0]

  def find_by_id(self, id):
    return self.soup.find_all(id=id)
  
  def find_by_class(self, class_name):
    return self.soup.find_all(class_=class_name)

  def find_table_by_class(self, class_name):
    return self.soup.find_all('table', class_=class_name)
  
  def parse_table(self, table):
    course = Course()
    course_title = table.find('td', class_='PAGROUPDIVIDER').text
    course_data = table.find('table', attrs={"class":"PSLEVEL3GRID", "cols": "7"})
    self.__parse_class_name(course_title, course)
    self.__parse_class_data(course_data, course)
    return course

  
  def __parse_class_name(self, course_title, course):
    course.class_name = course_title.split(' - ')[0]
    course.class_code = course_title.split(' - ')[1]

  def __parse_class_data(self, course_data, course):
    # Go row by row collecting class type, time, and location and professor
    rows = course_data.find_all('tr')
    component = None
    for row in rows[1:]:
      cells = row.find_all('td')
      course_section = CourseSection()
      for i, cell in enumerate(cells):
        item = cell.find('span').text if cell.find('span') else None
        # Skip the first two cells (Class Number and Section code)  
        match i:
          case 2:
            if(item != None and item != '\xa0'):
              component = item
            course_section.component = component
          case 3:
            try: 
              course_section.day = item.split(' ', 1)[0]
              course_section.time = item.split(' ', 1)[1]
            except:
              course_section.day = "N/A"
              course_section.time = "N/A"
          case 4:
            course_section.location = item
          case 5:
            course_section.instructor = item
          case 6: 
            course_section.start_date = item.split(' - ')[0]
            course_section.end_date = item.split(' - ')[1]
          case _:
            continue
      course.class_data.append(course_section)

def get_courses_info(self):
  tables = self.find_table_by_class('PSGROUPBOXWBO')
  courses = list()
  for table in tables:
    courses.append(self.parse_table(table))