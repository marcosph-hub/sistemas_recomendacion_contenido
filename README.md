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
        - [IDF](#idf)
        - [TF-IDF](#tf-idf)
    - [Similitud Coseno](#cálculo-de-la-similitud-coseno)
        - [Creación de la Matriz TF-IDF](#creación-de-la-matriz-tf-idf)
        - [Cálculo de la Similitud Coseno](#cálculo-de-la-similitud-coseno)
- [Resultado Obtenido del Programa](#resultado-obtenido-del-programa)




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
### Similitud Coseno
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
````csv 
             Document 1  Document 2  ...  Document 19  Document 20
Document 1     1.000000    0.022620  ...     0.014243     0.036087
Document 2     0.022620    1.000000  ...     0.016729     0.051006
Document 3     0.000000    0.018088  ...     0.000000     0.067228
Document 4     0.014353    0.001435  ...     0.051725     0.078128
Document 5     0.000000    0.002008  ...     0.000000     0.001612
Document 6     0.044568    0.020251  ...     0.015585     0.036612
Document 7     0.005112    0.024872  ...     0.050580     0.024720
Document 8     0.029460    0.073960  ...     0.044596     0.028311
Document 9     0.080476    0.000000  ...     0.021573     0.027165
Document 10    0.000000    0.037367  ...     0.000000     0.000674
Document 11    0.044786    0.021273  ...     0.033122     0.001953
Document 12    0.021487    0.088590  ...     0.054606     0.061606
Document 13    0.045663    0.048041  ...     0.018353     0.081076
Document 14    0.000000    0.024341  ...     0.022338     0.038627
Document 15    0.000000    0.000711  ...     0.021054     0.027082
Document 16    0.030384    0.019436  ...     0.022471     0.015427
Document 17    0.004165    0.055825  ...     0.003081     0.004886
Document 18    0.029164    0.000000  ...     0.005643     0.007106
Document 19    0.014243    0.016729  ...     1.000000     0.066527
Document 20    0.036087    0.051006  ...     0.066527     1.000000
````

## Resultado Obtenido del Programa
La salida del programa lo hace a través de un fichero `./result/recomendation_system.csv`
Output ``recomendation_system.csv``:
```csv
Documento 1
    Index         Term        TF       IDF    TF-IDF
0       1       aromas  0.052632  0.798508  0.042027
1       2      include  0.052632  2.302585  0.121189
2       3     tropical  0.052632  2.995732  0.157670
3       4       fruit,  0.052632  1.897120  0.099848
4       5       broom,  0.052632  2.995732  0.157670
5       6    brimstone  0.052632  2.995732  0.157670
6       7        dried  0.105263  2.302585  0.242377
7       8        herb.  0.052632  2.995732  0.157670
8       9       palate  0.052632  1.386294  0.072963
9      10       overly  0.052632  2.995732  0.157670
10     11  expressive,  0.052632  2.995732  0.157670
11     12        offer  0.052632  1.609438  0.084707
12     13    unripened  0.052632  2.995732  0.157670
13     14       apple,  0.052632  2.995732  0.157670
14     15       citrus  0.052632  2.302585  0.121189
15     16         sage  0.052632  2.995732  0.157670
16     17        brisk  0.052632  2.995732  0.157670
17     18     acidity.  0.052632  1.609438  0.084707

Documento 2
    Index         Term        TF       IDF    TF-IDF
0       1         ripe  0.058824  1.897120  0.111595
1       2      fruity,  0.058824  2.995732  0.176220
2       3            a  0.058824  0.287682  0.016922
3       4         wine  0.058824  1.386294  0.081547
4       5       smooth  0.058824  2.995732  0.176220
5       6  structured.  0.058824  2.995732  0.176220
6       7         firm  0.058824  1.897120  0.111595
7       8      tannins  0.058824  2.302585  0.135446
8       9         fill  0.058824  2.995732  0.176220
9      10        juicy  0.058824  1.897120  0.111595
10     11          red  0.058824  1.609438  0.094673
11     12        berry  0.058824  2.995732  0.176220
12     13       fruits  0.058824  1.897120  0.111595
13     14    freshened  0.058824  2.995732  0.176220
14     15     acidity.  0.058824  1.609438  0.094673
15     16   drinkable,  0.058824  2.995732  0.176220
16     17        2016.  0.058824  2.995732  0.176220

Documento 3
    Index             Term        TF       IDF    TF-IDF
0       1             tart  0.055556  1.897120  0.105396
1       2          snappy,  0.055556  2.995732  0.166430
2       3          flavors  0.055556  1.203973  0.066887
3       4             lime  0.055556  2.995732  0.166430
4       5            flesh  0.055556  2.995732  0.166430
5       6             rind  0.055556  2.995732  0.166430
6       7        dominate.  0.055556  2.995732  0.166430
7       8            green  0.055556  1.609438  0.089413
8       9        pineapple  0.055556  1.897120  0.105396
9      10            pokes  0.055556  2.995732  0.166430
10     11         through,  0.055556  2.302585  0.127921
11     12            crisp  0.055556  1.897120  0.105396
12     13          acidity  0.055556  1.609438  0.089413
13     14     underscoring  0.055556  2.995732  0.166430
14     15         flavors.  0.055556  2.995732  0.166430
15     16             wine  0.055556  1.386294  0.077016
16     17  stainless-steel  0.055556  2.995732  0.166430
17     18       fermented.  0.055556  2.995732  0.166430
Documento 4
    Index            Term        TF       IDF    TF-IDF
0       1       pineapple  0.045455  1.897120  0.086233
1       2           rind,  0.045455  2.995732  0.136170
2       3           lemon  0.045455  2.995732  0.136170
3       4            pith  0.045455  2.995732  0.136170
4       5          orange  0.045455  2.302585  0.104663
5       6         blossom  0.045455  2.995732  0.136170
6       7           start  0.045455  2.995732  0.136170
7       8         aromas.  0.045455  2.995732  0.136170
8       9          palate  0.045455  1.386294  0.063013
9      10               a  0.090909  0.287682  0.026153
10     11            bite  0.045455  2.302585  0.104663
11     12        opulent,  0.045455  2.995732  0.136170
12     13            note  0.045455  1.386294  0.063013
13     14  honey-drizzled  0.045455  2.995732  0.136170
14     15           guava  0.045455  2.995732  0.136170
15     16           mango  0.045455  2.995732  0.136170
16     17            give  0.045455  2.302585  0.104663
17     18        slightly  0.045455  1.897120  0.086233
18     19     astringent,  0.045455  2.302585  0.104663
19     20         semidry  0.045455  2.995732  0.136170
20     21         finish.  0.045455  1.897120  0.086233
Documento 5
    Index              Term        TF       IDF    TF-IDF
0       1           regular  0.045455  2.995732  0.136170
1       2          bottling  0.045455  2.995732  0.136170
2       3             2012,  0.045455  2.995732  0.136170
3       4             rough  0.045455  2.995732  0.136170
4       5           tannic,  0.045455  2.302585  0.104663
5       6           rustic,  0.045455  2.995732  0.136170
6       7           earthy,  0.045455  2.995732  0.136170
7       8            herbal  0.045455  2.302585  0.104663
8       9  characteristics.  0.045455  2.995732  0.136170
9      10      nonetheless,  0.045455  2.995732  0.136170
10     11                 a  0.136364  0.287682  0.039229
11     12        pleasantly  0.045455  2.995732  0.136170
12     13           unfussy  0.045455  2.995732  0.136170
13     14           country  0.045455  2.995732  0.136170
14     15             wine,  0.045455  1.897120  0.086233
15     16              good  0.045455  2.302585  0.104663
16     17         companion  0.045455  2.995732  0.136170
17     18            hearty  0.045455  2.995732  0.136170
18     19            winter  0.045455  2.995732  0.136170
19     20             stew.  0.045455  2.995732  0.136170
Documento 6
    Index          Term        TF       IDF    TF-IDF
0       1    blackberry  0.035714  2.302585  0.082235
1       2     raspberry  0.035714  2.995732  0.106990
2       3        aromas  0.035714  0.798508  0.028518
3       4          show  0.035714  2.995732  0.106990
4       5             a  0.035714  0.287682  0.010274
5       6       typical  0.035714  2.995732  0.106990
6       7      navarran  0.035714  2.995732  0.106990
7       8         whiff  0.035714  2.995732  0.106990
8       9         green  0.035714  1.609438  0.057480
9      10         herbs  0.035714  2.995732  0.106990
10     11          and,  0.035714  2.995732  0.106990
11     12         case,  0.035714  2.995732  0.106990
12     13  horseradish.  0.035714  2.995732  0.106990
13     14        mouth,  0.035714  2.995732  0.106990
14     15          full  0.035714  2.995732  0.106990
15     16       bodied,  0.035714  2.995732  0.106990
16     17      tomatoey  0.035714  2.995732  0.106990
17     18      acidity.  0.035714  1.609438  0.057480
18     19        spicy,  0.035714  2.302585  0.082235
19     20        herbal  0.035714  2.302585  0.082235
20     21       flavors  0.035714  1.203973  0.042999
21     22    complement  0.035714  2.995732  0.106990
22     23          dark  0.035714  2.302585  0.082235
23     24          plum  0.035714  1.609438  0.057480
24     25        fruit,  0.035714  1.897120  0.067754
25     26        finish  0.035714  1.897120  0.067754
26     27         fresh  0.035714  1.897120  0.067754
27     28       grabby.  0.035714  2.995732  0.106990
Documento 7
    Index      Term        TF       IDF    TF-IDF
0       1         a  0.052632  0.287682  0.015141
1       2   bright,  0.052632  2.995732  0.157670
2       3  informal  0.052632  2.995732  0.157670
3       4       red  0.052632  1.609438  0.084707
4       5      open  0.052632  2.302585  0.121189
5       6    aromas  0.052632  0.798508  0.042027
6       7   candied  0.052632  2.995732  0.157670
7       8    berry,  0.052632  2.995732  0.157670
8       9     white  0.052632  2.995732  0.157670
9      10    pepper  0.052632  2.995732  0.157670
10     11    savory  0.052632  2.302585  0.121189
11     12      herb  0.052632  2.995732  0.157670
12     13     carry  0.052632  1.897120  0.099848
13     14   palate.  0.052632  2.995732  0.157670
14     15   balance  0.052632  1.897120  0.099848
15     16     fresh  0.052632  1.897120  0.099848
16     17   acidity  0.052632  1.609438  0.084707
17     18      soft  0.052632  2.995732  0.157670
18     19  tannins.  0.052632  2.995732  0.157670
Documento 8
    Index        Term        TF       IDF    TF-IDF
0       1         dry  0.083333  1.609438  0.134120
1       2    restrain  0.083333  2.302585  0.191882
2       3        wine  0.083333  1.386294  0.115525
3       4       offer  0.083333  1.609438  0.134120
4       5       spice  0.083333  2.995732  0.249644
5       6  profusion.  0.083333  2.995732  0.249644
6       7     balance  0.083333  1.897120  0.158093
7       8     acidity  0.083333  1.609438  0.134120
8       9           a  0.083333  0.287682  0.023974
9      10        firm  0.083333  1.897120  0.158093
10     11    texture,  0.083333  2.995732  0.249644
11     12       food.  0.083333  2.995732  0.249644
Documento 9
    Index        Term        TF       IDF    TF-IDF
0       1      savory  0.058824  2.302585  0.135446
1       2       dried  0.058824  2.302585  0.135446
2       3       thyme  0.058824  2.995732  0.176220
3       4        note  0.058824  1.386294  0.081547
4       5      accent  0.058824  2.995732  0.176220
5       6     sunnier  0.058824  2.995732  0.176220
6       7     flavors  0.058824  1.203973  0.070822
7       8    preserve  0.058824  2.995732  0.176220
8       9       peach  0.058824  2.995732  0.176220
9      10      brisk,  0.058824  2.995732  0.176220
10     11     off-dry  0.058824  2.995732  0.176220
11     12       wine.  0.058824  2.995732  0.176220
12     13      fruity  0.058824  2.995732  0.176220
13     14      fresh,  0.058824  2.995732  0.176220
14     15    elegant,  0.058824  2.995732  0.176220
15     16   sprightly  0.058824  2.995732  0.176220
16     17  footprint.  0.058824  2.995732  0.176220
Documento 10
    Index      Term        TF       IDF    TF-IDF
0       1     great  0.058824  2.995732  0.176220
1       2     depth  0.058824  2.995732  0.176220
2       3    flavor  0.058824  2.302585  0.135446
3       4     fresh  0.058824  1.897120  0.111595
4       5     apple  0.058824  2.302585  0.135446
5       6      pear  0.058824  2.302585  0.135446
6       7    fruits  0.058824  1.897120  0.111595
7       8     touch  0.058824  2.995732  0.176220
8       9    spice.  0.058824  2.995732  0.176220
9      10       dry  0.058824  1.609438  0.094673
10     11   balance  0.058824  1.897120  0.111595
11     12   acidity  0.058824  1.609438  0.094673
12     13         a  0.058824  0.287682  0.016922
13     14     crisp  0.058824  1.897120  0.111595
14     15  texture.  0.058824  2.995732  0.176220
15     16     drink  0.058824  2.995732  0.176220
16     17      now.  0.058824  2.995732  0.176220
Documento 11
    Index         Term        TF       IDF    TF-IDF
0       1            a  0.157895  0.287682  0.045423
1       2          dry  0.052632  1.609438  0.084707
2       3        wine,  0.052632  1.897120  0.099848
3       4       spicy,  0.052632  2.302585  0.121189
4       5       tight,  0.052632  2.995732  0.157670
5       6         taut  0.052632  2.995732  0.157670
6       7      texture  0.052632  2.995732  0.157670
7       8     strongly  0.052632  2.995732  0.157670
8       9      mineral  0.052632  2.995732  0.157670
9      10    character  0.052632  2.302585  0.121189
10     11      layered  0.052632  2.995732  0.157670
11     12       citrus  0.052632  2.302585  0.121189
12     13      pepper.  0.052632  2.302585  0.121189
13     14         food  0.052632  2.995732  0.157670
14     15         wine  0.052632  1.386294  0.072963
15     16        crisp  0.052632  1.897120  0.099848
16     17  aftertaste.  0.052632  2.995732  0.157670
Documento 12
    Index       Term        TF       IDF    TF-IDF
0       1   slightly  0.055556  1.897120  0.105396
1       2   reduced,  0.055556  2.995732  0.166430
2       3       wine  0.055556  1.386294  0.077016
3       4      offer  0.055556  1.609438  0.089413
4       5          a  0.055556  0.287682  0.015982
5       6    chalky,  0.055556  2.995732  0.166430
6       7     tannic  0.055556  2.995732  0.166430
7       8   backbone  0.055556  2.995732  0.166430
8       9      juicy  0.055556  1.897120  0.105396
9      10  explosion  0.055556  2.995732  0.166430
10     11       rich  0.055556  2.995732  0.166430
11     12      black  0.055556  2.302585  0.127921
12     13    cherry,  0.055556  2.995732  0.166430
13     14   accented  0.055556  2.995732  0.166430
14     15       firm  0.055556  1.897120  0.105396
15     16        oak  0.055556  1.609438  0.089413
16     17      cigar  0.055556  2.302585  0.127921
17     18       box.  0.055556  2.995732  0.166430
Documento 13
    Index         Term        TF       IDF    TF-IDF
0       1     dominate  0.045455  2.302585  0.104663
1       2          oak  0.045455  1.609438  0.073156
2       3   oak-driven  0.045455  2.302585  0.104663
3       4       aromas  0.045455  0.798508  0.036296
4       5      include  0.045455  2.302585  0.104663
5       6      roasted  0.045455  2.995732  0.136170
6       7       coffee  0.045455  2.995732  0.136170
7       8        bean,  0.045455  2.995732  0.136170
8       9    espresso,  0.045455  2.995732  0.136170
9      10      coconut  0.045455  2.995732  0.136170
10     11      vanilla  0.045455  2.302585  0.104663
11     12        carry  0.045455  1.897120  0.086233
12     13      palate,  0.045455  2.302585  0.104663
13     14         plum  0.045455  1.609438  0.073156
14     15   chocolate.  0.045455  2.995732  0.136170
15     16  astringent,  0.045455  2.302585  0.104663
16     17       drying  0.045455  2.995732  0.136170
17     18      tannins  0.045455  2.302585  0.104663
18     19         give  0.045455  2.302585  0.104663
19     20            a  0.045455  0.287682  0.013076
20     21       abrupt  0.045455  2.995732  0.136170
21     22      finish.  0.045455  1.897120  0.086233
Documento 14
    Index          Term       TF       IDF    TF-IDF
0       1         build  0.03125  2.995732  0.093617
1       2           150  0.03125  2.995732  0.093617
2       3         years  0.03125  2.995732  0.093617
3       4   generations  0.03125  2.995732  0.093617
4       5    winemaking  0.03125  2.995732  0.093617
5       6    tradition,  0.03125  2.995732  0.093617
6       7        winery  0.03125  2.995732  0.093617
7       8        trends  0.03125  2.995732  0.093617
8       9             a  0.03125  0.287682  0.008990
9      10        leaner  0.03125  2.995732  0.093617
10     11        style,  0.03125  2.995732  0.093617
11     12       classic  0.03125  2.995732  0.093617
12     13    california  0.03125  2.995732  0.093617
13     14   buttercream  0.03125  2.995732  0.093617
14     15         aroma  0.03125  2.995732  0.093617
15     16           cut  0.03125  2.995732  0.093617
16     17          tart  0.03125  1.897120  0.059285
17     18         green  0.03125  1.609438  0.050295
18     19        apple.  0.03125  2.995732  0.093617
19     20          good  0.03125  2.302585  0.071956
20     21      everyday  0.03125  2.995732  0.093617
21     22       sipping  0.03125  2.995732  0.093617
22     23         wine,  0.03125  1.897120  0.059285
23     24       flavors  0.03125  1.203973  0.037624
24     25         range  0.03125  2.995732  0.093617
25     26          pear  0.03125  2.302585  0.071956
26     27        barely  0.03125  2.995732  0.093617
27     28          ripe  0.03125  1.897120  0.059285
28     29     pineapple  0.03125  1.897120  0.059285
29     30         prove  0.03125  2.995732  0.093617
30     31  approachable  0.03125  2.302585  0.071956
31     32  distinctive.  0.03125  2.995732  0.093617
Documento 15
    Index           Term        TF       IDF    TF-IDF
0       1          zesty  0.052632  2.995732  0.157670
1       2         orange  0.052632  2.302585  0.121189
2       3          peels  0.052632  2.995732  0.157670
3       4          apple  0.052632  2.302585  0.121189
4       5           note  0.052632  1.386294  0.072963
5       6         abound  0.052632  2.995732  0.157670
6       7     sprightly,  0.052632  2.995732  0.157670
7       8  mineral-toned  0.052632  2.995732  0.157670
8       9      riesling.  0.052632  2.995732  0.157670
9      10            dry  0.052632  1.609438  0.084707
10     11        palate,  0.052632  2.302585  0.121189
11     12           racy  0.052632  2.995732  0.157670
12     13          lean,  0.052632  2.995732  0.157670
13     14              a  0.052632  0.287682  0.015141
14     15    refreshing,  0.052632  2.995732  0.157670
15     16           easy  0.052632  2.995732  0.157670
16     17        quaffer  0.052632  2.995732  0.157670
17     18           wide  0.052632  2.995732  0.157670
18     19        appeal.  0.052632  2.995732  0.157670
Documento 16
    Index         Term        TF       IDF    TF-IDF
0       1         bake  0.030303  2.995732  0.090780
1       2        plum,  0.030303  2.995732  0.090780
2       3    molasses,  0.030303  2.995732  0.090780
3       4     balsamic  0.030303  2.995732  0.090780
4       5      vinegar  0.030303  2.995732  0.090780
5       6       cheesy  0.030303  2.995732  0.090780
6       7          oak  0.030303  1.609438  0.048771
7       8       aromas  0.030303  0.798508  0.024197
8       9         feed  0.030303  2.995732  0.090780
9      10            a  0.090909  0.287682  0.026153
10     11       palate  0.030303  1.386294  0.042009
11     12       braced  0.030303  2.995732  0.090780
12     13         bolt  0.030303  2.995732  0.090780
13     14     acidity.  0.030303  1.609438  0.048771
14     15      compact  0.030303  2.995732  0.090780
15     16          set  0.030303  2.995732  0.090780
16     17        saucy  0.030303  2.995732  0.090780
17     18    red-berry  0.030303  2.995732  0.090780
18     19         plum  0.030303  1.609438  0.048771
19     20      flavors  0.030303  1.203973  0.036484
20     21      feature  0.030303  2.995732  0.090780
21     22      tobacco  0.030303  2.995732  0.090780
22     23      peppery  0.030303  2.995732  0.090780
23     24     accents,  0.030303  2.995732  0.090780
24     25       finish  0.030303  1.897120  0.057488
25     26       mildly  0.030303  2.995732  0.090780
26     27        green  0.030303  1.609438  0.048771
27     28      flavor,  0.030303  2.995732  0.090780
28     29  respectable  0.030303  2.995732  0.090780
29     30       weight  0.030303  2.995732  0.090780
30     31     balance.  0.030303  2.995732  0.090780
Documento 17
    Index          Term        TF       IDF    TF-IDF
0       1           raw  0.038462  2.995732  0.115220
1       2  black-cherry  0.038462  2.995732  0.115220
2       3        aromas  0.038462  0.798508  0.030712
3       4        direct  0.038462  2.995732  0.115220
4       5        simple  0.038462  2.995732  0.115220
5       6         good.  0.038462  2.995732  0.115220
6       7             a  0.076923  0.287682  0.022129
7       8         juicy  0.038462  1.897120  0.072966
8       9          feel  0.038462  2.995732  0.115220
9      10      thickens  0.038462  2.995732  0.115220
10     11         time,  0.038462  2.995732  0.115220
11     12           oak  0.076923  1.609438  0.123803
12     13     character  0.038462  2.302585  0.088561
13     14       extract  0.038462  2.995732  0.115220
14     15     apparent.  0.038462  2.995732  0.115220
15     16        flavor  0.038462  2.302585  0.088561
16     17       profile  0.038462  2.995732  0.115220
17     18         drive  0.038462  2.995732  0.115220
18     19    dark-berry  0.038462  2.995732  0.115220
19     20        fruits  0.038462  1.897120  0.072966
20     21    smoldering  0.038462  2.995732  0.115220
21     22        finish  0.038462  1.897120  0.072966
22     23         meaty  0.038462  2.995732  0.115220
23     24          hot.  0.038462  2.995732  0.115220
Documento 18
    Index          Term        TF       IDF    TF-IDF
0       1    desiccated  0.034483  2.995732  0.103301
1       2   blackberry,  0.034483  2.995732  0.103301
2       3      leather,  0.034483  2.995732  0.103301
3       4       charred  0.034483  2.995732  0.103301
4       5          wood  0.034483  2.995732  0.103301
5       6          mint  0.034483  2.995732  0.103301
6       7        aromas  0.068966  0.798508  0.055069
7       8         carry  0.034483  1.897120  0.065418
8       9          nose  0.034483  2.995732  0.103301
9      10  full-bodied,  0.034483  2.995732  0.103301
10     11       tannic,  0.034483  2.302585  0.079399
11     12       heavily  0.034483  2.995732  0.103301
12     13         oaked  0.034483  2.995732  0.103301
13     14         tinto  0.034483  2.995732  0.103301
14     15         fino.  0.034483  2.995732  0.103301
15     16       flavors  0.034483  1.203973  0.041516
16     17         clove  0.034483  2.995732  0.103301
17     18     woodspice  0.034483  2.995732  0.103301
18     19           sit  0.034483  2.995732  0.103301
19     20           top  0.034483  2.995732  0.103301
20     21    blackberry  0.034483  2.302585  0.079399
21     22        fruit,  0.034483  1.897120  0.065418
22     23       hickory  0.034483  2.995732  0.103301
23     24      forceful  0.034483  2.995732  0.103301
24     25     oak-based  0.034483  2.995732  0.103301
25     26          rise  0.034483  2.995732  0.103301
26     27      dominate  0.034483  2.302585  0.079399
27     28       finish.  0.034483  1.897120  0.065418
Documento 19
    Index          Term       TF       IDF    TF-IDF
0       1           red  0.03125  1.609438  0.050295
1       2         fruit  0.03125  2.995732  0.093617
2       3        aromas  0.03125  0.798508  0.024953
3       4       pervade  0.03125  2.995732  0.093617
4       5         nose,  0.03125  2.995732  0.093617
5       6         cigar  0.03125  2.302585  0.071956
6       7           box  0.03125  2.995732  0.093617
7       8       menthol  0.03125  2.995732  0.093617
8       9          note  0.06250  1.386294  0.086643
9      10          ride  0.03125  2.995732  0.093617
10     11         back.  0.03125  2.995732  0.093617
11     12        palate  0.03125  1.386294  0.043322
12     13      slightly  0.03125  1.897120  0.059285
13     14      restrain  0.03125  2.302585  0.071956
14     15        entry,  0.03125  2.995732  0.093617
15     16          open  0.03125  2.302585  0.071956
16     17         riper  0.03125  2.995732  0.093617
17     18        cherry  0.03125  2.995732  0.093617
18     19          plum  0.03125  1.609438  0.050295
19     20       specked  0.03125  2.995732  0.093617
20     21       crushed  0.03125  2.995732  0.093617
21     22       pepper.  0.03125  2.302585  0.071956
22     23         blend  0.03125  2.995732  0.093617
23     24       merlot,  0.03125  2.995732  0.093617
24     25      cabernet  0.06250  2.995732  0.187233
25     26     sauvignon  0.03125  2.995732  0.093617
26     27         franc  0.03125  2.995732  0.093617
27     28  approachable  0.03125  2.302585  0.071956
28     29         ready  0.03125  2.995732  0.093617
29     30      enjoyed.  0.03125  2.995732  0.093617
Documento 20
    Index        Term        TF       IDF    TF-IDF
0       1        ripe  0.038462  1.897120  0.072966
1       2      aromas  0.038462  0.798508  0.030712
2       3        dark  0.038462  2.302585  0.088561
3       4     berries  0.038462  2.995732  0.115220
4       5      mingle  0.038462  2.995732  0.115220
5       6       ample  0.038462  2.995732  0.115220
6       7        note  0.076923  1.386294  0.106638
7       8       black  0.038462  2.302585  0.088561
8       9     pepper,  0.038462  2.995732  0.115220
9      10     toasted  0.038462  2.995732  0.115220
10     11     vanilla  0.038462  2.302585  0.088561
11     12       dusty  0.038462  2.995732  0.115220
12     13    tobacco.  0.038462  2.995732  0.115220
13     14      palate  0.038462  1.386294  0.053319
14     15  oak-driven  0.038462  2.302585  0.088561
15     16     nature,  0.038462  2.995732  0.115220
16     17        tart  0.038462  1.897120  0.072966
17     18         red  0.038462  1.609438  0.061901
18     19     currant  0.038462  2.995732  0.115220
19     20       shine  0.038462  2.995732  0.115220
20     21    through,  0.038462  2.302585  0.088561
21     22       offer  0.038462  1.609438  0.061901
22     23           a  0.038462  0.287682  0.011065
23     24        bite  0.038462  2.302585  0.088561
24     25     levity.  0.038462  2.995732  0.115220

Matriz de Similitud Coseno:
             Document 1  Document 2  ...  Document 19  Document 20
Document 1     1.000000    0.022620  ...     0.014243     0.036087
Document 2     0.022620    1.000000  ...     0.016729     0.051006
Document 3     0.000000    0.018088  ...     0.000000     0.067228
Document 4     0.014353    0.001435  ...     0.051725     0.078128
Document 5     0.000000    0.002008  ...     0.000000     0.001612
Document 6     0.044568    0.020251  ...     0.015585     0.036612
Document 7     0.005112    0.024872  ...     0.050580     0.024720
Document 8     0.029460    0.073960  ...     0.044596     0.028311
Document 9     0.080476    0.000000  ...     0.021573     0.027165
Document 10    0.000000    0.037367  ...     0.000000     0.000674
Document 11    0.044786    0.021273  ...     0.033122     0.001953
Document 12    0.021487    0.088590  ...     0.054606     0.061606
Document 13    0.045663    0.048041  ...     0.018353     0.081076
Document 14    0.000000    0.024341  ...     0.022338     0.038627
Document 15    0.000000    0.000711  ...     0.021054     0.027082
Document 16    0.030384    0.019436  ...     0.022471     0.015427
Document 17    0.004165    0.055825  ...     0.003081     0.004886
Document 18    0.029164    0.000000  ...     0.005643     0.007106
Document 19    0.014243    0.016729  ...     1.000000     0.066527
Document 20    0.036087    0.051006  ...     0.066527     1.000000

[20 rows x 20 columns]