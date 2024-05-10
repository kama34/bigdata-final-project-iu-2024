"""This module is used to train ML models ALS, Random Forest"""
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.recommendation import ALS
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml import Transformer
from pyspark.sql import DataFrame
import math
import os
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
# Connect to Hive

# Add here your team number teamx
TEAM = "team8"

# location of your Hive database in HDFS
WAREHOUSE = "project/hive/warehouse"

spark = SparkSession.builder\
        .appName(f"{TEAM} - spark ML")\
        .master("yarn")\
        .config("hive.metastore.uris", \
                "thrift://hadoop-02.uni.innopolis.ru:9883")\
        .config("spark.sql.warehouse.dir", WAREHOUSE)\
        .config("spark.sql.avro.compression.codec", "snappy")\
        .enableHiveSupport()\
        .getOrCreate()

sc = spark.sparkContext

# list Hive databases

spark.catalog.listDatabases()

spark.catalog.listTables("team8_projectdb")

# Read the Hive table

ratings = spark.read.format("avro").table('team8_projectdb.ratings')
movies = spark.read.format("avro").table('team8_projectdb.movies')
links = spark.read.format("avro").table('team8_projectdb.links')
tags = spark.read.format("avro").table('team8_projectdb.tags')
ganres = spark.read.format("avro").table('team8_projectdb.ganres_partitioned')

ratings.show()

# Transformation of categorical variables

indexer = StringIndexer(inputCol="tag", outputCol="tagIndex")
tags = indexer.fit(tags).transform(tags)

ratings = ratings.withColumnRenamed("timestamp", "ratings_timestamp")
tags = tags.withColumnRenamed("timestamp", "tags_timestamp")

# Data connection

data = ratings.join(tags, ["userId", "movieId"]).join(movies, "movieId")

data.show()

# Creating additional features

# Average user rating
user_avg = ratings.groupBy("userId").agg(F.avg("rating").alias("user_avg"))
data = data.join(user_avg, "userId")

# Average rating of the film
movie_avg = ratings.groupBy("movieId").agg(F.avg("rating").alias("movie_avg"))
data = data.join(movie_avg, "movieId")

# Number of user ratings
user_count = ratings.groupBy("userId").count().withColumnRenamed("count",
                                                                 "user_count")

data = data.join(user_count, "userId")

# Number of movie ratings
movie_count = ratings.groupBy("movieId").count().withColumnRenamed(
    "count", "movie_count")
data = data.join(movie_count, "movieId")

# Converting timestamp to separate columns
data = data.withColumn("year", F.year(F.from_unixtime(
    F.col("ratings_timestamp") / 1000)))
data = data.withColumn("month", F.month(F.from_unixtime(
    F.col("ratings_timestamp") / 1000)))
data = data.withColumn("day", F.dayofmonth(F.from_unixtime(
    F.col("ratings_timestamp") / 1000)))
data = data.withColumn("hour", F.hour(F.from_unixtime(
    F.col("ratings_timestamp") / 1000)))
data = data.withColumn("minute", F.minute(F.from_unixtime(
    F.col("ratings_timestamp") / 1000)))
data = data.withColumn("second", F.second(F.from_unixtime(
    F.col("ratings_timestamp") / 1000)))

data.show()

# drop
# recordid
# ratings_timestamp
# tag
# tags_timestamp
# title
# date_ratings
data = data.drop("recordid")
data = data.drop("ratings_timestamp")
data = data.drop("tag")
data = data.drop("tags_timestamp")
data = data.drop("title")
data = data.drop("date_ratings")

data.show()



class CyclicalEncoder(Transformer):
    def __init__(self, input_col: str, outputColSin: str, outputColCos: str, max_val: float):
        self.input_col = input_col
        self.outputColSin = outputColSin
        self.outputColCos = outputColCos
        self.max_val = max_val

    def _transform(self, df: DataFrame) -> DataFrame:
        df = df.withColumn(self.outputColSin,
                           F.sin(2 * math.pi * F.col(self.input_col)
                                 / self.max_val))
        df = df.withColumn(self.outputColCos,
                           F.cos(2 * math.pi * F.col(self.input_col)
                                 / self.max_val))
        return df

    def transform(self, df: DataFrame) -> DataFrame:
        self._transform(df)


# Applying the transformation
data = CyclicalEncoder("month", "month_sin", "month_cos", 12).transform(data)
data = CyclicalEncoder("day", "day_sin", "day_cos", 31).transform(data)
data = CyclicalEncoder("hour", "hour_sin", "hour_cos", 24).transform(data)
data = CyclicalEncoder("minute", "minute_sin", "minute_cos", 60).transform(data)
data = CyclicalEncoder("second", "second_sin", "second_cos", 60).transform(data)

# drop
# month
# day
# hour
# minute
# second
data = data.drop("month")
data = data.drop("day")
data = data.drop("hour")
data = data.drop("minute")
data = data.drop("second")

data.show()

# Creating an RF model in Spark ML


# Creating a feature vector
assembler = VectorAssembler(
 inputCols=["tagIndex", "user_avg", "movie_avg", "user_count", "movie_count",
            "year", "month_sin", "month_cos", "day_sin", "day_cos",
            "hour_sin", "hour_cos", "minute_sin", "minute_cos", "second_sin",
            "second_cos"],
 outputCol="features"
)
data = assembler.transform(data)

# Dividing the data into training and test samples
(train, test) = data.randomSplit([0.8, 0.2])

