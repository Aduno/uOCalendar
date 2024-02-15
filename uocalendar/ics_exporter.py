from ics import Calendar, Event
from uocalendar.model.course_section import CourseSection
from uocalendar.model.course import Course
from datetime import datetime
from dateutil.rrule import rrule, WEEKLY
import pytz


# This module will take the parsed information and export it to an .ics file
class ICSExporter:
  def __init__(self):
    self.day_mapping = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}
    self.cal = Calendar()
    self.eastern_tz = pytz.timezone('Canada/Eastern')


  def __get_all_dates(self, start_date, end_date, day):
    day_num = self.day_mapping[day]
    
    # Convert the start and end date to datetime object
    start_date = datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")

    # Generate all the dates within the range of the start and end date based on the day of the week
    dates = list(rrule(WEEKLY, dtstart=start_date, until=end_date, byweekday=day_num))
    return dates

  def format_date(self, date: datetime, time):
    # Take the date directly and converting it to the correct timezone then assign the time to it
    date = date.astimezone(self.eastern_tz)
    time = datetime.strptime(time, "%I:%M%p")
    date_time = date.replace(month=date.month, day=date.day, hour=time.hour, minute=time.minute)
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
          e = Event()
          e.name = course.class_name + " " + section.component
          e.description = "Instructor: " + section.instructor
          e.location = section.location
          e.begin = self.format_date(date, section.time.split(' - ')[0])
          e.end = self.format_date(date, section.time.split(' - ')[1]) 
          self.cal.events.add(e)
    return self.cal
  
