from collections import Counter

from project.clients.business_client import BusinessClient
from project.clients.regular_client import RegularClient
from project.plants.flower import Flower
from project.plants.leaf_plant import LeafPlant


class FlowerShopManager:
    PLANT_TYPES = {'Flower': Flower, 'LeafPlant': LeafPlant}
    CLIENT_TYPES = {"RegularClient": RegularClient, "BusinessClient": BusinessClient}

    def __init__(self):
        self.income = 0.0
        self.plants = []
        self.clients = []

    def add_plant(self, plant_type: str, plant_name: str, plant_price: float, plant_water_needed: int, plant_extra_data: str):
        if plant_type not in self.PLANT_TYPES:
            raise ValueError("Unknown plant type!")

        new_plant = self.PLANT_TYPES[plant_type](plant_name, plant_price, plant_water_needed, plant_extra_data)
        self.plants.append(new_plant)
        return f"{plant_name} is added to the shop as {plant_type}."

    def add_client(self, client_type: str, client_name: str, client_phone_number: str):
        if client_type not in self.CLIENT_TYPES:
            raise ValueError("Unknown client type!")

        if self.find_client(client_phone_number):
            raise ValueError("This phone number has been used!")

        new_client = self.CLIENT_TYPES[client_type](client_name, client_phone_number)
        self.clients.append(new_client)
        return f"{client_name} is successfully added as a {client_type}."

    def sell_plants(self, client_phone_number: str, plant_name: str, plant_quantity: int):
        client = self.find_client(client_phone_number)
        if not client:
            raise ValueError("Client not found!")

        plants = self.find_plants(plant_name)
        if not plants:
            raise ValueError("Plants not found!")

        if len(plants) < plant_quantity:
            return "Not enough plant quantity."

        del plants[plant_quantity:]
        amount = sum(p.price for p in plants)
        discount = client.discount
        order_amount = amount - (discount / 100) * amount
        self.income += order_amount
        [self.plants.remove(p) for p in plants]

        client.update_total_orders()
        client.update_discount()

        return f"{plant_quantity}pcs. of {plant_name} plant sold for {order_amount:.2f}"

    def remove_plant(self, plant_name: str):
        plants = self.find_plants(plant_name)
        if not plants:
            return "No such plant name."

        plant = plants[0]
        self.plants.remove(plant)
        return f"Removed {plant.plant_details()}"

    def remove_clients(self):
        initial_count = len(self.clients)
        self.clients = [client for client in self.clients if client.total_orders > 0]
        count = initial_count - len(self.clients)
        return f"{count} client/s removed."

    def shop_report(self):

        plant_counts = Counter(p.name for p in self.plants)
        sorted_plants = sorted(plant_counts.items(), key=lambda p: (-p[1], p[0]), reverse=False)
        sorted_clients = sorted(self.clients, key=lambda c: (-c.total_orders, c.phone_number))

        result = '~Flower Shop Report~\n'
        result += f'Income: {self.income:.2f}\n'
        result += f'Count of orders: {sum(c.total_orders for c in self.clients)}\n'
        result += f'~~Unsold plants: {len(self.plants)}~~\n'

        for plant, count in sorted_plants:
            result += f"{plant}: {count}\n"

        result += f'~~Clients number: {len(self.clients)}~~\n'

        for client in sorted_clients:
            result += client.client_details() + '\n'

        return result.strip()

    def find_client(self, number):
        clients = [c for c in self.clients if c.phone_number == number]
        return clients[0] if clients else None

    def find_plants(self, name):
        plants = [p for p in self.plants if p.name == name]
        return plants if plants else None
