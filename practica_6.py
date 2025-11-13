import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import os

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
    global resultados_derivas, limite_excedido, max_deriva, piso_max_deriva
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

        # ================================================================
        # Generar reporte profesional (en pantalla)
        # ================================================================
        text_resultados.config(state="normal")
        text_resultados.delete(1.0, tk.END)

        text_resultados.insert(tk.END, "───────────────────────────────────────────────\n")
        text_resultados.insert(tk.END, "        INFORME TÉCNICO DE ANÁLISIS SÍSMICO\n")
        text_resultados.insert(tk.END, "───────────────────────────────────────────────\n\n")
        text_resultados.insert(tk.END, "📋 DATOS GENERALES:\n")
        text_resultados.insert(tk.END, f"• Número de pisos analizados: {len(masas)}\n")
        text_resultados.insert(tk.END, f"• Límite de deriva permitido: {LIMITE_DERIVA:.6f} m\n\n")

        text_resultados.insert(tk.END, "🏗️ RESULTADOS POR PISO:\n")
        text_resultados.insert(tk.END, "-----------------------------------------------\n")
        text_resultados.insert(tk.END, " Piso |   Deriva (m)   |   Evaluación\n")
        text_resultados.insert(tk.END, "-----------------------------------------------\n")

        for i, d in enumerate(resultados_derivas):
            estado = "✅ Cumple" if d <= LIMITE_DERIVA else "⚠️ Falla"
            text_resultados.insert(tk.END, f"  {i+1:<4} |   {d:.6f}   |   {estado}\n")

        text_resultados.insert(tk.END, "-----------------------------------------------\n\n")
        text_resultados.insert(tk.END, "📊 RESUMEN GENERAL:\n")

        if limite_excedido:
            text_resultados.insert(tk.END, f"⚠️  Se detectaron derivas superiores al límite permitido.\n")
            text_resultados.insert(tk.END, f"🔹 Deriva máxima registrada: {max_deriva:.6f} m (Piso {piso_max_deriva})\n")
            text_resultados.insert(tk.END, f"🔸 Límite reglamentario: {LIMITE_DERIVA:.6f} m\n\n")
            text_resultados.insert(tk.END, "📑 OBSERVACIONES:\n")
            text_resultados.insert(tk.END, "• Se recomienda revisar el diseño estructural.\n")
            text_resultados.insert(tk.END, "• Aumentar la rigidez lateral o mejorar la distribución de masas.\n")
        else:
            text_resultados.insert(tk.END, f"✅ Todas las derivas cumplen con el límite establecido.\n")
            text_resultados.insert(tk.END, f"🔹 Deriva máxima registrada: {max_deriva:.6f} m (Piso {piso_max_deriva})\n\n")
            text_resultados.insert(tk.END, "📑 OBSERVACIONES:\n")
            text_resultados.insert(tk.END, "• La estructura cumple con los criterios de deriva.\n")
            text_resultados.insert(tk.END, "• No se requiere modificación estructural.\n")

        text_resultados.insert(tk.END, "\n───────────────────────────────────────────────\n")
        text_resultados.insert(tk.END, "Fin del informe técnico.\n")
        text_resultados.insert(tk.END, "───────────────────────────────────────────────\n")

        text_resultados.config(state="disabled")

        btn_pdf.config(state="normal")

        # ================================================================
        # GRAFICAR DERIVAS POR PISO
        # ================================================================
        pisos = list(range(1, len(resultados_derivas) + 1))
        plt.figure(figsize=(6, 4))
        plt.bar(pisos, resultados_derivas, color="#7289da", edgecolor="black")
        plt.axhline(y=LIMITE_DERIVA, color="red", linestyle="--", label=f"Límite permitido ({LIMITE_DERIVA})")
        plt.title("Deriva por Piso", fontsize=14, fontweight="bold")
        plt.xlabel("Piso")
        plt.ylabel("Deriva (m)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Debe llenar todos los campos con valores numéricos válidos.")


