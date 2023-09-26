import json
import time
import numpy as np
import pymemcache
from pymemcache.client.base import Client
from find_car_by_id import find_car_by_id
import socket

class CacheClient:
    def __init__(self, host="memcached", port=11211):
        self.mc_client = Client(f"{host}:{port}")

    def get(self, key, simulated=False):
        start_time = time.time()  # Inicio del temporizador

        # Intenta obtener el valor desde Memcached
        cache_key = f"{key}"
        cached_value = self.mc_client.get(cache_key)

        if cached_value is not None:
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            print(f"Time taken (cache): {elapsed_time:.5f} seconds")
            return cached_value.decode('utf-8')

        # Si no está en el caché, busca en el JSON
        value = find_car_by_id(int(key))
        value = str(value)
        if value:
            value_str = json.dumps(value)
            print("Key found in JSON. Adding to cache...")

            # Agrega la llave-valor al caché
            self.mc_client.set(cache_key, value_str)

            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            print(f"Time taken (JSON): {elapsed_time:.5f} seconds")
            return value_str
        else:
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            print(f"Time taken: {elapsed_time:.5f} seconds")
            print("Key not found.")
            return None
            
    def simulate_searches(self, n_searches=100):
        keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_searches)]

        # Métricas
        time_without_cache = 0
        time_with_cache = 0
        avoided_json_lookups = 0

        count = 0
        for key in keys_to_search:
            # clear console
            count += 1
            print("\033[H\033[J")
            print(f"Searching : {count}/{n_searches}")
            start_time = time.time()
            self.get(key)
            elapsed_time = time.time() - start_time
            if elapsed_time < 1:
                avoided_json_lookups += 1

        print(f"\nTime saved thanks to cache: {elapsed_time:.2f} seconds")
        print(f"Number of times JSON lookup was avoided: {avoided_json_lookups}")
        

if __name__ == '__main__':

    client = CacheClient()

    while True:
        print("\nChoose an operation:")
        print("1. Get")
        print("2. Simulate Searches")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            key = input("Enter key: ")
            value = client.get(key)
            if value is not None:
                print(f"Value: {value}")
        elif choice == "2":
            n_searches = int(input("Enter the number of searches you want to simulate: "))
            client.simulate_searches(n_searches)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")