from uoparser import UOParser 

if __name__ == '__main__':
  with open('test\My Class Schedule_files\SA_LEARNER_SERVICES.htm') as file:
    html = file.read()
  parser = UOParser(html)

  # Selecting only relavent part of the soup to make it easier to work with and to reduce the amount of data to process
  parser.soup = parser.soup.select('table[id*="ACE_STDNT_ENRL"]')[0]

  tables = parser.find_table_by_class('PSGROUPBOXWBO')
  courses = list()

  for table in tables:
    courses.append(parser.parse_table(table))
    
  print(courses)
