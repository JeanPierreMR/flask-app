# GUATE-HOGAR
Guate-hogar es una aplicación que busca facilitar la venta/renta de viviendas dentro de Guatemala. 
Actualmente se encuentra delimitado a zonas céntricas de la ciudad capital. 

# Integrantes
- Jean Pierre Mejicanos
- Adriana Mundo
- Pablo Velasquez

## Contenido
-   [UML](#UML)
-   [Requisitos](#Requisitos)
-   [Ejecución](#Ejecución)
-   [Acceso](#Acceso)
-   [Profiler](#Profiler)
-   [Prueba de carga](#Pruebas de carga)
-   [Autores](#Autores)


### UML 
![Image text](https://github.com/JeanPierreMR/flask-app/blob/master/Pictures/UML/vender.jpeg)
![Image text](https://github.com/JeanPierreMR/flask-app/blob/master/Pictures/UML/comprar.jpeg)
![Image text](https://github.com/JeanPierreMR/flask-app/blob/master/Pictures/UML/compra_confirmada.jpeg)


### Requisitos

 -  pipenv, python3

 -  requierements.txt 
    pip install -r requirements.txt

 -  ElasticSearch
    docker network create elastic-network
    node 1: docker run --rm --name esn01 -p 9200:9200 -v esdata01:/usr/share/elasticsearch/data --network elastic-network -e "node.name=esn01" -e "cluster.name=stanislavs-docker-cluster" -e "cluster.initial_master_nodes=esn01" -e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1 -e ES_JAVA_OPTS="-Xms2g -Xmx2g" docker.elastic.co/elasticsearch/elasticsearch:7.3.0

    node 2: docker run --rm --name esn01 -p 9200:9200 -v esdata01:/usr/share/elasticsearch/data --network elastic-network -e "node.name=esn01" -e "cluster.name=stanislavs-docker-cluster" -e "cluster.initial_master_nodes=esn01" -e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1 -e ES_JAVA_OPTS="-Xms2g -Xmx2g" docker.elastic.co/elasticsearch/elasticsearch:7.3.0

-   MySql
    docker-compose -f app/mysql-docker-compose.yml up -d

-   Kibana
    docker run --rm --link esn01:elasticsearch --name kibana --network elastic-network -p 5601:5601 docker.elastic.co/kibana/kibana:7.3.0

-   Kafka
    docker-compose -f app/kafka-docker-compose.yml up -d

-  Logstash 
   docker-compose -f app/mysql-docker-compose.yml up -d

-  JBDC
   logstash-plugin install jbdc

-  Snakeviz (visual profiler)
   pip install snakeviz


### Ejecución
-   venv
    venv\Scripts\activate

-   Python
    python3 run.py

-   Logstash 
    .../logstash-7.15.2/bin/logstash

-   Visual profiler
    snakeviz <profile_file_name>


### Acceso

se puede acceder a la app a través de las siguientes 2 opciones: 
-   http://localhost:5000/
-   http://127.0.0.1:5000/


### Profiler
Se utilizó Werkzeug profiler que muestra resultados en terminal. 

![Image text](https://github.com/JeanPierreMR/flask-app/blob/master/Pictures/Profiler/terminal.JPG)

Para poder visualizarlo utilizamos snakeviz que muestra gráficas y tablas. 
![Image text](https://github.com/JeanPierreMR/flask-app/blob/master/Pictures/Profiler/terminal.JPG)



### Pruebas de carga
Con JMeter realizamos el testing de pruebas de carga.
Aquí se muestran algunas imágenes, sin embargo más de estas se pueden encontrar en el folder 'JMeter'. 
-   Con Cache
![Image text](https://github.com/JeanPierreMR/flask-app/blob/master/JMeter/Cache/muchos_usuarios_con_cache.jpeg)

-   Sin Cache
![Image text](https://github.com/JeanPierreMR/flask-app/blob/master/JMeter/Sin%20cache/muchos_usuarios_sin_cache.jpeg)


### Autores
-   Jean Pierre Mejicanos
-   Adriana Mundo
-   Pablo Velasquez 
