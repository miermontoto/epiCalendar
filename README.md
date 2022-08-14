# epiCalendar

Fork de [un script de Python](https://github.com/Bimo99B9/autoUniCalendar) que convierte el calendario del SIES a formato CSV para poder exportarlo a otros calendarios.

## Uso

Para utilizar el script, se puede utilizar tanto [la versión web](https://epicalendar.herokuapp.com) como el script en local.

### Página web (recomendado)

Para utilizar la web, solo hay que [obtener una cookie](https://github.com/miermontoto/epiCalendar/edit/main/README.md#obtener-jsessionid) desde el SIES y hacer click en "Generar".

### Script

- Para utilizar el script sin necesidad de página web, hay que [descargar la última versión del proyecto](https://github.com/miermontoto/epiCalendar/archive/refs/heads/main.zip) o hacer clone del repositorio:

  ```git clone https://github.com/miermontoto/epiCalendar```
- Una vez descargado, el script se ejecuta normalmente como cualquier otro input de Python: `python3 epiCalendar.py`
  - El script admite parámetros de entrada, tanto flags como la propia cookie necesaria.

Necesita el paquete [`requests`](https://pypi.org/project/requests/).

## Obtener JSESSIONID

Para obtener tu `JSESSIONID`, inicia sesión en el SIES y pulsa `F12` o `Ctrl+Shift+I`.

- En Chrome y derivados (Opera, Edge, Brave), accede al menú `Application` y dentro de `Cookies / https://sies.uniovi.es`...
- En Firefox, accede al menú `Storage` y dentro de `Cookies / https://sies.uniovi.es`...

... copia la cookie `JSESSIONID`. Si hay varias, busca la que tenga como `Path`: `/serviciosacademicos`.

## Modificaciones

### Filtrado de localización (solo EPI Gijón)

El "filtrado de localización" corrige automáticamente el nombre de las clases insertadas en el calendario del SIES.
Ejemplos de esto son:

- `Aula As-1` → `AS-1`
- `Aula B5` → `AN-B5`
- `Aula de Informática B1` → `AN-B1`
- `Sala Informática S8` → `AN-S8`
- `Laboratorio 1.5.01 Tecnología y Microprocesadores` → `EP-1.5.01`

### Filtrado de tipos de clase

Se añade al final de cada clase el tipo de clase, como por ejemplo: `Cálculo (CEX)`, o `Fundamentos de Informática (PL1)`.

- `CEX` cuando es una clase expositiva / teoría.
- `PAx`cuando es un práctica de aula, incluyendo el número del grupo.
- `PLx` cuando es una práctica de laboratorio, incluyendo el número del grupo.
- `TGx` cuando es una tutoría grupal, incluyendo el número del grupo.

Se incluye el grupo excepto en clases de teoría.

### Estadísticas

El script recoge varias estadísticas sobre el calendario:

- Número de clases.
- Número de horas.
- Número de clases por tipo de clase.
- Número de clases por aula.

Para activar las estadísticas se debe introducir el parámetro `--stats` o `-s`.

### Flags

- `[-h | --help]` para mostrar el diálogo de ayuda.
- `[-o | --output <filename>]` para cambiar el nombre del archivo resultante.
- `[--disable-location-parsing]` para desactivar el filtrado de localización específico de la EPI.
- `[--disable-experimental-location-parsing]` para desactivar el filtrado experimental específico de la EPI.
- `[--disable-class-type-parsing]` para desactivar el filtrado del tipo de clases.
- `[-s | --stats | --enable-statistics]` para activar las estadísticas al final del script.

[epiCalendar](https://github.com/miermontoto/epiCalendar), a fork of [autoUniCalendar](https://github.com/BimoBB9B/autoUniCalendar), 2022 by [Juan Mier](https://github.com/miermontoto) is licensed under [CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1)
