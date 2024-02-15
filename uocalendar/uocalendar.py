from uocalendar.uoparser import UOParser 
from uocalendar.ics_exporter import ICSExporter

class UOCalendar:

  def run(self, htm_file):
    with open(htm_file) as file:
      html = file.read()
    
    # Initialize the parser and the exporter
    parser = UOParser(html)
    ics_exporter = ICSExporter()

    courses = parser.get_courses_info()
    
    # Generate ics file from course information
    file = ics_exporter.generate_ics(courses)
    return file.serialize()
    # with open('My Schedule.ics', 'w') as my_file:
    #   my_file.writelines(file.serialize_iter())
    
  
