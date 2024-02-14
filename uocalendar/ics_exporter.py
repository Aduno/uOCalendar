from ics import Calendar, Event
from model.course_section import CourseSection
from model.course import Course
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil.rrule import rrule, WEEKLY
import pytz


# This module will take the parsed information and export it to an .ics file
class ICSExporter:
  def __init__(self):
    self.day_mapping = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}
    self.cal = Calendar()

  def __get_all_dates(self, start_date, end_date, day):
    day_num = self.day_mapping[day]
    
    # Convert the start and end date to datetime object
    start_date = datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")

    # Generate all the dates within the range of the start and end date based on the day of the week
    dates = list(rrule(WEEKLY, dtstart=start_date, until=end_date, byweekday=day_num))

    # Convert the dates to string
    dates = [date.strftime("%Y-%m-%d") for date in dates]

    return dates
  def __convert24(self, time):
    # Parse the time string into a datetime object
    t = datetime.strptime(time, '%I:%M%p')
    print("$$$$$$$$$$")
    print(t.isoformat())
    # Give the time object the timezone offset of eastern time
    # Format the datetime object into a 24-hour time string
    return t.strftime('%H:%M:%S')
  def format_date(self, date, time):
    # Convert the time string into a 24-hour time string
    date_time = datetime.strptime(date + time, '%Y-%m-%d%I:%M%p')
    print(date_time.isoformat())

    # there is still some bugs with this. Fix it later
    return date_time
  def generate_ics(self, courses):
    course: Course
    for course in courses:
      section : CourseSection
      for section in course.class_data:
        if section.day == "N/A":
          continue
        section_dates = self.__get_all_dates(section.start_date, section.end_date, section.day)
        for date in section_dates:
          print(date)
          e = Event()
          e.name = course.class_name + " " + section.component
          # Make this into its own function 
          e.begin = self.format_date(date, section.time.split(' - ')[0])
          e.end = self.format_date(date, section.time.split(' - ')[1])
          e.description = "Instructor: " + section.instructor
          e.location = section.location
          self.cal.events.add(e)
    return self.cal
  
