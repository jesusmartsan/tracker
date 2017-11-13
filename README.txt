Inicio:
- 2 opciones: 
	1 - Calibrar: Puesta en estacion - alineación polar, seleccionar cuando el teles esté apuntando a la polar
	2 - Buscar: Busqueda de astro, muestra una lista con las opciones disponibles y permite seleccionar una de ellas
	3 - Introducir coordenadas a mano RA(H-M-S)/DEC(H-M-S)
	4 - Ir a la opción seleccionada y seguir: Esto se hace en un hilo aparte (a), para que se puedan seguir metiendo opciones.
	5 - Parar seguimiento: Para el hilo creado en el punto anterior
	
(a):
- Necesitamos: 
	1.- Coordenadas del astro donde estamos apuntando
	2.- Coordenadas del astro al que queremos ir
	
	- Una vez tengamos lo anterior, calculamos la diferencia en segundos de arco,tanto en RA como en DEC
	- Movemos el eje correspondiente la cantidad de segundos calculada anteriormente.
	- Activamos el seguimiento y nos quedamos con el identificador del hilo para poder pararlo cuando sea necesario
	
Ejemplo punto 3/4:
	- Estrella polar: 2-31-51/89-15-51 = 9111/(89*60+51)*60+51 = 323460 segundos
	- Aldebaran: 4-35-55/16-30-30 = 16555/59430