# =========================
#  SISTEMA DE INVENTARIO
#  Archivo: menu.py
# =========================

def ejecutar_menu():
    """
    Función principal que controla el menú del sistema de inventario.
    Se ejecuta en un bucle infinito hasta que el usuario elija salir (opción 0).
    """

    # Inventario en memoria (lista de diccionarios).
    # Nota: si tu tarea exige guardar en archivo/DB, esto se reemplaza por persistencia.
    inventario = []

    while True:
        # -------------------------
        # Mostrar menú de opciones
        # -------------------------
        print("\n===== MENÚ INVENTARIO =====")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("0. Salir")

        opcion = input("Elige una opción: ").strip()

        # -------------------------
        # Opción 1: Agregar producto
        # -------------------------
        if opcion == "1":
            print("\n--- Agregar producto ---")

            # Solicita datos del producto
            try:
                producto_id = int(input("ID: ").strip())
            except ValueError:
                print("⚠️ ID inválido. Debe ser un número entero.")
                continue

            # Validar que el ID no exista ya
            id_existe = any(p["id"] == producto_id for p in inventario)
            if id_existe:
                print("⚠️ Ese ID ya existe. Usa otro.")
                continue

            nombre = input("Nombre: ").strip()
            if not nombre:
                print("⚠️ El nombre no puede estar vacío.")
                continue

            try:
                cantidad = int(input("Cantidad: ").strip())
                precio = float(input("Precio: ").strip())
            except ValueError:
                print("⚠️ Cantidad y precio deben ser numéricos.")
                continue

            # Agregar al inventario
            inventario.append({
                "id": producto_id,
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio
            })

            print("✅ Producto agregado correctamente")

        # -------------------------
        # Opción 2: Eliminar producto
        # -------------------------
        elif opcion == "2":
            print("\n--- Eliminar producto ---")

            if not inventario:
                print("⚠️ Inventario vacío")
                continue

            try:
                producto_id = int(input("ID del producto a eliminar: ").strip())
            except ValueError:
                print("⚠️ ID inválido. Debe ser un número entero.")
                continue

            # Buscar y eliminar
            eliminado = False
            for i, p in enumerate(inventario):
                if p["id"] == producto_id:
                    inventario.pop(i)
                    eliminado = True
                    break

            if eliminado:
                print("✅ Producto eliminado correctamente")
            else:
                print(f"⚠️ No existe el producto con ID: {producto_id}")

        # -------------------------
        # Opción 3: Actualizar producto
        # -------------------------
        elif opcion == "3":
            print("\n--- Actualizar producto ---")

            if not inventario:
                print("⚠️ Inventario vacío")
                continue

            try:
                producto_id = int(input("ID del producto a actualizar: ").strip())
            except ValueError:
                print("⚠️ ID inválido. Debe ser un número entero.")
                continue

            # Buscar producto
            producto = None
            for p in inventario:
                if p["id"] == producto_id:
                    producto = p
                    break

            if producto is None:
                print(f"⚠️ No existe el producto con ID: {producto_id}")
                continue

            # Permite dejar Enter para no cambiar
            nueva_cantidad = input("Nueva cantidad (Enter para no cambiar): ").strip()
            nuevo_precio = input("Nuevo precio (Enter para no cambiar): ").strip()

            # Actualizar cantidad si corresponde
            if nueva_cantidad:
                try:
                    producto["cantidad"] = int(nueva_cantidad)
                except ValueError:
                    print("⚠️ Cantidad inválida. Debe ser un entero.")
                    continue

            # Actualizar precio si corresponde
            if nuevo_precio:
                try:
                    producto["precio"] = float(nuevo_precio)
                except ValueError:
                    print("⚠️ Precio inválido. Debe ser numérico.")
                    continue

            print("✅ Producto actualizado correctamente")

        # -------------------------
        # Opción 4: Buscar producto por nombre
        # -------------------------
        elif opcion == "4":
            print("\n--- Buscar producto por nombre ---")

            if not inventario:
                print("⚠️ Inventario vacío")
                continue

            termino = input("Buscar por nombre: ").strip().lower()
            if not termino:
                print("⚠️ Debes escribir un nombre o parte del nombre.")
                continue

            resultados = [p for p in inventario if termino in p["nombre"].lower()]

            if resultados:
                print("✅ Resultados:")
                for p in resultados:
                    print(f'[{p["id"]}] {p["nombre"]} - Cantidad: {p["cantidad"]} - Precio: ${p["precio"]}')
            else:
                print(f"⚠️ No se encontraron productos con: {termino}")

        # -------------------------
        # Opción 5: Mostrar todos los productos
        # -------------------------
        elif opcion == "5":
            print("\n--- Mostrar todos los productos ---")

            if not inventario:
                print("⚠️ Inventario vacío")
            else:
                print("📦 Inventario:")
                for p in inventario:
                    print(f'[{p["id"]}] {p["nombre"]} - Cantidad: {p["cantidad"]} - Precio: ${p["precio"]}')

        # -------------------------
        # Opción 0: Salir del sistema
        # -------------------------
        elif opcion == "0":
            print("👋 Saliendo...")
            break

        # -------------------------
        # Opción inválida
        # -------------------------
        else:
            print("⚠️ Opción inválida. Intente nuevamente.")


# Punto de entrada del programa
if __name__ == "__main__":
    ejecutar_menu()