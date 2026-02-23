# ==========================================
# MODELOS DEL SISTEMA DE INVENTARIO
# POO + COLECCIONES
# ==========================================


class Producto:
    """
    Clase que representa un producto del inventario.
    """

    def __init__(self, id, nombre, cantidad, precio):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # -------------------------
    # GETTERS
    # -------------------------
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # -------------------------
    # SETTERS CON VALIDACIÓN
    # -------------------------
    def set_nombre(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = cantidad

    def set_precio(self, precio):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = precio

    def __str__(self):
        return f"[{self._id}] {self._nombre} - Cantidad: {self._cantidad} - Precio: ${self._precio}"


# ==========================================
# CLASE INVENTARIO
# UTILIZA COLECCIONES
# ==========================================

class Inventario:
    """
    Clase que gestiona los productos utilizando colecciones.
    """

    def __init__(self):
        # Diccionario principal: {id: Producto}
        self.productos = {}

        # Conjunto para control rápido de IDs únicos
        self.ids_registrados = set()

        # Tupla de campos del producto (estructura fija)
        self.campos = ("id", "nombre", "cantidad", "precio")

    # -------------------------
    # AGREGAR PRODUCTO
    # -------------------------
    def agregar_producto(self, producto):
        if producto.get_id() in self.ids_registrados:
            raise ValueError("El ID ya existe")

        self.productos[producto.get_id()] = producto
        self.ids_registrados.add(producto.get_id())

    # -------------------------
    # ELIMINAR PRODUCTO
    # -------------------------
    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
            self.ids_registrados.remove(id)
        else:
            raise ValueError("Producto no encontrado")

    # -------------------------
    # ACTUALIZAR PRODUCTO
    # -------------------------
    def actualizar_producto(self, id, cantidad=None, precio=None):
        if id not in self.productos:
            raise ValueError("Producto no encontrado")

        producto = self.productos[id]

        if cantidad is not None:
            producto.set_cantidad(cantidad)

        if precio is not None:
            producto.set_precio(precio)

    # -------------------------
    # BUSCAR POR NOMBRE
    # -------------------------
    def buscar_por_nombre(self, nombre):
        return [
            producto
            for producto in self.productos.values()
            if nombre.lower() in producto.get_nombre().lower()
        ]

    # -------------------------
    # MOSTRAR TODOS
    # -------------------------
    def mostrar_todos(self):
        return list(self.productos.values())