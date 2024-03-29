#Proyecto: Página de Venta de Productos de Fútbol

Autor: María Celeste Campagnoli Martinez
Fecha: 28/03/2024
Versión: 1.0

###Objetivo:
El objetivo del proyecto es proporcionar una interfaz para una tienda web de productos de fútbol.

###Consideraciones:
Instalar jazzmin --> pip install -U django-jazzmin

###Modelos usados:
- **Etiqueta**: objetos Etiqueta que se le pueden atribuir a cada producto (relación many-to-many). Esto permite que se puedan filtrar todos los productos por la etiqueta que tienen, y que al entrar a los detalles del producto se puedan ver todas las que tiene atribuidas. El administrador las puede cambiar, agregar nuevas, o borrar.
- **Producto**: contiene los detalles del producto: nombre, descripción, precio, imagen, etiquetas, código y tipo (la categoría a la que pertenece). El administrador puede crear, editar, o borrar.
- **Avatar**: la imagen de perfil del usuario, quien la puede cambiar.
- **Comentario**: modelo con campos autor, fecha, comentario, avatar y producto, que permite que los usuarios puedan crear comentarios sobre un producto (se muestran debajo de éste en la página de detalles del producto), editarlos y borrarlos (sólo los de su autoría).

###USUARIOS:
usuario: admin
clave: 1234

usuario_test: Ciclon123
clave: aeiou123
