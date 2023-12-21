import random


class Clients:
    def __init__(self, crm):
        self.crm = crm

    def get_clients(self):
        return self.crm.req("GET", "clients")

    def get_client_ids(self):
        clients = self.get_clients()
        return [c['id'] for c in clients]

    def generate_client_id(self):
        current_ids = self.get_client_ids()
        bottom = 10000
        top = 20000 + len(current_ids)
        while True:
            new_id = random.randint(bottom, top)
            if new_id not in current_ids:
                return new_id
