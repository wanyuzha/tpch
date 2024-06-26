from pyspark.sql import SparkSession

if __name__ == '__main__':

    spark = SparkSession.builder.appName("Q9-SF100-P40").config("spark.sql.files.maxPartitionBytes", 26214400) \
    .config("spark.default.parallelism", "300")     \
    .config("spark.sql.shuffle.partitions", "300").getOrCreate()
    spark.conf.set("spark.sql.shuffle.partitions", "300")  

    lineitem = spark.read.parquet("hdfs://rcnfs:8020/tpch/sf100/lineitem/")
    lineitem.createOrReplaceTempView("lineitem")

    nation = spark.read.parquet("hdfs://rcnfs:8020/tpch/sf100/nation/")
    nation.createOrReplaceTempView("nation")

    orders = spark.read.parquet("hdfs://rcnfs:8020/tpch/sf100/orders/")
    orders.createOrReplaceTempView("orders")

    part = spark.read.parquet("hdfs://rcnfs:8020/tpch/sf100/part/")
    part.createOrReplaceTempView("part")

    partsupp = spark.read.parquet("hdfs://rcnfs:8020/tpch/sf100/partsupp/")
    partsupp.createOrReplaceTempView("partsupp")

    supplier = spark.read.parquet("hdfs://rcnfs:8020/tpch/sf100/supplier/")
    supplier.createOrReplaceTempView("supplier")

    for i in range(10):
        result = spark.sql("""SELECT
        nation,
        o_year,
        SUM(amount) AS sum_profit
    FROM
        (
            SELECT
                n_name AS nation,
                YEAR(o_orderdate) AS o_year,
                l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity AS amount
            FROM
                part,
                supplier,
                lineitem,
                partsupp,
                orders,
                nation
            WHERE
                s_suppkey = l_suppkey
                AND ps_suppkey = l_suppkey
                AND ps_partkey = l_partkey
                AND p_partkey = l_partkey
                AND o_orderkey = l_orderkey
                AND s_nationkey = n_nationkey
                AND p_name LIKE '%green%'
        ) AS profit
    GROUP BY
        nation,
        o_year
    ORDER BY
        nation,
        o_year DESC;
    """)

        result.show()
