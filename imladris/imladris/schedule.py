import json
import string
from builtins import enumerate

HOST = 'moderator'
CO_HOST = 'współprowadzący'
CURRENT_YEAR = 2022


class Schedule:
    def __init__(self):
        super().__init__()

    def prepare_schedule_json(self, rows, people):
        json_data = []

        for row in rows:
            json_data.append(self._to_konopas_schedule_item(row, people))

        return json.dumps(json_data, indent=2, ensure_ascii=False)

    def _to_konopas_schedule_item(self, row, people):
        return {
            "id": row['id'],
            "title": ' '.join((row['kind'], row['title'])),
            "tags": self._make_tags(row),
            "date": self._make_date(row),
            "time": row['start_time'],
            "mins": self._make_duration(row),
            "loc": [row['place']],
            "people": self._make_people(row, people),
            "desc": row['description'],
            "links": []
        }

    def _make_tags(self, row):
        return [row['category']] if row['category'] else []

    def _make_date(self, row):
        if not row['date']:
            return ''

        stripped = row['date'].rstrip(string.punctuation)

        day, month = stripped.split('.')

        return '%s-%s-%s' % (CURRENT_YEAR, month, day)

    def _make_duration(self, row):
        return row['duration'].replace('minut', '').strip()

    def _make_people(self, row, people):
        participants = []

        for i, host in enumerate(row['hosts']):
            role = HOST if i == 0 else CO_HOST

            participants.append({
                'id': people[host['display_name']]['id'],
                'name': host['display_name'].replace('  ', ' ').strip(),
                'sortname': host['sortname'].replace('  ', ' ').strip(),
                'role': role
            })

        return participants
