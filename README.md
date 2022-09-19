# books_to_scrape

Este desafío consiste en realizar un scraping a una página web y almacenar la información en
un archivo con formato definido. Se debe desarrollar en Python, utilizando cualquier librería
necesaria. El código debe estar comentado y se debe incluir un script o un documento claro
que permita reproducir la solución.

La página web objetivo de este proyecto es http://books.toscrape.com. Los elementos
relevantes para la solución son las categorías (Travel, Mystery, Classics, etc.) y sus libros.

Requerido
El código entregado debe realizar lo siguiente:
1. Obtener todos los libros de la categoría Biography.  
2. Elegir 1 categoría al azar distinta a Biography, y obtener también todos sus libros.  
3. Para cada libro, extraer solo los siguientes campos, con el tipo de dato indicado:  
○ Título (str)  
○ Categoría (str)  
○ UPC (str)  
○ Precio (float)  
○ Cantidad de stock disponible (int)  
○ Rating (float)  
4. Guardar los elementos obtenidos en CSV o JSON.

Extras
● Utilizar Git durante el desarrollo de la solución.
● En el punto 4, si se eligió CSV, agregar JSON (y viceversa).
● Incorporar Docker en el proyecto.
● Agregar una API que permita lanzar una ejecución completa mediante GET o POST.
● Para cada elemento obtenido, agregar también su imagen.

Entregable
El candidato debe recibir este enunciado por email, y cuenta con 7 días corridos para
desarrollar una solución. Luego de este período, se debe responder a dicho email, adjuntando
un archivo comprimido en ZIP o GZ que contenga la versión final del proyecto. Se puede utilizar
la misma cadena de emails para realizar cualquier consulta.
