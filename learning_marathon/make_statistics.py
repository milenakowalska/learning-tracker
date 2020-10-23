from .models import User, LearningSession
from datetime import datetime, date, timedelta


def day_summary(user, date, theory: bool):
    entries = LearningSession.objects.filter(user=user, theory=theory)
    day_complete = timedelta(seconds=0)

    for entry in entries:
        if entry.start_date.day == date.day and entry.start_date.month == date.month and entry.start_date.year == date.year:
            day_complete += entry.duration()
    summary = day_complete - timedelta(microseconds=day_complete.microseconds)
    if summary:
        return summary
    else:
        return timedelta(seconds=0)

def new_data(date, user):

    day_entry = {
        'day':date.isoformat(),
        'theory': day_summary(user, date, True),
        'practice':day_summary(user, date, False),
        'rewards': day_summary(user, date, False).seconds//3600,
        'rewards_practice': day_summary(user, date, False).seconds//3600
    }
    return day_entry

def get_data(start_date, user):
    current_data = []

    theory_summary = timedelta(seconds=0)
    practice_summary = timedelta(seconds=0)

    end_date = date.today()
    time_range = end_date - start_date
    print(time_range.days)
    date_list = [(date.today()) - timedelta(days=x) for x in range(time_range.days )]

    for day in date_list:
        day_data = new_data(day, user)
        current_data.append(day_data)

        theory_summary += day_data['theory']
        practice_summary += day_data['practice']
    
    summary_entry = {
        'theory_summary' : theory_summary,
        'practice_summary' : practice_summary
    }
    current_data.append(summary_entry)
    
    return current_data