# ================================================================
# Exportar reporte a PDF (con gráfica y eliminación automática)
# ================================================================
def exportar_pdf():
    try:
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        doc = SimpleDocTemplate("Informe_Sismico.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # ======= Encabezado =======
        elements.append(Paragraph("<b>INFORME TÉCNICO DE ANÁLISIS SÍSMICO</b>", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>Fecha de generación:</b> {fecha_actual}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Límite de deriva permitido:</b> {LIMITE_DERIVA:.6f} m", styles["Normal"]))
        elements.append(Spacer(1, 12))

        # ======= Tabla =======
        data = [["Piso", "Deriva (m)", "Evaluación"]]
        for i, d in enumerate(resultados_derivas):
            estado = "Cumple" if d <= LIMITE_DERIVA else "Falla"
            data.append([str(i + 1), f"{d:.6f}", estado])

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black)
        ]))
        elements.append(tabla)
        elements.append(Spacer(1, 18))

        # ======= Gráfica =======
        pisos = list(range(1, len(resultados_derivas) + 1))
        plt.figure(figsize=(5, 3))
        plt.bar(pisos, resultados_derivas, color="#7289da", edgecolor="black")
        plt.axhline(y=LIMITE_DERIVA, color="red", linestyle="--", label=f"Límite permitido ({LIMITE_DERIVA})")
        plt.title("Deriva por Piso", fontsize=12)
        plt.xlabel("Piso")
        plt.ylabel("Deriva (m)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig("grafica_derivas.png", dpi=150)
        plt.close()

        elements.append(Paragraph("<b>Gráfica de Derivas:</b>", styles["Heading3"]))
        elements.append(Image("grafica_derivas.png", width=400, height=240))
        elements.append(Spacer(1, 18))

        # ======= Resumen =======
        if limite_excedido:
            resumen = f"Se detectaron derivas superiores al límite permitido. Deriva máxima: {max_deriva:.6f} m (Piso {piso_max_deriva})."
        else:
            resumen = f"Todas las derivas cumplen con el límite establecido. Deriva máxima: {max_deriva:.6f} m (Piso {piso_max_deriva})."

        elements.append(Paragraph("<b>Resumen:</b>", styles["Heading3"]))
        elements.append(Paragraph(resumen, styles["Normal"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Observaciones:", styles["Heading3"]))
        if limite_excedido:
            elements.append(Paragraph("Se recomienda revisar el diseño estructural y aumentar la rigidez lateral.", styles["Normal"]))
        else:
            elements.append(Paragraph("La estructura cumple con los criterios de deriva y no requiere modificaciones.", styles["Normal"]))
        elements.append(Spacer(1, 24))
        elements.append(Paragraph("<i>Generado automáticamente por el Sistema de Análisis Sísmico</i>", styles["Italic"]))

        # ======= Crear PDF =======
        doc.build(elements)

        # ======= Eliminar imagen temporal =======
        if os.path.exists("grafica_derivas.png"):
            os.remove("grafica_derivas.png")

        messagebox.showinfo("Éxito", "Informe PDF generado correctamente como 'Informe_Sismico.pdf' (con gráfica).")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")


# ================================================================
# Interfaz Gráfica
# ================================================================
root = tk.Tk()
root.title("Análisis Sísmico de Estructura")
root.geometry("880x700")

fondo = tk.Canvas(root, width=880, height=700)
fondo.pack(fill="both", expand=True)
for i in range(700):
    color = f'#{int(30 + i/5):02x}{int(33 + i/7):02x}{int(36 + i/10):02x}'
    fondo.create_line(0, i, 880, i, fill=color)

main_frame = tk.Frame(root, bg="#1e2124", bd=4, relief="ridge")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=820, height=640)

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
btn_calcular.pack(pady=8)

btn_pdf = tk.Button(main_frame, text="Exportar Informe a PDF", bg="#faa61a", fg="black",
                    font=("Arial", 11, "bold"), state="disabled", command=exportar_pdf)
btn_pdf.pack(pady=5)

frame_resultados = tk.Frame(main_frame, bg="#2c2f33", bd=3, relief="ridge")
frame_resultados.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(frame_resultados, text="Resultados del Análisis:", bg="#2c2f33", fg="white", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)

text_resultados = tk.Text(frame_resultados, height=10, state="disabled", bg="#99aab5", fg="black", font=("Consolas", 10))
text_resultados.pack(padx=10, pady=5, fill="both", expand=True)

root.mainloop()