# Creating an instance of RandomForestRegressor
rf = RandomForestRegressor(featuresCol="features", labelCol="rating",
                           maxBins=2000)


def run(command):
    return os.popen(command).read()


train.select("features", "rating")\
    .coalesce(1)\
    .write\
    .mode("overwrite")\
    .format("json")\
    .save("project/data/train")

# Run it from root directory of the repository
run("hdfs dfs -cat project/data/train/*.json > data/train.json")

test.select("features", "rating")\
    .coalesce(1)\
    .write\
    .mode("overwrite")\
    .format("json")\
    .save("project/data/test")

# Run it from root directory of the repository
run("hdfs dfs -cat project/data/test/*.json > data/test.json")

selected_columns = ["tagIndex", "user_avg", "movie_avg", "user_count",
                    "movie_count", "year", "month_sin", "month_cos",
                    "day_sin", "day_cos", "hour_sin", "hour_cos",
                    "minute_sin", "minute_cos", "second_sin",
                    "second_cos"]
selected_columns.append("rating")
train.select(*selected_columns)\
    .coalesce(1)\
    .write\
    .mode("overwrite")\
    .format("csv")\
    .option("sep", ",")\
    .option("header", "true")\
    .save("project/data/train")

# Run it from root directory of the repository
run("hdfs dfs -cat project/data/train/*.csv > data/train.csv")

test.select(*selected_columns)\
    .coalesce(1)\
    .write\
    .mode("overwrite")\
    .format("csv")\
    .option("sep", ",")\
    .option("header", "true")\
    .save("project/data/train")

# Run it from root directory of the repository
run("hdfs dfs -cat project/data/test/*.csv > data/test.csv")


# Обучение модели RandomForestRegressor
model = rf.fit(train)

# Predicting ratings for all users and movies
predictions = model.transform(test)

predictions = predictions.withColumn("id", F.monotonically_increasing_id())
predictions.select("id", "rating", "prediction")\
    .coalesce(1)\
    .write\
    .mode("overwrite")\
    .format("csv")\
    .option("sep", ",")\
    .option("header", "true")\
    .save("project/output/model1_predictions.csv")

# Run it from root directory of the repository
run("hdfs dfs -cat project/output/model1_predictions.csv/*.csv > output/model1_predictions.csv")

# Evaluating the performance of the model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)

print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")

# Evaluating the performance of the model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction",
                                metricName="r2")
r2 = evaluator.evaluate(predictions)

print(f"R2 on test data = {r2}")


# Creating an ALS model in Spark ML

# Creating an instance of ALS
als = ALS(
  userCol="userid",
  itemCol="movieid",
  ratingCol="rating",
  coldStartStrategy="drop"
)

# ALS Model Training
model = als.fit(train)

# Predicting ratings for all users and movies
predictions = model.transform(test)

predictions = predictions.withColumn("id", F.monotonically_increasing_id())
predictions.select("id", "rating", "prediction")\
    .coalesce(1)\
    .write\
    .mode("overwrite")\
    .format("csv")\
    .option("sep", ",")\
    .option("header", "true")\
    .save("project/output/model2_predictions.csv")

# Run it from root directory of the repository
run("hdfs dfs -cat project/output/model2_predictions.csv/*.csv > output/model2_predictions.csv")

# Evaluating the performance of the model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction",
                                metricName="rmse")
rmse = evaluator.evaluate(predictions)

print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")

# Evaluating the performance of the model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction",
                                metricName="r2")
r2 = evaluator.evaluate(predictions)

print(f"R2 on test data = {r2}")


# Configuring hyperparameters and Grid search for RF


# Creating a grid of parameters
paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [10, 50, 100]) \
    .addGrid(rf.maxDepth, [5, 10, 20]) \
    .build()

# Creating a cross-validator
crossval = CrossValidator(estimator=rf,
                          estimatorParamMaps=paramGrid,
                          evaluator=evaluator,
                          numFolds=3)  # используйте 3-кратную кросс-валидацию

# Training the RandomForestRegressor model on a training sample using cross-validation
cvModel = crossval.fit(train)
# bestModel1 = cvModel.bestModel

# Predicting ratings for a test sample using the best model
predictions = cvModel.transform(test)

# Evaluating the performance of the best model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction",
                                metricName="rmse")
rmse = evaluator.evaluate(predictions)

# Evaluating the performance of the model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction",
                                metricName="r2")
r2 = evaluator.evaluate(predictions)

print(f"Root Mean Squared Error (RMSE) on test data = {rmse}" )
print(f"R2 on test data = {r2}")

# Configuring hyperparameters and Grid search for ALS

# Creating a grid of parameters
paramGrid = ParamGridBuilder() \
    .addGrid(als.rank, [10, 50, 100]) \
    .addGrid(als.regParam, [0.01, 0.1, 1.0]) \
    .build()

# Creating a cross-validator
crossval = CrossValidator(estimator=als,
                          estimatorParamMaps=paramGrid,
                          evaluator=evaluator,
                          numFolds=3)  # use 3x cross validation

# Training the ALS model on a training sample using cross-validation
cvModel = crossval.fit(train)

# Predicting ratings for a test sample using the best model
predictions = cvModel.transform(test)

# Evaluating the performance of the best model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction",
                                metricName="rmse")
rmse = evaluator.evaluate(predictions)

# Evaluating the performance of the model
evaluator = RegressionEvaluator(labelCol="rating", predictionCol="prediction",
                                metricName="r2")
r2 = evaluator.evaluate(predictions)

print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")
print(f"R2 on test data = {r2}")
