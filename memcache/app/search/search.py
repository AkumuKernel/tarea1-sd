import json
import time
import numpy as np
import pymemcache
from pymemcache.client.base import Client
from find_car_by_id import find_car_by_id
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class CacheClient:
    def __init__(self, host="memcached", port=11211):
        self.mc_client = Client(f"{host}:{port}")
        self.reset_metrics()

    def reset_metrics(self):
        self.tiempo_total = 0
        self.tiempo_de_busqueda = []
        self.num_busquedas_cache = 0
        self.num_busquedas_json = 0      

    def get(self, key, simulated=False):
        start_time = time.time()  # Inicio del temporizador

        # Intenta obtener el valor desde Memcached
        cache_key = f"{key}"
        cached_value = self.mc_client.get(cache_key)

        if cached_value is not None:
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            self.tiempo_de_busqueda.append(elapsed_time)
            self.tiempo_total += elapsed_time
            self.num_busquedas_cache += 1
            print(f"Time taken (memcached): {elapsed_time:.5f} seconds")

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
            self.tiempo_de_busqueda.append(elapsed_time)
            self.tiempo_total += elapsed_time
            self.num_busquedas_json += 1
            print(f"Time taken (JSON): {elapsed_time:.5f} seconds")
            return value_str
        else:
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            self.tiempo_de_busqueda.append(elapsed_time)
            self.tiempo_total += elapsed_time
            print(f"Time taken: {elapsed_time:.5f} seconds")
            print("Key not found.")
            return None
            
    def simulate_searches(self, n_searches=100):
        self.reset_metrics()
        keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_searches)]

        count = 0
        for key in keys_to_search:
            # clear console
            count += 1
            print("\033[H\033[J")
            print(f"Searching : {count}/{n_searches}")
            start_time = time.time()
            self.get(key)

        print(f"Número total de búsquedas (JSON): {self.num_busquedas_json}")
        print(f"Número total de búsquedas (cache): {self.num_busquedas_cache}")
        print(f"Tiempo total de ejecución de las búsquedas: {self.tiempo_total}")
        print(f"Tiempo promedio de las búsquedas: {self.tiempo_total/n_searches}")

    def create_dataframe(self, filename=None):
      data = {
       'Tiempo de búsqueda': self.tiempo_de_busqueda,
       'Tipo de búsqueda': ['Caché' if i < self.num_busquedas_cache else 'JSON' for i in range(len(self.tiempo_de_busqueda))]
      }
      df = pd.DataFrame(data)

      if filename:
        df.to_csv(filename, index=False)

      return df

    def generate_graphic(self):
     if len(self.tiempo_de_busqueda) > 10:
        df = self.create_dataframe("tabla_resultados.csv")
        plt.figure(figsize=(8, 6))
        df['Tipo de búsqueda'].value_counts().plot(kind='bar')
        plt.title(f"Número de búsquedas ({len(self.tiempo_de_busqueda)}) en Caché vs. JSON")
        plt.xlabel('Tipo de búsqueda')
        plt.ylabel('Número de búsquedas')
        plt.savefig('./grafico_mem.png')
        print("Gráfico generado correctamente")
     else:
        print("First Simulate Searches")
if __name__ == '__main__':

    client = CacheClient()

    while True:
        print("\nChoose an operation:")
        print("1. Get")
        print("2. Simulate Searches")
        print("3. Generate Graph")
        print("4. Exit")

        choice = input("Enter your choice: ")
        n_searches = 0
        if choice == "1":
            key = input("Enter key: ")
            value = client.get(key)
            if value is not None:
                print(f"Value: {value}")
        elif choice == "2":
            n_searches = int(input("Enter the number of searches you want to simulate: "))
            client.simulate_searches(n_searches)
        elif choice == "3":
            client.generate_graphic()
        elif choice == "4":
            print("Goodbye!")
            break        
        else:
            print("Invalid choice. Try again.")