#!/bin/bash

password=$(head -n 1 /home/team8/project/secrets/.psql.pass)

# sqoop list-databases --connect jdbc:postgresql://hadoop-04.uni.innopolis.ru/team8_projectdb --username team8 --password $password

sqoop list-tables --connect jdbc:postgresql://hadoop-04.uni.innopolis.ru/team8_projectdb --username team8 --password $password

sqoop import-all-tables --connect jdbc:postgresql://hadoop-04.uni.innopolis.ru/team8_projectdb --username team8 --password $password --compression-codec=snappy --compress --as-avrodatafile --warehouse-dir=/home/team8/project/warehouse --m 1

# sqoop import --connect jdbc:postgresql://hadoop-04.uni.innopolis.ru/team8_projectdb --username team8 --password $password --compression-codec=snappy --compress --as-avrodatafile --warehouse-dir=/user/team8/project/warehouse --m 1 --table emps --columns empno, sal