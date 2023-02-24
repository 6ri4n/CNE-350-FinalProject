# Raspberry Pi Hydration Reminder
#
# This is a Python script that will run on a Raspberry Pi and play a sound at regular intervals to remind the user to drink water and stay hydrated
#
# The script will require the user to:
# - configure a hydration reminder interval(this will be the interval for the hydration reminders)
# - configure a do not disturb interval (during this interval the hydration reminders will not be triggered)

import pygame
import datetime
import time

def setup_configuration():
    hydration_interval = input('\nenter time interval for hydration reminder (in minutes): ')
    # brief check for hydration_interval
    while int(hydration_interval) < 1:
        print('\ninvalid input, try again')
        hydration_interval = input('enter time interval for hydration reminder (in minutes): ')
    else:
        dnd_interval = input('\nenter do not disturb time interval (in this format, e.g. 7:00AM-10:25PM or 10:05PM-9:30AM): ')
        # brief check for dnd_interval
        while not ((':' in dnd_interval) and ('-' in dnd_interval) and (('PM' in dnd_interval) or ('AM' in dnd_interval))):
            print('\ninvalid input, try again')
            dnd_interval = input('enter do not disturb time interval (in this format, e.g. 7:00AM-10:25PM or 10:05PM-9:30AM): ')
        else:
            return int(hydration_interval), dnd_interval

def parse_dnd_interval(dnd_interval):
    # dnd interval e.g. 7:00AM-10:25PM
    dash_index = dnd_interval.index('-')

    # e.g. 7:00AM
    first_part = dnd_interval[0:dash_index]
    # e.g. AM
    first_part_time = first_part[len(first_part) - 2:]

    # e.g. 10:25PM
    second_part = dnd_interval[dash_index + 1:]
    # e.g. PM
    second_part_time = second_part[len(second_part) - 2:]

    first_hour = first_part[0:first_part.index(':')]
    first_min = first_part[first_part.index(':') + 1: first_part.index(first_part_time)]
    second_hour = second_part[0:second_part.index(':')]
    second_min = second_part[second_part.index(':') + 1: second_part.index(second_part_time)]

    return [[first_hour, first_min, first_part_time], [second_hour, second_min, second_part_time]]

def in_dnd_interval(parse_dnd):
    dnd_first_hour = parse_dnd[0][0]
    dnd_first_min = parse_dnd[0][1]
    dnd_first_time = parse_dnd[0][2]

    dnd_second_hour = parse_dnd[1][0]
    dnd_second_min = parse_dnd[1][1]
    dnd_second_time = parse_dnd[1][2]

    if int(dnd_first_min[0]) < 1:
        dnd_first_min = dnd_first_min[1]

    if int(dnd_second_min[0]) < 1:
        dnd_second_min = dnd_second_min[1]

    dnd_first_hour = int(parse_dnd[0][0])
    dnd_first_min = int(dnd_first_min)
    dnd_second_hour = int(parse_dnd[1][0])
    dnd_second_min = int(dnd_second_min)

    print('\n!! dnd interval:', dnd_first_hour, dnd_first_min, dnd_first_time, 'to', dnd_second_hour, dnd_second_min, dnd_second_time)

    if dnd_first_time == 'PM':
        dnd_first_hour += 12

    if dnd_second_time == 'PM':
        dnd_second_hour += 12

    now = datetime.datetime.now()
    nh = now.hour
    nm = now.minute

    if nh > 12:
        print('!! current time:', nh % 12, ':', nm, 'PM\n')
    else:
        print('!! current time:', nh, ':', nm, 'AM\n')

    if nh > dnd_first_hour and nh < dnd_second_hour:
        return True
    elif nh == dnd_first_hour and nh == dnd_second_hour:
        if nm < dnd_second_min:
            return True
        else:
            return False
    elif nh == dnd_first_hour:
        if nm < dnd_first_min:
            return False
        else:
            return True
    elif nh == dnd_second_hour:
        if nm < dnd_second_min:
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load('drink-water.mp3')

    hydration_interval, dnd_interval = setup_configuration()
    parse_dnd = parse_dnd_interval(dnd_interval)

    while True:
        if in_dnd_interval(parse_dnd):
            print('++ within the dnd interval')
            time.sleep(hydration_interval * 60)
        else:
            print('-- not within the dnd interval')
            pygame.mixer.music.play()
            time.sleep(5)
            pygame.mixer.music.stop()
            time.sleep((hydration_interval * 60) - 5)