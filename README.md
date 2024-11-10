# Sistemas de Recomendacion. Modelo Basados en el Contenido

## Índice

- [Instrucciones de Instalación](#instrucciones-de-instalción)
    - [Requisitos](#requisitos)
    - [Instalación de Dependencia](#instalación-de-dependencias)
    - [Ejecución del Programa y Ayuda](#ejecución-del-programa-y-ayuda)

- [Descripción del Código Desarrollado](#descripción-del-código-desarrollado)
    - [Preprocesamiento de los Datos](#preprocesamiento-de-los-datos)
        - [Carga y procesamiento de los documentos. Funcion load_documets()](#carga-y-procesamiento-de-los-documentos-funcion-load_documentsdocuments)
        - [Carga y procesamiento de los stopwords. Funcion load_stopword()](#carga-y-procesamiento-de-los-stopwords-funcion-load_stopword)
        - [Carga y procesamiento de los lematización. Funcion load_lematization().](#carga-y-procesamiento-de-los-lematización-funcion-load_lematization)
        - [Tokenización de los documentos](#tokenización-de-los-documentos)
    - [Cálculo de TF, IDF y TF-IDF](#cálculo-de-tf-idf-y-tf-idf)
        - [TF](#tf)



## Instrucciones de Instalción

### Requisitos

- **Python** 3.8+
- **Entorno Virtual** _(Opcional pero recomendado)_
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
### Instalación de Dependencias
- **Numpy**: Para cálculos matemáticos y manipulación de matrices.
- **Pandas**: Para manipulación de datos y creación de tablas.
- **Math**: Proporciona funciones matemáticas avanzadas, como logaritmos y trigonometría.
- **Json**: Permite trabajar con datos JSON, facilitando la conversión entre cadenas JSON y objetos de Python.
- **Argparse**: Gestiona argumentos de línea de comandos, permitiendo configurar opciones al ejecutar un programa.

    ````shell
    pip install numpy pandas
**Nota**: math, json, y argparse son módulos integrados en Python y no requieren instalación adicional.

### Ejecución del programa y Ayuda
````shell
python .\src\main.py .\documents\documents-01.txt .\stop_words\stop-words-en.txt .\corpus\corpus-en.txt > .\result\recomendation_system.csv
````

Se requiere indicarle la ruta de los datos que necesita el programa para poder procesar los documentos. El programa cuenta con una opcion de ayuda _(-h, --help)_ que da más información sobre los argumentos que se espera pasarle al programa
`````shell
 ❯ python .\src\main.py -h
usage: main.py [-h] document_file stopwords_file lemmatization_file

Sistema de recomendación basado en el contenido

positional arguments:
  document_file       Archivo con los documentos
  stopwords_file      Archivo con las palabras de parada
  lemmatization_file  Archivo de lematización de términos

options:
  -h, --help          show this help message and exit
`````
## Descripción del Código Desarrollado.
### Preprocesamiento de los Datos.
El primer paso será procesar los datos que han sido pasados por argumentos en el main
````python
    parser = argparse.ArgumentParser(description="Sistema de recomendación basado en el contenido")
    parser.add_argument('document_file', help="Archivo con los documentos")
    parser.add_argument('stopwords_file', help="Archivo con las palabras de parada")
    parser.add_argument('lemmatization_file', help="Archivo de lematización de términos")
    args = parser.parse_args()
````
Simplemente `parser` es un objeto _ArgumentParser_ que guardará cada uno de los ficheros que ha indicado el usuario que quiere que se procese y mediante la función `add_argument` se irán agregando un argumento posicional al objeto `parser`.

- ``'document_file'``: Este es el primer argumento posicional. El valor que se pase al ejecutar el programa se guardará en la variable document_file.

- ``'stopwords_file'``: Este es el segundo argumento posicional. El valor que se pase al ejecutar el programa se guardará en la variable stopwords_file.

- ``'lemmatization_file'``: Este es el tercer argumento posicional. El valor que se pase se guardará en la variable lemmatization_file.

#### Carga y procesamiento de los documentos. Funcion load_documents().
Una vez el programa ya tenga el fichero de documentos se necesita procesar dicho fichero para poder separar todos los documentos que se encuentran en su interior
````python
document_container = laod_documents(args.document_file)
````
La función `load_documents()` recibe el nombre del fichero que contiene todos los documentos y los procesa para devolver una lista donde en cada posicion hay un documento
```python
def laod_documents(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]
```
Output:
````python
["Aromas include tropical fruit, broom, brimstone and dried herb. The palate isn't overly expressive, offering unripened apple, citrus and dried sage alongside brisk acidity.", "This is ripe and fruity, a wine that is smooth while still structured. Firm tannins are filled out with juicy red berry fruits and freshened with acidity. It's  already drinkable, although it will certainly be better from 2016.",...]
````
#### Carga y procesamiento de los stopwords. Funcion load_stopword().
````python
def load_stopwords(filename):
    with open(filename, 'r') as f:
        stopwords = set(f.read().splitlines())
    return stopwords
````
La función ``load_stopwords`` toma un parámetro ``filename``, que es el nombre o la ruta del archivo de texto que contiene las palabras de parada (stopwords). Lo primero se abrirá el archivo de manera segura mediante el uso del bloque ``with`` . Dentro de este bloque se crea una lista de cadenas que corresponde a cada elemento de una línea del archivo, con el uso del `set()` convierte esta lista en un conjunto, lo que elimina cualquier duplicado y retorna dicho conjunto.

Output:
````python
{'ignored', 'wherever', 'end', 'and', 'whole', 'corresponding', 'nine', 'her', 'hello', 'it', 'useful', 'inc', ...}
````

#### Carga y procesamiento de los lematización. Funcion load_lematization().
````python
def load_lematization(file_path):
    with open(file_path, 'r') as f:
        lematization = json.load(f)
    return lematization
````
Esta función simplemente se encargará de leer el archivo como u JSON y lo convertirá a un objeto python
Output:
````python
{
    'is': 'be', 
    'was': 'be', 
    'does': 'do', 
    'doing': 'do', 
    ...
}
````
#### Tokenización de los documentos
En este proceso se busca tener guardados cada palabra única (_tóken_) de cada uno de los documentos, para ello se creará una matriz que será una lista de listas de palabras claves.
````python
all_tokens_matrix = [process_document(doc, stopwords, lematization) for doc in document_container]
````
`all_tokens_matrix` será la estrucura de datos que contendrá los tokens de cada documento. Para cada documento dentro del fichero que contiene todos los documentos (`document_container`) se llamará a la función `process_documet()` al que se le pasará el documento en si, las palabras de parada, y el fichero de lematización. 
Output:
```python	
[
    ['aromas', 'include', 'tropical', 'fruit,', 'broom,', 'brimstone', 'dried', 'herb.', 'palate', 'overly', 'expressive,', 'offer', 'unripened', 'apple,', 'citrus', 'dried', 'sage', 'brisk', 'acidity.'], 
    ['ripe', 'fruity,', 'a', 'wine', 'smooth', 'structured.', 'firm', 'tannins', 'fill', 'juicy', 'red', 'berry', 'fruits', 'freshened', 'acidity.', 'drinkable,', '2016.'],
    [...]
]
```

### Cálculo de TF, IDF y TF-IDF
### TF
````python
tf_list = [calculate_tf(token) for token in all_tokens_matrix]
````
Esta línea utiliza una comprensión de lista para llamar a la función ``calculate_tf()`` en cada uno de los elementos de ``all_tokens_matrix()``, de manera que a la función que va a calcular el valor ``TF`` recibirá una lista de tokens para un documento determinado

````python
def calculate_tf(document_tokens):
    tf = {}
    for term in document_tokens:
        tf[term] = tf.get(term, 0) + 1
    total_terms = len(document_tokens)

    return {term: freq / total_terms for term, freq in tf.items()}
````

Esta función `calculate_tf` devolverá una lista de diccionarios, para cada elemento de la lista habrá un diccionario **término** - **valor**(TF). Primero se creará un diccionario vacío ``tf`` que almacenará la frecuencia de aparición de cada término dentro del documento. El bucle recorre cada término ``term`` en la lista ``document_tokens``. Para cada término, se actualiza su frecuencia en el diccionario ``tf``:

- ``tf.get(term, 0)``: Obtiene la frecuencia actual del término ``term`` en el diccionario ``tf``. Si el término no se ha encontrado previamente, se devuelve ``0``.

- ``tf[term] = tf.get(term, 0) + 1``: Se incrementa la frecuencia del término en el diccionario tf.

````python
return {term: freq / total_terms for term, freq in tf.items()}
````
Lo que va a retornar es un diccionario en el que cada clave es un término y el valor es la frecuenciadel término dividida entre el total de términos.

Output:
