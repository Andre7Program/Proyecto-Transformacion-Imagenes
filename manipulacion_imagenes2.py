import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def cargar_imagen(ruta):
    """Carga una imagen desde la ruta especificada."""
    imagen = cv2.imread(ruta)
    if imagen is None:
        raise FileNotFoundError("No se pudo cargar la imagen. Verifica la ruta.")
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)  # Convertir a RGB

def rotar_imagen(imagen, angulo):
    """Aplica una rotación a la imagen."""
    filas, columnas, _ = imagen.shape
    matriz_rotacion = cv2.getRotationMatrix2D((columnas / 2, filas / 2), angulo, 1)
    return cv2.warpAffine(imagen, matriz_rotacion, (columnas, filas))

def escalar_imagen(imagen, factor_x, factor_y):
    """Escala la imagen por los factores especificados."""
    filas, columnas, _ = imagen.shape
    if factor_x > 5 or factor_y > 5:
        raise ValueError("El factor de escala no puede ser mayor a 5 para evitar problemas de memoria.")
    nuevo_ancho = max(1, int(columnas * factor_x))  # Asegurarse de que el ancho sea al menos 1
    nuevo_alto = max(1, int(filas * factor_y))  # Asegurarse de que el alto sea al menos 1
    return cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_LINEAR)

def reflejar_imagen(imagen, eje):
    """Refleja la imagen sobre el eje especificado."""
    if eje == 'horizontal':
        return cv2.flip(imagen, 0)
    elif eje == 'vertical':
        return cv2.flip(imagen, 1)
    else:
        raise ValueError("El eje debe ser 'horizontal' o 'vertical'.")

def trasladar_imagen(imagen, desplazamiento_x, desplazamiento_y):
    """Aplica una traslación a la imagen."""
    filas, columnas, _ = imagen.shape
    matriz_traslacion = np.float32([[1, 0, desplazamiento_x], [0, 1, desplazamiento_y]])
    return cv2.warpAffine(imagen, matriz_traslacion, (columnas, filas))

def mostrar_imagen(imagen_cv):
    """Convierte la imagen de OpenCV a un formato compatible con Tkinter y la muestra."""
    imagen_pil = Image.fromarray(imagen_cv)
    return ImageTk.PhotoImage(imagen_pil)

def cargar_archivo():
    """Abre un cuadro de diálogo para seleccionar una imagen y cargarla."""
    global imagen_original, imagen_transformada, tk_imagen_original, historial_transformaciones
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.png")])
    if ruta:
        try:
            imagen_original = cargar_imagen(ruta)
            imagen_transformada = imagen_original.copy()  # Inicializar la imagen transformada
            historial_transformaciones = [imagen_original.copy()]  # Inicializar historial
            tk_imagen_original = mostrar_imagen(imagen_original)
            etiqueta_imagen_original.config(image=tk_imagen_original)
            etiqueta_imagen_original.image = tk_imagen_original
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

def actualizar_campos(*args):
    """Actualiza los campos visibles según la transformación seleccionada."""
    seleccion = opcion_transformacion.get()
    
    # Ocultar todos los elementos primero
    entrada_parametro_1.pack_forget()
    entrada_parametro_2.pack_forget()
    etiqueta_parametro_1.pack_forget()
    etiqueta_parametro_2.pack_forget()
    boton_aplicar.pack_forget()
    boton_guardar.pack_forget()

    if seleccion == "Rotar":
        etiqueta_parametro_1.config(text="Ángulo (grados):")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
    elif seleccion == "Escalar":
        # Mostrar primero los campos X e Y
        etiqueta_parametro_1.config(text="Factor de escala en X (máx. 5):")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
        etiqueta_parametro_2.config(text="Factor de escala en Y (máx. 5):")
        etiqueta_parametro_2.pack(pady=5)
        entrada_parametro_2.pack(pady=5, ipadx=5, ipady=5)
    elif seleccion == "Reflejar":
        etiqueta_parametro_1.config(text="Eje (horizontal/vertical):")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
    elif seleccion == "Trasladar":
        # Mostrar primero los campos X e Y
        etiqueta_parametro_1.config(text="Desplazamiento en X (px):")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
        etiqueta_parametro_2.config(text="Desplazamiento en Y (px):")
        etiqueta_parametro_2.pack(pady=5)
        entrada_parametro_2.pack(pady=5, ipadx=5, ipady=5)

    # Mostrar los botones al final
    boton_aplicar.pack(pady=10, ipadx=5, ipady=5)
    boton_guardar.pack(pady=10, ipadx=5, ipady=5)

def aplicar_transformacion():
    """Aplica la transformación seleccionada a la imagen transformada."""
    global imagen_transformada, tk_imagen_transformada, historial_transformaciones
    if imagen_transformada is None:
        messagebox.showerror("Error", "Primero carga una imagen.")
        return

    try:
        if opcion_transformacion.get() == "Rotar":
            angulo = float(entrada_parametro_1.get())
            imagen_transformada = rotar_imagen(imagen_transformada, angulo)
        elif opcion_transformacion.get() == "Escalar":
            factor_x = float(entrada_parametro_1.get())
            factor_y = float(entrada_parametro_2.get())
            imagen_transformada = escalar_imagen(imagen_transformada, factor_x, factor_y)
        elif opcion_transformacion.get() == "Reflejar":
            eje = entrada_parametro_1.get().strip().lower()
            imagen_transformada = reflejar_imagen(imagen_transformada, eje)
        elif opcion_transformacion.get() == "Trasladar":
            desplazamiento_x = int(entrada_parametro_1.get())
            desplazamiento_y = int(entrada_parametro_2.get())
            imagen_transformada = trasladar_imagen(imagen_transformada, desplazamiento_x, desplazamiento_y)
        else:
            messagebox.showerror("Error", "Selecciona una transformación válida.")
            return

        historial_transformaciones.append(imagen_transformada.copy())  # Guardar en historial
        tk_imagen_transformada = mostrar_imagen(imagen_transformada)
        etiqueta_imagen_transformada.config(image=tk_imagen_transformada)
        etiqueta_imagen_transformada.image = tk_imagen_transformada
    except ValueError as e:
        messagebox.showerror("Error", "Los parámetros deben ser números válidos.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def deshacer_transformacion():
    """Deshace la última transformación aplicada."""
    global imagen_transformada, tk_imagen_transformada, historial_transformaciones
    if len(historial_transformaciones) > 1:
        historial_transformaciones.pop()  # Eliminar la última transformación
        imagen_transformada = historial_transformaciones[-1].copy()  # Restaurar la anterior
        tk_imagen_transformada = mostrar_imagen(imagen_transformada)
        etiqueta_imagen_transformada.config(image=tk_imagen_transformada)
        etiqueta_imagen_transformada.image = tk_imagen_transformada
    else:
        messagebox.showinfo("Deshacer", "No hay más transformaciones para deshacer.")

def restaurar_imagen_original():
    """Restaura la imagen original completamente."""
    global imagen_transformada, tk_imagen_transformada, historial_transformaciones
    if imagen_original is not None:
        imagen_transformada = imagen_original.copy()
        historial_transformaciones = [imagen_original.copy()]  # Reiniciar historial
        tk_imagen_transformada = mostrar_imagen(imagen_transformada)
        etiqueta_imagen_transformada.config(image=tk_imagen_transformada)
        etiqueta_imagen_transformada.image = tk_imagen_transformada
    else:
        messagebox.showinfo("Restaurar", "No hay una imagen cargada para restaurar.")

def guardar_imagen():
    """Guarda la imagen transformada en un archivo."""
    if imagen_transformada is None:
        messagebox.showerror("Error", "No hay una imagen transformada para guardar.")
        return

    ruta = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Imágenes", "*.jpg;*.png")])
    if ruta:
        cv2.imwrite(ruta, cv2.cvtColor(imagen_transformada, cv2.COLOR_RGB2BGR))  # Convertir a BGR para guardar
        messagebox.showinfo("Éxito", "Imagen guardada correctamente.")

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Manipulación de Imágenes")
ventana.geometry("1000x700")
ventana.configure(bg="#2b2b2b")

# Variables globales
imagen_original = None
imagen_transformada = None
tk_imagen_original = None
tk_imagen_transformada = None
historial_transformaciones = []

# Configuración de estilos
estilo_label = {"bg": "#2b2b2b", "fg": "#ffffff", "font": ("Arial", 14)}
estilo_button = {"bg": "#444444", "fg": "#ffffff", "font": ("Arial", 12), "relief": "flat", "activebackground": "#555555"}

# Marco de controles
marco_controles = tk.Frame(ventana, bg="#2b2b2b")
marco_controles.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

boton_cargar = tk.Button(marco_controles, text="Cargar Imagen", command=cargar_archivo, **estilo_button)
boton_cargar.pack(pady=10, ipadx=5, ipady=5)

opcion_transformacion = tk.StringVar(value="Rotar")
opcion_transformacion.trace_add("write", actualizar_campos)  # Detectar cambios en la selección del menú
menu_transformaciones = tk.OptionMenu(marco_controles, opcion_transformacion, "Rotar", "Escalar", "Reflejar", "Trasladar")
menu_transformaciones.config(bg="#444444", fg="#ffffff", font=("Arial", 12), activebackground="#555555", relief="flat")
menu_transformaciones.pack(pady=10, ipadx=5, ipady=5)

etiqueta_parametro_1 = tk.Label(marco_controles, text="Ángulo (grados):", **estilo_label)
etiqueta_parametro_1.pack(pady=5)
entrada_parametro_1 = tk.Entry(marco_controles, font=("Arial", 12))
entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)

etiqueta_parametro_2 = tk.Label(marco_controles, text="", **estilo_label)
etiqueta_parametro_2.pack(pady=5)
entrada_parametro_2 = tk.Entry(marco_controles, font=("Arial", 12))
entrada_parametro_2.pack(pady=5, ipadx=5, ipady=5)

boton_aplicar = tk.Button(marco_controles, text="Aplicar Transformación", command=aplicar_transformacion, **estilo_button)
boton_aplicar.pack(pady=10, ipadx=5, ipady=5)

boton_guardar = tk.Button(marco_controles, text="Guardar Imagen", command=guardar_imagen, **estilo_button)
boton_guardar.pack(pady=10, ipadx=5, ipady=5)

boton_deshacer = tk.Button(marco_controles, text="Deshacer Transformación", command=deshacer_transformacion, **estilo_button)
boton_deshacer.pack(pady=10, ipadx=5, ipady=5)

boton_restaurar = tk.Button(marco_controles, text="Restaurar Imagen Original", command=restaurar_imagen_original, **estilo_button)
boton_restaurar.pack(pady=10, ipadx=5, ipady=5)

# Marcos para mostrar imágenes
marco_imagenes = tk.Frame(ventana, bg="#2b2b2b")
marco_imagenes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

etiqueta_imagen_original = tk.Label(marco_imagenes, text="Imagen Original", **estilo_label)
etiqueta_imagen_original.pack(side=tk.LEFT, padx=10, pady=10)

etiqueta_imagen_transformada = tk.Label(marco_imagenes, text="Imagen Transformada", **estilo_label)
etiqueta_imagen_transformada.pack(side=tk.RIGHT, padx=10, pady=10)

# Configurar campos iniciales
actualizar_campos()

# Iniciar la ventana
ventana.mainloop()
