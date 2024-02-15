from uoparser import UOParser 
from ics_exporter import ICSExporter

if __name__ == '__main__':
  input_file_path = 'test\My Class Schedule_files\SA_LEARNER_SERVICES.htm'
  output_file_name = 'My Schedule.ics'
  with open(input_file_path) as file:
    html = file.read()
  
  # Initialize the parser and the exporter
  parser = UOParser(html)
  ics_exporter = ICSExporter()

  courses = parser.get_courses_info()
  
  # Generate ics file from course information
  file = ics_exporter.generate_ics(courses)
  with open(output_file_name, 'w') as my_file:
    my_file.writelines(file.serialize_iter())
  
