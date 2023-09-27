import grpc
import json
import time
import numpy as np
import cache_service_pb2
import cache_service_pb2_grpc
from find_car_by_id import find_car_by_id
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class CacheClient:
    def __init__(self, host="master", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = cache_service_pb2_grpc.CacheServiceStub(self.channel)
        self.reset_metrics()

    def reset_metrics(self):
        self.tiempo_total = 0
        self.tiempo_de_busqueda = []
        self.num_busquedas_cache = 0
        self.num_busquedas_json = 0      


    def get(self, key, simulated=False):
        start_time = time.time()  # Inicio del temporizador

        response = self.stub.Get(cache_service_pb2.Key(key=key))
        
        if response.value:
            elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
            self.tiempo_de_busqueda.append(elapsed_time)
            self.tiempo_total += elapsed_time
            self.num_busquedas_cache += 1            
            print(f"Time taken (cache): {elapsed_time:.5f} seconds")
            return response.value
        else:
            print("Key not found in cache.")

            # Si no está en el caché, buscar en el JSON
            value = find_car_by_id(int(key))
            value = str(value)
            if value:
                print("Key found in JSON. Adding to cache...")
                
                # Agregando la llave-valor al caché
                self.stub.Put(cache_service_pb2.CacheItem(key=key, value=value))
                
                elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                self.tiempo_de_busqueda.append(elapsed_time)
                self.tiempo_total += elapsed_time
                self.num_busquedas_json += 1                

                print(f"Time taken (JSON): {elapsed_time:.5f} seconds")
                
                return value
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

        # Métricas
        num_busquedas_json = n_searches

        count = 0
        for key in keys_to_search:
            # clear console
            count += 1
            print("\033[H\033[J")
            print(f"Searching : {count}/{n_searches}")
            start_time = time.time()
            self.get(key)

        print(f"Número total de búsquedas: {num_busquedas_json}")
        print(f"Tiempo total de ejecución de las búsquedas: {self.tiempo_total}")
        print(f"Tiempo promedio de las búsquedas: {self.tiempo_total/num_busquedas_json}")
        
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
        plt.savefig('./grafico_casero.png')
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