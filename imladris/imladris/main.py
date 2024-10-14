#!/usr/bin/python3
import sys

from file_support import FileSupport
from people import People
from schedule import Schedule


class Main:
    def __init__(self):
        super().__init__()
        self._people = People()
        self._schedule = Schedule()
        self._file_support = FileSupport()

    def work(self, src_file_name, people_file_name, schedule_file_name):
        rows = self._file_support.parse_csv(src_file_name)

        people = self._people.prepare_people_dict(rows)

        self._write_schedule(rows, people, schedule_file_name)

        self._write_participants(people, people_file_name)

    def _write_schedule(self, rows, people, schedule_file_name):
        schedule_json = self._schedule.prepare_schedule_json(rows, people)
        self._file_support.write_file(schedule_file_name, schedule_json)

    def _write_participants(self, people, people_file_name):
        people_json = self._people.prepare_people_json(people)
        self._file_support.write_file(people_file_name, people_json)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise Exception('Usage: %s source.csv participants.jsonp schedule.jsonp' % sys.argv[0])

    main = Main()

    main.work(sys.argv[1], sys.argv[2], sys.argv[3])
