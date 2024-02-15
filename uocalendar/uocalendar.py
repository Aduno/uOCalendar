from uocalendar.uoparser import UOParser 
from uocalendar.ics_exporter import ICSExporter
import logging

class UOCalendar:

  def run(self, htm_file):
    # Initialize the parser and the exporter
    parser = UOParser(htm_file)
    ics_exporter = ICSExporter()

    courses = parser.get_courses_info()
    logging.info("Parsed courses")
    logging.debug(courses)
    # Generate ics file from course information
    file: Calendar = ics_exporter.generate_ics(courses)
    logging.info("Generated ics file")
    return file
    # with open('My Schedule.ics', 'w') as my_file:
    #   my_file.writelines(file.serialize_iter())
    
  
