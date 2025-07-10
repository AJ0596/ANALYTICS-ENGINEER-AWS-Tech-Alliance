import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import col, to_timestamp

# Initialize the Glue job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# S3 input and RDS connection details
s3_bucket = "s3://OLIST/SALES_FILES/"
jdbc_url = "jdbc:mysql://your-rds-endpoint:3306/PROJECT_2"
db_user = "DB_USER"
db_password = "MY_PASS"

# Utility function to write DataFrame to RDS
def write_to_rds(df, table_name):
    df.write.format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", db_user) \
        .option("password", db_password) \
        .mode("append") \
        .save()

# Customers Dimension
customers_df = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [s3_bucket + "olist_customers_dataset.csv"]},
    transformation_ctx="customers_df"
).toDF().select(
    col("customer_id").cast("string"),
    col("customer_unique_id").cast("string"),
    col("customer_city").cast("string"),
    col("customer_state").cast("string")
).dropDuplicates(["customer_id"])

# Products Dimension
products_df = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [s3_bucket + "olist_products_dataset.csv"]},
    transformation_ctx="products_df"
).toDF().select(
    col("product_id").cast("string"),
    col("product_category_name").cast("string").alias("product_cat_name"),
    col("product_weight_g").cast("int").alias("product_weight"),
    col("product_length_cm").cast("int").alias("product_length"),
    col("product_height_cm").cast("int").alias("product_height"),
    col("product_width_cm").cast("int").alias("product_width")
).dropDuplicates(["product_id"])

# Sellers Dimension
sellers_df = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [s3_bucket + "olist_sellers_dataset.csv"]},
    transformation_ctx="sellers_df"
).toDF().select(
    col("seller_id").cast("string"),
    col("seller_city").cast("string"),
    col("seller_zip_code_prefix").cast("int").alias("seller_zip_code"),
    col("seller_state").cast("string")
).dropDuplicates(["seller_id"])

# Orders Dimension
orders_df = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [s3_bucket + "olist_orders_dataset.csv"]},
    transformation_ctx="orders_df"
).toDF().select(
    col("order_id").cast("string").alias("order_cust_id"),
    col("customer_id").cast("string"),
    col("order_status").cast("string"),
    to_timestamp(col("order_purchase_timestamp")).alias("purchase_date_time"),
    to_timestamp(col("order_approved_at")).alias("approved_date_time"),
    to_timestamp(col("order_delivered_carrier_date")).alias("delivery_start"),
    to_timestamp(col("order_delivered_customer_date")).alias("delivery_end"),
    to_timestamp(col("order_estimated_delivery_date")).alias("estimated_delivery")
).dropDuplicates(["order_cust_id"])

# Order Items Dimension
order_items_df = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [s3_bucket + "olist_order_items_dataset.csv"]},
    transformation_ctx="order_items_df"
).toDF().select(
    col("order_id").cast("string"),
    col("order_item_id").cast("int"),
    col("product_id").cast("string"),
    col("seller_id").cast("string"),
    col("price").cast("decimal(10,2)").alias("order_price"),
    col("freight_value").cast("decimal(10,2)").alias("order_freight_value")
).dropDuplicates(["order_id", "order_item_id"])

# Create Fact Table: seller_analysis_fct
seller_analysis_fct_df = orders_df.join(order_items_df, orders_df.order_cust_id == order_items_df.order_id, "inner") \
    .select(
        orders_df.customer_id,
        order_items_df.product_id,
        order_items_df.seller_id,
        order_items_df.order_id,
        orders_df.order_cust_id
    ).dropDuplicates(["customer_id", "product_id", "seller_id", "order_id", "order_cust_id"])

# Write all tables to RDS
write_to_rds(customers_df, "customers")
write_to_rds(products_df, "products")
write_to_rds(sellers_df, "seller")
write_to_rds(orders_df, "orders")
write_to_rds(order_items_df, "order_items")
write_to_rds(seller_analysis_fct_df, "seller_analysis_fct")

# Commit the job
job.commit()
