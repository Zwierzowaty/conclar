import csv

FIELDS = [
    'date',
    'start_time',
    'end_time',
    'place',
    'id',
    'surname',
    'firstname',
    'nickname',
    'display_name',
    'sortname',
    'sortname_short',
    'title',
    'src_co_hosts',
    'kind',
    'category',
    'description',
    'duration'
]

ROW_SIZE = len(FIELDS)


class FileSupport:
    def __init__(self):
        super().__init__()

    def parse_csv(self, src_file_name):
        data = []

        raw_data = self._read_csv(src_file_name)

        keys = sorted(raw_data.keys())

        for key in keys:
            items = raw_data[key]

            data.append(self._prepare_single_prog_position(items))

        return data

    def write_file(self, file_name, text_json):
        with open(file_name, 'w') as file:
            file.writelines(text_json)

    def _read_csv(self, src_file_name):
        data = {}

        with open(src_file_name, newline='\r\n') as csv_file:
            csv_reader = csv.reader(csv_file)

            for line_no, row in enumerate(csv_reader):
                if line_no == 0:
                    continue

                parsed_row = self._parse_single_row(line_no, row)

                if parsed_row['id'] not in data:
                    data[parsed_row['id']] = []

                data[parsed_row['id']].append(parsed_row)

        return data

    def _prepare_single_prog_position(self, items):
        first_item = items[0]

        hosts_present = set()
        hosts = []

        for i, item in enumerate(items):
            display_name = item['display_name'].strip()

            if display_name not in hosts_present:
                hosts_present.add(display_name)

                hosts.append({
                    'display_name': display_name,
                    'sortname': item['sortname'].strip()
                })

        item = {
            'date': first_item['date'],
            'start_time': first_item['start_time'],
            'end_time': first_item['end_time'],
            'place': first_item['place'],
            'id': first_item['id'],
            'hosts': hosts,
            'title': first_item['title'],
            'kind': first_item['kind'],
            'category': first_item['category'],
            'description': first_item['description'],
            'duration': first_item['duration']
        }

        return item

    def _parse_single_row(self, line_no, row):
        if len(row) != ROW_SIZE:
            raise Exception('Row should have %s items, was: %s, line no: %s' % (
                ROW_SIZE,
                len(row),
                line_no
            ))

        parsed_row = {}

        for i, field in enumerate(FIELDS):
            parsed_row[field] = row[i].strip()

        return parsed_row

    def _parse_co_hosts(self, src_co_hosts):
        co_hosts = []

        if src_co_hosts:
            for name in src_co_hosts.split(','):
                co_hosts.append(name.strip())

        return co_hosts
