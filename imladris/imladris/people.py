import json


class People:
    def prepare_people_json(self, people):
        json_data = []

        for person_name, person_details in people.items():
            json_data.append(self._to_konopas_person_item(person_name, person_details))

        return json.dumps(json_data, indent=2, ensure_ascii=False)

    def prepare_people_dict(self, rows):
        people = {}
        person_id = 1

        for line_no, row in enumerate(rows):
            for host in row['hosts']:
                person_id = self._add_person_to_people_dict(people, host, person_id)

                self._add_prog_item_to_person(people[host['display_name']], row['id'])

        return people

    def _to_konopas_person_item(self, person_name, person_details):
        return {
            "id": person_details['id'],
            "name": person_name,
            "sortname": person_details['sortname'],
            "tags": [],
            "prog": sorted(list(person_details['prog'])),
            "links": [],
            "bio": ""
        }

    def _add_person_to_people_dict(self, people, person, person_id):
        if person['display_name'] not in people:
            people[person['display_name']] = {
                'id': person_id,
                'sortname': person['sortname'],
                'prog': set()
            }
            person_id += 1

        return person_id

    def _add_prog_item_to_person(self, person, prog_item_id):
        person['prog'].add(prog_item_id)
