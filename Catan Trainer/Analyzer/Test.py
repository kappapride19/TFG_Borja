import json
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


# Función para cargar el archivo JSON desde una ruta seleccionada por el usuario
def cargar_json_desde_ruta():
    ruta = filedialog.askopenfilename(
        title="Selecciona el archivo JSON",
        filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*"))
    )

    if not ruta:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")
        return None

    try:
        with open(ruta, 'r') as archivo:
            data = json.load(archivo)
        return data
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo JSON.\nError: {e}")
        return None


# Función para calcular las victorias por estrategia
def calcular_victorias_por_estrategia(data):
    resume_bots = data['resume']['resume_bots']
    estrategias = ["agresiva", "pasiva", "cartas", "aleatoria"]
    total_victorias = {estrategia: 0 for estrategia in estrategias}

    for bot_key, bot_info in resume_bots.items():
        matriz_victorias = eval(bot_info["Matriz de victorias en esta partida:"])
        for i, estrategia in enumerate(estrategias):
            total_victorias[estrategia] += matriz_victorias[i]

    return total_victorias


# Función para calcular los porcentajes de victorias
def calcular_porcentajes_victorias(total_victorias):
    total_victorias_totales = sum(total_victorias.values())
    porcentajes = {estrategia: (victorias / total_victorias_totales) * 100 for estrategia, victorias in
                   total_victorias.items()}
    return porcentajes, total_victorias_totales


# Función para mostrar los resultados en una tabla
def mostrar_resultados():
    data = cargar_json_desde_ruta()
    if data is None:
        return

    victorias_por_estrategia = calcular_victorias_por_estrategia(data)
    porcentajes_victorias, total_victorias_totales = calcular_porcentajes_victorias(victorias_por_estrategia)

    df = pd.DataFrame({
        'Estrategia': victorias_por_estrategia.keys(),
        'Total de Victorias': victorias_por_estrategia.values(),
        'Porcentaje de Victorias (%)': [f"{porcentaje:.2f}%" for porcentaje in porcentajes_victorias.values()]
    })

    df.loc[len(df.index)] = ['Total', total_victorias_totales, '100.00%']

    # Crear una nueva ventana para mostrar la tabla
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados")

    tabla = ttk.Treeview(ventana_resultados, columns=list(df.columns), show='headings')
    tabla.pack(expand=True, fill='both')

    for col in df.columns:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center")

    for index, row in df.iterrows():
        tabla.insert("", "end", values=list(row))


# Crear la ventana principal
root = tk.Tk()
root.title("Analizador de Estrategias")

# Configurar el tamaño de la ventana principal
root.geometry("300x200")

# Crear un botón para seleccionar el archivo y mostrar resultados
boton = tk.Button(root, text="Seleccionar Archivo JSON y Mostrar Resultados", command=mostrar_resultados)
boton.pack(pady=50)

# Iniciar el bucle de eventos de la interfaz gráfica
root.mainloop()
