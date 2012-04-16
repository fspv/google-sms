#!/usr/bin/python2
# -*- coding: utf-8 -*-
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import time
version = "0.01"
config = {  'email':'mail@example.com',
            'password':'passwd',
            'calendar':'default',
            'title':'Title of your event here',
            'location':'Location of your event here'
}
def usage():
    """Prints right usage for this script"""
    print("Usage: "+sys.argv[0]+" [-t title] [-l location] [-e email] [-p password]\n\r\
    -e  --email=EMAIL           set your email for Google account\n\r\
    -p  --password=PASSWORD     set password for your Google account\n\r\
    -t  --title=TITLE           set title of event\n\r\
    -l  --location=LOCATION     set location of event\n\r\
    -c  --calendar=CALENDAR     set calendar name (default if not specifyed\n\r\
    -h  --help                  display this help and exit\n\r\
    -v  --version               display script version and exit")
class SMS():
    def __init__(self,email,password,title,location,calendar):
        """Connect to Google Calendar"""
        self.title = title
        self.location = location
        self.calendar_title = calendar
        self.calendar_link = "http://www.google.com/calendar/feeds/default/private/full"
        self.calendar_service = gdata.calendar.service.CalendarService()
        self.calendar_service.email = email
        self.calendar_service.password = password
        try:
            self.calendar_service.ProgrammaticLogin()
        except gdata.service.BadAuthentication as BadAuth:
            print(BadAuth)
            sys.exit(2)
        except gdata.service.CaptchaRequired as Captcha:
            print(Captcha)
            sys.exit(2)
        except:
            raise
        self.feed = self.calendar_service.GetOwnCalendarsFeed()
        for a_calendar in self.feed.entry:
            if self.calendar_title == a_calendar.title.text:
                self.calendar_link = a_calendar.link[0].href
    def send(self):
        """Add new event and set SMS-reminder"""
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=self.title)
        event.content = atom.Content(text='')
        event.where.append(gdata.calendar.Where(value_string=self.location))
        # Set start time in 6 minutes
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 6*60))
        # Set end time in an hour
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
        minutes=5
        for a_when in event.when:
            if len(a_when.reminder) > 0:
                # Adding reminder in 5 minutes before event (start_time)
                a_when.reminder[0].minutes = 5
            else:
                a_when.reminder.append(gdata.calendar.Reminder(minutes=minutes))
        # Insert new event
        new_event = self.calendar_service.InsertEvent(event, self.calendar_link)
        return new_event
def usage():
    """Prints right usage for this script"""
    print("Usage: "+sys.argv[0]+" [-t title] [-l location] [-e email] [-p password]\n\r\
    -e  --email=EMAIL           set your email for Google account\n\r\
    -p  --password=PASSWORD     set password for your Google account\n\r\
    -t  --title=TITLE           set title of event\n\r\
    -l  --location=LOCATION     set location of event\n\r\
    -c  --calendar=CALENDAR     set calendar name to which you want to add event\n\r\
    -h  --help                  display this help and exit\n\r\
    -v  --version               display script version and exit")
def main():
    """Check args, setting values and try to send SMS"""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hve:p:t:l:c:", ["help", "email=", "password=", "title=","location=","calendar="])
    except getopt.GetoptError as err:
        """ print help information and exit """
        print(err)
        usage()
        sys.exit(2)
    email = config['email']
    password = config['password']
    title = config['title']
    location = config['location']
    calendar = config['calendar']
    for o,a in opts:
        if o == "-v":
            print("Python script for sending free SMS via Google Calendar v"+version)
            sys.exit()
        elif o in ("-h","--help"):
            usage()
            sys.exit()
        elif o in ("-e","--email"):
            email = a
        elif o in ("-p","--password"):
            password = a
        elif o in ("-t","--title"):
            title = a
        elif o in ("-l","--location"):
            location = a
        elif o in ("-c","--calendar"):
            calendar = a
    try:
        sms = SMS(email,password,title,location,calendar)
    except:
        raise
    else:
        try:
            sms.send()
        except:
            raise
if __name__ == "__main__":
    main()
