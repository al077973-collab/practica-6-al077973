import tkinter as tk
from tkinter import messagebox
import math

LIMITE_DERIVA = 0.005

# ================================================================
# Funciones principales
# ================================================================
def obtener_datos_estructura():
    try:
        N_pisos = int(entry_pisos.get())
        if N_pisos <= 0:
            messagebox.showerror("Error", "El número de pisos debe ser positivo.")
            return
        
        for widget in frame_datos.winfo_children():
            widget.destroy()

        headers = ["Masa (kg)", "Rigidez (N/m)", "Fuerza Sísmica (N)"]
        entries_por_piso.clear()

        header_style = ("Arial", 11, "bold")
        for j, h in enumerate(["Piso"] + headers):
            tk.Label(frame_datos, text=h, bg="#1e2124", fg="#99aab5", font=header_style).grid(row=0, column=j, padx=6, pady=4)

        for i in range(N_pisos):
            piso_num = i + 1
            tk.Label(frame_datos, text=f"{piso_num}", bg="#1e2124", fg="#ffffff", font=("Arial", 10, "bold")).grid(row=piso_num, column=0, padx=6, pady=4)
            fila_entries = []

            placeholders = ["Ej: 20000", "Ej: 8000000", "Ej: 4000"]

            for j, texto in enumerate(placeholders):
                e = tk.Entry(frame_datos, width=15, justify="center", fg="gray")
                e.insert(0, texto)
                e.bind("<FocusIn>", lambda event, entry=e, val=texto: limpiar_placeholder(event, entry, val))
                e.bind("<FocusOut>", lambda event, entry=e, val=texto: restaurar_placeholder(event, entry, val))
                e.grid(row=piso_num, column=j+1, padx=6, pady=4)
                fila_entries.append(e)

            entries_por_piso.append(fila_entries)

        btn_calcular.config(state="normal")

    except ValueError:
        messagebox.showerror("Error", "Debe ingresar un número válido de pisos.")


def limpiar_placeholder(event, entry, valor):
    if entry.get() == valor:
        entry.delete(0, tk.END)
        entry.config(fg="black")


def restaurar_placeholder(event, entry, valor):
    if entry.get() == "":
        entry.insert(0, valor)
        entry.config(fg="gray")


def analisis_sismico():
    try:
        masas, rigideces, fuerzas = [], [], []

        for fila in entries_por_piso:
            M = float(fila[0].get())
            K = float(fila[1].get())
            F = float(fila[2].get())
            masas.append(M)
            rigideces.append(K)
            fuerzas.append(F)

        max_deriva, piso_max_deriva, limite_excedido = -1.0, -1, False
        resultados_derivas = []

        for i in range(len(masas)):
            F = fuerzas[i]
            K = rigideces[i]
            deriva = F / K if K != 0 else float('inf')
            resultados_derivas.append(deriva)

            if deriva > max_deriva:
                max_deriva = deriva
                piso_max_deriva = i + 1
            if deriva > LIMITE_DERIVA:
                limite_excedido = True

        text_resultados.config(state="normal")
        text_resultados.delete(1.0, tk.END)
        text_resultados.insert(tk.END, "🏗️  INFORME DE RESPUESTA DINÁMICA DE LA ESTRUCTURA\n")
        text_resultados.insert(tk.END, "="*60 + "\n\n")
        for i, d in enumerate(resultados_derivas):
            estado = "✅ Cumple" if d <= LIMITE_DERIVA else "⚠️ Falla"
            text_resultados.insert(tk.END, f"Piso {i+1}: Deriva = {d:.6f} m   --> {estado}\n")

        text_resultados.insert(tk.END, "\n--- Resumen del Análisis ---\n")
        if limite_excedido:
            text_resultados.insert(tk.END, f"⚠️ ¡ADVERTENCIA! Límite de deriva excedido.\n")
            text_resultados.insert(tk.END, f"Deriva máxima: {max_deriva:.6f} m en Piso {piso_max_deriva}\n")
            text_resultados.insert(tk.END, f"Límite permitido: {LIMITE_DERIVA} m\n")
        else:
            text_resultados.insert(tk.END, f"✅ Cumple con el límite de deriva.\n")
            text_resultados.insert(tk.END, f"Deriva máxima: {max_deriva:.6f} m (Piso {piso_max_deriva})\n")

        text_resultados.config(state="disabled")

    except ValueError:
        messagebox.showerror("Error", "Debe llenar todos los campos con valores numéricos válidos.")


# ================================================================
# Interfaz Gráfica
# ================================================================
root = tk.Tk()
root.title("Análisis Sísmico de Estructura")
root.geometry("880x680")

# Fondo degradado
fondo = tk.Canvas(root, width=880, height=680)
fondo.pack(fill="both", expand=True)
for i in range(680):
    color = f'#{int(30 + i/5):02x}{int(33 + i/7):02x}{int(36 + i/10):02x}'
    fondo.create_line(0, i, 880, i, fill=color)

# Frame principal
main_frame = tk.Frame(root, bg="#1e2124", bd=4, relief="ridge")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=820, height=620)

tk.Label(main_frame, text="ANÁLISIS SÍSMICO DE ESTRUCTURA", bg="#1e2124", fg="#7289da",
         font=("Arial", 18, "bold")).pack(pady=15)

frame_superior = tk.Frame(main_frame, bg="#2c2f33", bd=3, relief="ridge")
frame_superior.pack(pady=10, padx=10, fill="x")

tk.Label(frame_superior, text="Número de Pisos:", bg="#2c2f33", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
entry_pisos = tk.Entry(frame_superior, width=10)
entry_pisos.pack(side="left", padx=5)
tk.Button(frame_superior, text="Generar Datos", bg="#7289da", fg="white",
          font=("Arial", 10, "bold"), command=obtener_datos_estructura).pack(side="left", padx=10)

frame_datos = tk.Frame(main_frame, bg="#1e2124", bd=3, relief="ridge")
frame_datos.pack(pady=10, padx=10, fill="both", expand=True)

entries_por_piso = []

btn_calcular = tk.Button(main_frame, text="Calcular Derivas", bg="#43b581", fg="white",
                         font=("Arial", 12, "bold"), state="disabled", command=analisis_sismico)
btn_calcular.pack(pady=12)

frame_resultados = tk.Frame(main_frame, bg="#2c2f33", bd=3, relief="ridge")
frame_resultados.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(frame_resultados, text="Resultados del Análisis:", bg="#2c2f33", fg="white", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)

text_resultados = tk.Text(frame_resultados, height=10, state="disabled", bg="#99aab5", fg="black", font=("Consolas", 10))
text_resultados.pack(padx=10, pady=5, fill="both", expand=True)

root.mainloop()
