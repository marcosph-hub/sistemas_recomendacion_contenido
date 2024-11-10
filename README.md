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
#### TF
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
````python 
[
    {
        'aromas': 0.05263157894736842, 
        'include': 0.05263157894736842, 
        'tropical': 0.05263157894736842, ...
    },
    {
        'ripe': 0.058823529411764705, 
        'fruity,': 0.058823529411764705, 
        'wine': 0.058823529411764705, ...
    },
    { 
        ... 
    }
]
````
#### IDF
````python
def calculate_idf(documents):
    idf = {}
    total_documents = len(documents)
    for document in documents:
        for term in set(document):
            idf[term] = idf.get(term, 0) + 1
    return {term: math.log(total_documents / freq) for term, freq in idf.items()}

idf_dict = calculate_idf(all_tokens_matrix)
````
La función que calculará el valor `IDF` recibirá la lista de tokens de **cada** documento, cabe recordar que `all_tokens_matrix`contiene una posicion para cada documento con los tokens de dichos documentos devolverá un diccionario **término**-**valor**(IDF).
Lo primero será crear el diccionario `idf = {}` vacío donde almacenar la frecuencia de aparición de cada término en los documentos y calacular el número total de docuentos en el conjunto de documentos `total_documents = len(documents)`. 

El primer bucle `for` será para hacer iterar en cada documento que se convierte en un conjunto de palabras `for term in set(document)` para eliminar si hubiera algun caso repetido.

``idf[term] = idf.get(term, 0) + 1``: Actualiza el diccionario ``idf`` para cada término encontrado en el documento. La función ``get(term, 0)`` obtiene el valor actual del término si ya existe en el diccionario, o ``0`` si no está presente. Luego, incrementa su frecuencia por ``1``.

Después de recorrer todos los documentos y contar las frecuencias de los términos, el código utiliza una comprensión de diccionario para calcular el IDF para cada término:
- ``math.log(total_documents / freq)``: Calcula el valor de IDF de un término
Y ya una vez acabado el proceso de calculo  se devuelve un diccionario donde cada término es una clave y su correspondiente valor ``IDF``

Output:
`````python
{
    'palate': 1.3862943611198906, 
    'expressive,': 2.995732273553991, 
    'offer': 1.6094379124341003, 
    'unripened': 2.995732273553991, 
    'apple,': 2.995732273553991,
    ...
}
`````
#### TF-IDF

`````python	
def calculate_tfidf(tf, idf):
    return {term: tf_value * idf.get(term, 0) for term, tf_value in tf.items()}
`````

