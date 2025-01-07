import numpy as np
import cv2
import os

def cargar_imagen(ruta):
    """Carga una imagen desde la ruta especificada."""
    imagen = cv2.imread(ruta)
    if imagen is None:
        raise FileNotFoundError("No se pudo cargar la imagen. Verifica la ruta.")
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

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
    nuevo_ancho = max(1, int(columnas * factor_x))
    nuevo_alto = max(1, int(filas * factor_y))
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

def mostrar_imagenes(original, transformada, titulo_transformacion=""):
    """Muestra la imagen original y transformada lado a lado."""
    # Convertir de RGB a BGR para mostrar correctamente
    original_bgr = cv2.cvtColor(original, cv2.COLOR_RGB2BGR)
    transformada_bgr = cv2.cvtColor(transformada, cv2.COLOR_RGB2BGR)
    
    # Redimensionar las imágenes a un tamaño máximo para visualización
    max_altura = 500
    max_anchura = 800
    
    # Calcular proporciones para redimensionar
    altura_original = original.shape[0]
    anchura_original = original.shape[1]
    
    # Calcular factores de escala
    escala_altura = min(1.0, max_altura / altura_original)
    escala_anchura = min(1.0, max_anchura / (anchura_original * 2))  # Dividir por 2 porque mostraremos dos imágenes
    escala = min(escala_altura, escala_anchura)
    
    # Redimensionar imágenes
    if escala < 1.0:
        nueva_altura = int(altura_original * escala)
        nueva_anchura = int(anchura_original * escala)
        original_bgr = cv2.resize(original_bgr, (nueva_anchura, nueva_altura))
        transformada_bgr = cv2.resize(transformada_bgr, (nueva_anchura, nueva_altura))
    
    # Crear una imagen combinada
    combinada = np.hstack((original_bgr, transformada_bgr))
    
    # Mostrar las imágenes
    cv2.imshow(f'Original vs {titulo_transformacion}', combinada)
    cv2.waitKey(0)

def mostrar_menu():
    """Muestra el menú de opciones disponibles."""
    print("\n=== MENÚ DE MANIPULACIÓN DE IMÁGENES ===")
    print("1. Rotar imagen")
    print("2. Escalar imagen")
    print("3. Reflejar imagen")
    print("4. Trasladar imagen")
    print("5. Deshacer última transformación")
    print("6. Restaurar imagen original")
    print("7. Guardar imagen")
    print("8. Salir")
    print("=======================================")

def main():
    # Solicitar la ruta de la imagen
    while True:
        ruta_imagen = input("\nIngrese la ruta de la imagen (jpg o png): ")
        if os.path.exists(ruta_imagen):
            try:
                imagen_original = cargar_imagen(ruta_imagen)
                imagen_actual = imagen_original.copy()
                historial = [imagen_original.copy()]
                print("Imagen cargada exitosamente.")
                # Mostrar la imagen original al inicio
                cv2.imshow('Imagen Original', cv2.cvtColor(imagen_original, cv2.COLOR_RGB2BGR))
                cv2.waitKey(1000)
                break
            except Exception as e:
                print(f"Error al cargar la imagen: {str(e)}")
        else:
            print("La ruta especificada no existe. Intente nuevamente.")

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-8): ")

        try:
            if opcion == "1":  # Rotar
                angulo = float(input("Ingrese el ángulo de rotación en grados: "))
                nueva_imagen = rotar_imagen(imagen_actual, angulo)
                mostrar_imagenes(imagen_actual, nueva_imagen, f"Rotación {angulo}°")
                imagen_actual = nueva_imagen
                historial.append(imagen_actual.copy())
                print("Rotación aplicada.")

            elif opcion == "2":  # Escalar
                factor_x = float(input("Ingrese el factor de escala en X (máx. 5): "))
                factor_y = float(input("Ingrese el factor de escala en Y (máx. 5): "))
                nueva_imagen = escalar_imagen(imagen_actual, factor_x, factor_y)
                mostrar_imagenes(imagen_actual, nueva_imagen, f"Escalado {factor_x}x, {factor_y}y")
                imagen_actual = nueva_imagen
                historial.append(imagen_actual.copy())
                print("Escalado aplicado.")

            elif opcion == "3":  # Reflejar
                eje = input("Ingrese el eje de reflexión (horizontal/vertical): ").lower()
                nueva_imagen = reflejar_imagen(imagen_actual, eje)
                mostrar_imagenes(imagen_actual, nueva_imagen, f"Reflexión {eje}")
                imagen_actual = nueva_imagen
                historial.append(imagen_actual.copy())
                print("Reflexión aplicada.")

            elif opcion == "4":  # Trasladar
                desp_x = int(input("Ingrese el desplazamiento en X (píxeles): "))
                desp_y = int(input("Ingrese el desplazamiento en Y (píxeles): "))
                nueva_imagen = trasladar_imagen(imagen_actual, desp_x, desp_y)
                mostrar_imagenes(imagen_actual, nueva_imagen, f"Traslación ({desp_x}, {desp_y})")
                imagen_actual = nueva_imagen
                historial.append(imagen_actual.copy())
                print("Traslación aplicada.")

            elif opcion == "5":  # Deshacer
                if len(historial) > 1:
                    historial.pop()
                    imagen_actual = historial[-1].copy()
                    mostrar_imagenes(historial[-2], imagen_actual, "Deshacer")
                    print("Última transformación deshecha.")
                else:
                    print("No hay transformaciones para deshacer.")

            elif opcion == "6":  # Restaurar original
                mostrar_imagenes(imagen_actual, imagen_original, "Restauración a Original")
                imagen_actual = imagen_original.copy()
                historial = [imagen_original.copy()]
                print("Imagen restaurada al estado original.")

            elif opcion == "7":  # Guardar
                ruta_guardar = input("Ingrese la ruta donde guardar la imagen (con extensión .jpg o .png): ")
                cv2.imwrite(ruta_guardar, cv2.cvtColor(imagen_actual, cv2.COLOR_RGB2BGR))
                print(f"Imagen guardada en: {ruta_guardar}")

            elif opcion == "8":  # Salir
                print("¡Gracias por usar el programa!")
                break

            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 8.")

        except Exception as e:
            print(f"Error: {str(e)}")

    # Cerrar todas las ventanas al finalizar
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()