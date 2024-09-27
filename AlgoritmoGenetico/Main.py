import random
import tkinter as tk
from tkinter import messagebox

# Definición de cultivos y sus características
crops = [
    {'name': 'Maíz', 'temperature_range': (15, 30), 'soil_type': 'Fértil'},
    {'name': 'Trigo', 'temperature_range': (10, 25), 'soil_type': 'Arcilloso'},
    {'name': 'Arroz', 'temperature_range': (20, 35), 'soil_type': 'Húmedo'},
    {'name': 'Soja', 'temperature_range': (20, 28), 'soil_type': 'Fértil'},
    {'name': 'Cebada', 'temperature_range': (5, 20), 'soil_type': 'Seco'},
]

# Función de aptitud
def fitness(crop, temperature, soil_type):
    temp_range = crop['temperature_range']
    if temp_range[0] <= temperature <= temp_range[1] and crop['soil_type'] in soil_type:
        return 1  # Cultivo apto
    return 0  # Cultivo no apto

# Inicialización de la población
def initialize_population(size):
    return random.sample(crops, size)

# Selección de los mejores cultivos
def selection(population, temperature, soil_type):
    scored_population = [(crop, fitness(crop, temperature, soil_type)) for crop in population]
    scored_population.sort(key=lambda x: x[1], reverse=True)
    
    # Mostrar en la terminal los cultivos seleccionados
    print(f"Selección actual (para temperatura={temperature} y suelo={soil_type}):")
    for crop, score in scored_population:
        print(f" - {crop['name']} (Fitness: {score})")
    
    return [crop for crop, score in scored_population if score > 0]

# Cruce de cultivos
def cruce(parent1, parent2):
    return random.choice([parent1, parent2])

# Mutación
def mutacion(crop):
    new_crop = random.choice(crops)
    # Mostrar la mutación en la terminal
    print(f"Mutación: {crop['name']} -> {new_crop['name']}")
    return new_crop

# Algoritmo genético
def genetic_algorithm(temperature, soil_type, generations=10, population_size=5):
    population = initialize_population(population_size)
    
    for generation in range(generations):
        print(f"\nGeneración {generation + 1}:")
        selected = selection(population, temperature, soil_type)
        
        if selected:
            next_generation = []
            while len(next_generation) < population_size:
                parent1 = random.choice(selected)
                parent2 = random.choice(selected)
                child = cruce(parent1, parent2)
                if random.random() < 0.1:  # Probabilidad de mutación
                    child = mutacion(child)
                next_generation.append(child)
            population = next_generation
        else:
            break

    # Remover duplicados de los resultados
    return list({crop['name']: crop for crop in selection(population, temperature, soil_type)}.values())

# Función para manejar la lógica del botón
def recommend_crops():
    try:
        temperature = float(entry_temperature.get())
        
        selected_soils = []
        if var_fertile.get():
            selected_soils.append('Fértil')
        if var_clay.get():
            selected_soils.append('Arcilloso')
        if var_humid.get():
            selected_soils.append('Húmedo')
        if var_dry.get():
            selected_soils.append('Seco')

        if not selected_soils:
            messagebox.showerror("Error", "Selecciona al menos un tipo de suelo.")
            return
        
        result = genetic_algorithm(temperature, selected_soils)
        
        if result:
            recommendations = "Cultivos recomendados:\n" + "\n".join([crop['name'] for crop in result])
            messagebox.showinfo("Recomendaciones", recommendations)
        else:
            messagebox.showinfo("Recomendaciones", "No hay cultivos adecuados para las condiciones dadas.")
    
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa una temperatura válida.")

# Crear la ventana principal
root = tk.Tk()
root.title("Recomendación de Cultivos")

# Configurar el tamaño de la ventana
root.geometry("400x400")
root.configure(bg="#f0f0f0")

# Estilos de fuente
font_large = ("Arial", 14, "bold")
font_medium = ("Arial", 12)
font_small = ("Arial", 10)

# Etiquetas y campos de entrada con estilos mejorados
label_temperature = tk.Label(root, text="Temperatura (°C):", font=font_large, bg="#f0f0f0")
label_temperature.pack(pady=10)
entry_temperature = tk.Entry(root, font=font_medium, width=10)
entry_temperature.pack(pady=5)

label_soil_type = tk.Label(root, text="Selecciona el tipo de suelo:", font=font_large, bg="#f0f0f0")
label_soil_type.pack(pady=10)

# Variables para los checkboxes
var_fertile = tk.BooleanVar()
var_clay = tk.BooleanVar()
var_humid = tk.BooleanVar()
var_dry = tk.BooleanVar()

# Checkbuttons para seleccionar el tipo de suelo con espaciado y tamaño mejorado
check_fertile = tk.Checkbutton(root, text="Fértil", variable=var_fertile, font=font_medium, bg="#f0f0f0")
check_fertile.pack(pady=5)
check_clay = tk.Checkbutton(root, text="Arcilloso", variable=var_clay, font=font_medium, bg="#f0f0f0")
check_clay.pack(pady=5)
check_humid = tk.Checkbutton(root, text="Húmedo", variable=var_humid, font=font_medium, bg="#f0f0f0")
check_humid.pack(pady=5)
check_dry = tk.Checkbutton(root, text="Seco", variable=var_dry, font=font_medium, bg="#f0f0f0")
check_dry.pack(pady=5)

# Botón para recomendar cultivos con estilos mejorados
button_recommend = tk.Button(root, text="Recomendar Cultivos", font=font_large, bg="#f0f0f0", fg="black", padx=10, pady=5, command=recommend_crops)
button_recommend.pack(pady=20)

# Iniciar el bucle de la interfaz
root.mainloop()