La función ``calculate_tfidf()`` calcula el ``TF-IDF ``para cada término en un documento, usando los valores de ``TF`` y I``DF`` comentados anteriormente, el valor ``TF-IDF`` se calcula multiplicando el valor de ``TF`` por el valor de ``IDF``. Se itera sobre todos los términos de ``tf`` donde para cad uno se obtiene el valor de ``TF````tf_value`` su valor de ``IDF``desde el diccionario ``idf``, si el término no está en idf, se asigna un valor ``0```. El resultado es un diccionario donde cada clave es un término y su valor es TF-IDF

Output:
````python
[
    {
        'aromas': 0.04202672085356692, 
        'include': 0.12118868910494977, 
        'tropical': 0.15767011966073635,
        ...
    },
    {
        'ripe': 0.11159529322858125, 
        'fruity,': 0.17621954550317592, 
        'wine': 0.08154672712469944,
        ...
    },
    {
        ...
    }
]
````
### Cálculo de la Similitud Coseno
#### Creación de la Matriz TF-IDF 
Se requiere crear una matriz de los valores TF-IDF para poder hacer el calculo de la Similitud Coseno 
````python
def create_tfidf_matrix(tokens_matrix,idf_dict):
    vocabulary = list(set(term for doc in tokens_matrix for term in doc))
    tfidf_matrix = []

    for token in tokens_matrix:
        tf = calculate_tf(token)
        tfidf = calculate_tfidf(tf, idf_dict)
        tfidf_vector = [tfidf.get(term, 0) for term in vocabulary]
        tfidf_matrix.append(tfidf_vector)

    return tfidf_matrix

tfidf_matrix = create_tfidf_matrix(all_tokens_matrix, idf_dict)
````
La función ``create_tfidf_matrix()`` genera una matriz de ``TF-IDF`` a partir de una lista de documentos, donde cada documento es representado como una lista de términos (``tokens``). La matriz resultante tiene una fila por documento y una columna por cada término en el vocabulario global.
- **Vocabulario Global**: a partir de la matriz de tokens calculada anteriormente se crea un vocabulario global, es decir, una lista de todos los términos únicos en el conjunto de documentos (sin duplicados).

Output de `vocabulary`:
````python 
['tradition,', 'tomatoey', 'sunnier', 'tobacco', 'spice', 'cheesy', 'informal', 'fruity,', 'apple,', 'wood', 'blossom', 'flavor',...
]
````
Con el vocabulario global a mano y para cada termino se calcula el `tf`y el ``tfidf`` con estos datos se constrye un vector que contiene los valores de ``TF-IDF`` de todos los términos en el vocabulario global. La función devuelve la matriz de ``TF-IDF`` (``tfidf_matrix``), donde cada fila representa un documento y cada columna representa un término del vocabulario global, con el valor de ``TF-IDF`` correspondiente a ese término en ese documento.

Output de la matriz de ``TF-IDF``:
````python
[
    [0, 0, 0.15767011966073635, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,...],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.17621954550317592,...], 
    [0, 0, 0, 0, 0, 0, 0, 0.1664295707529995, 0, 0, 0, 0, 0, 0,...],
    ...
]
````
**Nota**: que hayan 0 en la matriz indica que el término correspondiente no está presente en el documento o tiene una frecuencia nula para ese término en particular.

#### Cálculo de la Similitud Coseno

Una vez ya se tenga la matriz TF-IDF se procede al calculo de la Similitud Coseno
````python
def cosine_similarity(vec_a, vec_b):
    dot_product = np.dot(vec_a, vec_b)

    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    return dot_product / (norm_a * norm_b)
````
Esta función calcula la similitud coseno entre dos vectores vec_a y vec_b:
- `dot_product = np.dot(vec_a, vec_b)`: Calcula el producto punto entre los dos vectores vec_a y vec_b. El producto punto es una operación matemática que suma los productos de los elementos correspondientes de los dos vectores.
- ``norm_a = np.linalg.norm(vec_a) y norm_b = np.linalg.norm(vec_b)``: Calcula los modulos de ambos vectores
- `return dot_product / (norm_a * norm_b):`La similitud coseno se calcula dividiendo el producto punto entre los productos de las normas de los vectores. 

````python
def calculate_cosine_similarities(tfidf_matrix):
    num_documents = len(tfidf_matrix)
    cosine_similarities = np.zeros((num_documents, num_documents))  
    
    for i in range(num_documents):
        for j in range(i, num_documents):
            similarity = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])
            cosine_similarities[i][j] = similarity
            cosine_similarities[j][i] = similarity
    
    return cosine_similarities
````
Esta función calcula la matriz de similitudes coseno entre todos los documentos a partir de la matriz de ``TF-IDF``. La matriz de similitudes coseno es una matriz cuadrada donde cada celda (i, j) contiene la similitud coseno entre el documento i y el documento j.

- ``cosine_similarities = np.zeros((num_documents, num_documents))``: Crea una matriz de similitudes coseno inicializada con ceros. Esta matriz es de tamaño (num_documents, num_documents), donde cada celda almacenará la similitud coseno entre dos documentos.
- `similarity = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])`: Llama a la función cosine_similarity para calcular la similitud entre los documentos i y j.
- `cosine_similarities[i][j] = similarity` y `cosine_similarities[j][i] = similarity:` Asigna el valor de la similitud calculada en la matriz de similitudes. Se asigna en las posiciones (i, j) y (j, i) para asegurarse de que la matriz sea simétrica.

Despues de todo el calculo la función retorna  la matriz de similitudes coseno que contiene las similitudes entre todos los documentos.

Output:
