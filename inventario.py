# ==========================================================
# SISTEMA DE GESTIÓN DE INVENTARIO CON ARCHIVOS Y EXCEPCIONES
# ==========================================================

import os

ARCHIVO_INVENTARIO = "inventario.txt"


# ==========================================================
# CLASE PRODUCTO
# Representa cada elemento del inventario
# ==========================================================
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Convertir objeto a línea de archivo
    def a_linea(self):
        return f"{self.id},{self.nombre},{self.cantidad},{self.precio}"

    # Crear objeto desde línea de archivo
    @staticmethod
    def desde_linea(linea):
        partes = linea.strip().split(",")
        if len(partes) != 4:
            raise ValueError("Formato de línea inválido")
        return Producto(
            int(partes[0]),
            partes[1],
            int(partes[2]),
            float(partes[3])
        )


# ==========================================================
# CLASE INVENTARIO
# Gestiona los productos y su persistencia en archivo
# ==========================================================
class Inventario:

    def __init__(self, archivo=ARCHIVO_INVENTARIO):
        self.archivo = archivo
        self.productos = {}
        self.cargar_desde_archivo()

    # ------------------------------------------------------
    # CARGAR INVENTARIO DESDE ARCHIVO
    # ------------------------------------------------------
    def cargar_desde_archivo(self):
        """
        Lee el archivo de inventario y reconstruye los productos.
        Si el archivo no existe, lo crea automáticamente.
        """
        try:
            if not os.path.exists(self.archivo):
                open(self.archivo, "w").close()
                print("Archivo de inventario creado automáticamente.")
                return

            with open(self.archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip() == "":
                        continue
                    try:
                        producto = Producto.desde_linea(linea)
                        self.productos[producto.id] = producto
                    except ValueError:
                        print("Advertencia: línea corrupta ignorada:", linea.strip())

            print("Inventario cargado correctamente.")

        except PermissionError:
            print("ERROR: No hay permisos para leer el archivo.")
        except Exception as e:
            print("Error inesperado al cargar archivo:", e)

    # ------------------------------------------------------
    # GUARDAR INVENTARIO EN ARCHIVO
    # ------------------------------------------------------
    def guardar_en_archivo(self):
        """
        Guarda todos los productos en el archivo.
        """
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                for producto in self.productos.values():
                    f.write(producto.a_linea() + "\n")

            print("Inventario guardado correctamente.")

        except PermissionError:
            print("ERROR: No hay permisos de escritura en el archivo.")
        except Exception as e:
            print("Error inesperado al guardar:", e)

    # ------------------------------------------------------
    # AÑADIR PRODUCTO
    # ------------------------------------------------------
    def agregar_producto(self, producto):
        if producto.id in self.productos:
            print("ERROR: Ya existe un producto con ese ID.")
            return
        self.productos[producto.id] = producto
        self.guardar_en_archivo()
        print("Producto añadido correctamente.")

    # ------------------------------------------------------
    # ACTUALIZAR PRODUCTO
    # ------------------------------------------------------
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto not in self.productos:
            print("Producto no encontrado.")
            return

        if cantidad is not None:
            self.productos[id_producto].cantidad = cantidad

        if precio is not None:
            self.productos[id_producto].precio = precio

        self.guardar_en_archivo()
        print("Producto actualizado correctamente.")

    # ------------------------------------------------------
    # ELIMINAR PRODUCTO
    # ------------------------------------------------------
    def eliminar_producto(self, id_producto):
        if id_producto not in self.productos:
            print("Producto no encontrado.")
            return

        del self.productos[id_producto]
        self.guardar_en_archivo()
        print("Producto eliminado correctamente.")

    # ------------------------------------------------------
    # MOSTRAR INVENTARIO
    # ------------------------------------------------------
    def mostrar(self):
        if not self.productos:
            print("Inventario vacío.")
            return

        print("\n=== INVENTARIO ===")
        for p in self.productos.values():
            print(f"ID:{p.id} | {p.nombre} | Cantidad:{p.cantidad} | Precio:{p.precio}")


# ==========================================================
# INTERFAZ DE CONSOLA
# ==========================================================
def menu():
    inventario = Inventario()

    while True:
        print("\n===== SISTEMA INVENTARIO =====")
        print("1. Mostrar productos")
        print("2. Agregar producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Salir")

        opcion = input("Seleccione opción: ")

        if opcion == "1":
            inventario.mostrar()

        elif opcion == "2":
            try:
                idp = int(input("ID: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                inventario.agregar_producto(
                    Producto(idp, nombre, cantidad, precio)
                )
            except ValueError:
                print("Error: datos inválidos.")

        elif opcion == "3":
            try:
                idp = int(input("ID producto: "))
                cantidad = input("Nueva cantidad (enter para omitir): ")
                precio = input("Nuevo precio (enter para omitir): ")

                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None

                inventario.actualizar_producto(idp, cantidad, precio)
            except ValueError:
                print("Datos inválidos.")

        elif opcion == "4":
            try:
                idp = int(input("ID a eliminar: "))
                inventario.eliminar_producto(idp)
            except ValueError:
                print("ID inválido.")

        elif opcion == "5":
            print("Sistema finalizado.")
            break

        else:
            print("Opción inválida.")


# ==========================================================
# EJECUCIÓN PRINCIPAL
# ==========================================================
if __name__ == "__main__":
    menu()
    