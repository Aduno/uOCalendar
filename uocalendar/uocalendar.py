from uoparser import UOParser 
from ics_exporter import ICSExporter

if __name__ == '__main__':
  with open('test\My Class Schedule_files\SA_LEARNER_SERVICES.htm') as file:
    html = file.read()
  parser = UOParser(html)
  courses = list()
  ics_exporter = ICSExporter()
  # Selecting only relavent part of the soup to make it easier to work with and to reduce the amount of data to process
  parser.soup = parser.soup.select('table[id*="ACE_STDNT_ENRL"]')[0]
  tables = parser.find_table_by_class('PSGROUPBOXWBO')

  for table in tables:
    courses.append(parser.parse_table(table))
  
  # Generate ics file from course information
  file = ics_exporter.generate_ics(courses)
  with open('out.ics', 'w') as my_file:
    my_file.writelines(file.serialize_iter())
  
