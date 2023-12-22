import random


class Clients:
    def __init__(self, crm):
        self.crm = crm

    def get_clients(self, params={}):
        return self.crm.req("GET", "clients", params=params)

    def get_client_ids(self):
        clients = self.get_clients()
        return [c['userIdent'] for c in clients]

    def generate_client_id(self):
        current_ids = self.get_client_ids()
        bottom = 10000
        top = 20000 + len(current_ids)
        while True:
            new_id = random.randint(bottom, top)
            if new_id not in current_ids:
                return new_id

    def create_client(self, data):
        data['userIdent'] = self.generate_client_id()
        new_client = self.crm.req("POST", "clients", json=data)
        return new_client

    def get_client(self, client_id):
        return self.crm.req("GET", f"clients/{client_id}")

    def update_client(self, client_id, data):
        return self.crm.req("PATCH", f"clients/{client_id}", json=data)

    def delete_client(self, client_id):
        return self.crm.req("DELETE", f"clients/{client_id}")
