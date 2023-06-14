from excel_writer import create_excel
from mail_data import send_mail
import sched
import time


def routine(scheduler):
    scheduler.enter(86400, 1, routine, (scheduler,))

    print("Creating excel file")
    create_excel()
    print("Sending email")
    try:
        send_mail()
    except Exception as e:
        print(e)
    print("Done, waiting until tomorrow")


def main():
    # runs the routine every 24 hours
    # the first one is run instantly
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, routine, (scheduler,))
    scheduler.run()


main()
