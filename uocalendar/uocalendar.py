from uocalendar.uoparser import UOParser 
from uocalendar.ics_exporter import ICSExporter
import logging

class UOCalendar:
  ics_exporter = ICSExporter()

  def run(self, htm_file):
    # Initialize the parser and the exporter
    parser = UOParser(htm_file)

    courses = parser.get_courses_info()
    logging.info("Parsed courses")
    logging.debug(courses)
    # Generate ics file from course information
    file = self.ics_exporter.generate_ics(courses)
    logging.info("Generated ics file")
    return file

    
  
