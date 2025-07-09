import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import col, to_timestamp

# -----------------------------
# Initialize Glue Job
# -----------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -----------------------------
# Configurations
# -----------------------------
s3_bucket = "s3://OLIST/MARKETING_FILES/"
jdbc_url = "jdbc:mysql://MYSQL.amazonaws.com:3306/PROJECT_1"
db_user = "DB_USER"
db_password = "MY_PASS"

# -----------------------------
# Read olist_closed_deals from S3
# -----------------------------
closed_deals_dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": [s3_bucket + "olist_closed_deals_dataset.csv"]},
    format_options={"withHeader": True}
).toDF()

# Clean & Transform closed deals
closed_deals_df = closed_deals_dyf.na.drop() \
    .dropDuplicates(["mql_id"]) \
    .select(
        col("mql_id").cast("string"),
        col("seller_id").cast("string"),
        col("sdr_id").cast("string"),
        col("sr_id").cast("string"),
        to_timestamp(col("won_date"), "M/d/yyyy H:mm").alias("won_date"),
        col("business_segment").cast("string"),
        col("lead_type").cast("string"),
        col("lead_behaviour_profile").cast("string"),
        col("business_type").cast("string")
    )

# -----------------------------
# Read olist_qualified_leads from S3
# -----------------------------
qualified_leads_dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    format="csv",
    connection_options={"paths": [s3_bucket + "olist_marketing_qualified_leads_dataset.csv"]},
    format_options={"withHeader": True}
).toDF()

# Clean & Transform qualified leads
qualified_leads_df = qualified_leads_dyf.na.drop() \
    .dropDuplicates(["mql_id"]) \
    .select(
        col("mql_id").cast("string"),
        to_timestamp(col("first_contact_date"), "M/d/yyyy").alias("first_contact_date"),
        col("landing_page_id").cast("string"),
        col("origin").cast("string")
    )

# -----------------------------
# Function to write to MySQL (RDS)
# -----------------------------
def write_to_rds(df, table_name):
    df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", db_user) \
        .option("password", db_password) \
        .option("driver", "com.mysql.jdbc.Driver") \
        .mode("append") \
        .save()

# -----------------------------
# Load data into RDS
# -----------------------------
write_to_rds(qualified_leads_df, "olist_qualified_leads")
write_to_rds(closed_deals_df, "olist_closed_deals")

job.commit()
