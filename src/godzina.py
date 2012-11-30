#!/usr/bin/python

"""
Python module that tells you the time in Polish in both official (24hr) and unofficial (12hr)
formats. Also, tells you how to say something happened *at* that time.
"""

__author__ = 'Matthew Hasler (matthew@ganzogo.com)'
__copyright__ = '2012 Ganzogo Limited'

import re
import sys

TIME_PATTERN = '^(\d{1,2})\:(\d{2})$'

def load_numbers(filename):
  number_dict = {}
  number = 0
  f = open(filename, 'r')
  for line in f.readlines():
    number_dict[number] = line.rstrip().decode('UTF-8')
    number += 1
  f.close()
  return number_dict

OFFICIAL_HOURS_A = load_numbers('official_hours_a.txt')
OFFICIAL_HOURS_EJ = load_numbers('official_hours_ej.txt')
UNOFFICIAL_HOURS_A = load_numbers('unofficial_hours_a.txt')
UNOFFICIAL_HOURS_EJ = load_numbers('unofficial_hours_ej.txt')
MINUTES = load_numbers('minutes.txt')
QUARTER = u'kwadrans'
HALF = u'wp\xf3\u0142'

def print_usage():
  print 'USAGE:'
  print '\tpython %s HH:MM' % sys.argv[0]
  sys.exit()

def oficjalnie_jest(hours, minutes):
  """Returns the official time in words based on the given values for hours and minutes.

  >>> oficjalnie_jest(21, 0)
  u'jest dwudziesta pierwsza'
  >>> oficjalnie_jest(7, 15)
  u'jest si\\xf3dma pietna\u015bcie'
  >>> oficjalnie_jest(16, 20)
  u'jest szesnasta dwadzie\u015bcia'
  >>> oficjalnie_jest(8, 30)
  u'jest \\xf3sma trzydzie\u015bci'
  >>> oficjalnie_jest(22, 30)
  u'jest dzudziesta druga trzydzie\u015bci'
  >>> oficjalnie_jest(17, 55)
  u'jest siedemnasta pi\u0119dzie\u015b\u0105t pi\u0119\u0107'
  """
  if minutes == 0:
    return 'jest %s' % OFFICIAL_HOURS_A[hours]
  else:
    return 'jest %s %s' % (OFFICIAL_HOURS_A[hours], MINUTES[minutes])

def nieoficjalnie_jest(hours, minutes):
  """Returns the unofficial time in words based on the given values for hours and minutes.

  >>> nieoficjalnie_jest(21, 0)
  u'jest dziewi\u0105ta'
  >>> nieoficjalnie_jest(7, 15)
  u'jest kwadrans po si\\xf3dmej'
  >>> nieoficjalnie_jest(16, 20)
  u'jest dwadzie\u015bcia po czwartej'
  >>> nieoficjalnie_jest(8, 30)
  u'jest wp\\xf3\u0142 do dziewi\u0105tej'
  >>> nieoficjalnie_jest(22, 30)
  u'jest wp\\xf3\u0142 do jedenastej'
  >>> nieoficjalnie_jest(17, 55)
  u'jest za pi\u0119\u0107 sz\\xf3sta'
  """
  next_hour = (hours + 1) % 24
  if minutes == 0:
    return 'jest %s' % UNOFFICIAL_HOURS_A[hours]
  elif minutes == 15:
    return 'jest %s po %s' % (QUARTER, UNOFFICIAL_HOURS_EJ[hours])
  elif minutes == 30:
    return 'jest %s do %s' % (HALF, UNOFFICIAL_HOURS_EJ[next_hour])
  elif minutes == 45:
    return 'jest za %s %s' % (QUARTER, UNOFFICIAL_HOURS_A[next_hour])
  elif minutes < 30:
    return 'jest %s po %s' % (MINUTES[minutes], UNOFFICIAL_HOURS_EJ[hours])
  else:
    return 'jest za %s %s' % (MINUTES[60 - minutes], UNOFFICIAL_HOURS_A[next_hour])

def oficjalnie_o(hours, minutes):
  """Returns the official way to say that something happened at the given time.

  >>> oficjalnie_o(13, 0)
  u'o trzynastej'
  >>> oficjalnie_o(13, 15)
  u'o trzynastej pietna\u015bcie'
  >>> oficjalnie_o(13, 30)
  u'o trzynastej trzydzie\u015bci'
  >>> oficjalnie_o(13, 45)
  u'o trzynastej czterdzie\u015bci pi\u0119\u0107'
  >>> oficjalnie_o(14, 0)
  u'o czternastej'
  """ 
  if minutes == 0:
    return 'o %s' % OFFICIAL_HOURS_EJ[hours]
  else:
    return 'o %s %s' % (OFFICIAL_HOURS_EJ[hours], MINUTES[minutes])

def nieoficjalnie_o(hours, minutes):
  """Returns the unofficial way to say that something happened at the given time.

  >>> nieoficjalnie_o(13, 0)
  u'o pierwszej'
  >>> nieoficjalnie_o(13, 15)
  u'kwadrans po pierwszej'
  >>> nieoficjalnie_o(13, 30)
  u'o wp\\xf3\u0142 do drugiej'
  >>> nieoficjalnie_o(13, 45)
  u'za kwadrans druga'
  >>> nieoficjalnie_o(14, 0)
  u'o drugiej'
  """
  next_hour = (hours + 1) % 24
  if minutes == 0:
    return 'o %s' % UNOFFICIAL_HOURS_EJ[hours]
  elif minutes == 15:
    return '%s po %s' % (QUARTER, UNOFFICIAL_HOURS_EJ[hours])
  elif minutes == 30:
    return 'o %s do %s' % (HALF, UNOFFICIAL_HOURS_EJ[next_hour])
  elif minutes == 45:
    return 'za %s %s' % (QUARTER, UNOFFICIAL_HOURS_A[next_hour])
  elif minutes < 30:
    return '%s po %s' % (MINUTES[minutes], UNOFFICIAL_HOURS_EJ[hours])
  else:
    return 'za %s %s' % (MINUTES[60 - minutes], UNOFFICIAL_HOURS_A[next_hour])

def main():
  if len(sys.argv) == 2:

    match = re.match(TIME_PATTERN, sys.argv[1])
    if match is None:
      print_usage()

    hours = int(match.groups()[0])
    minutes = int(match.groups()[1])

    if hours < 0 or hours > 23:
      print_usage()

    if minutes < 0 or minutes > 59:
      print_usage()

    print '%02d:%02d' % (hours, minutes)
    print 'oficjalnie: %s, %s' % (oficjalnie_jest(hours, minutes), oficjalnie_o(hours, minutes))
    print 'nieoficjalnie: %s, %s' % (nieoficjalnie_jest(hours, minutes), nieoficjalnie_o(hours, minutes))

  else:
    print_usage()

if __name__ == '__main__':
  main()
