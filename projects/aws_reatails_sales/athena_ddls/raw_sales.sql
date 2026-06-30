CREATE EXTERNAL TABLE IF NOT EXISTS retail_dev.raw_sales (
    sale_id         STRING,
    sale_date       STRING,
    customer_id     STRING,
    product_id      STRING,
    product_name    STRING,
    category        STRING,
    quantity        STRING,
    unit_price      STRING,
    discount_pct    STRING,
    total_amount    STRING,
    city            STRING,
    state           STRING,
    store_id        STRING,
    payment_mode    STRING
)
PARTITIONED BY (
    year STRING,
    month STRING,
    day STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar" = "\"",
    "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION 's3://retail-data-lake-dev/raw/'
TBLPROPERTIES (
    'skip.header.line.count'='1'
);