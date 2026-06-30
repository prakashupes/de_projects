# Retail Sales Data Lake on AWS

## Overview

This project demonstrates how to build a production-style AWS Data Lake for a retail company. Instead of relying entirely on AWS Glue Studio and Crawlers, the project follows software engineering best practices by separating infrastructure, metadata, and ETL code.

The project simulates a retail company receiving daily sales files from stores across India. The pipeline ingests raw CSV files into Amazon S3, registers metadata in the AWS Glue Data Catalog using SQL DDL, transforms the data using AWS Glue (Apache Spark), stores optimized Parquet files, and enables analytics through Amazon Athena.

---

# Business Problem

A retail company receives daily sales data from hundreds of stores.

Business users need answers to questions such as:

* Daily revenue
* Revenue by city
* Revenue by category
* Top-selling products
* Store performance
* Payment mode analysis

The incoming data is delivered as CSV files and must be transformed into an analytics-ready format.

---

# Project Objectives

* Build a scalable AWS Data Lake
* Learn AWS Glue fundamentals
* Implement production-style Glue development
* Use Git for version control
* Define metadata using SQL instead of Crawlers
* Execute Glue jobs using Python scripts stored in Amazon S3
* Query processed data using Athena

---

# Architecture

```text
                   Daily Sales Files
                           │
                           ▼
                  Amazon S3 (Raw Zone)
                           │
                           ▼
              SQL DDL → Athena Execution
                           │
                           ▼
                 AWS Glue Data Catalog
                           │
                           ▼
              AWS Glue ETL Job (Spark)
             • Read Raw Data
             • Clean Records
             • Calculate total_amount
             • Convert CSV → Parquet
                           │
                           ▼
               Amazon S3 (Bronze Layer)
                           │
                           ▼
                  AWS Glue Catalog
                           │
                           ▼
                      Amazon Athena
                           │
                           ▼
                    Business Analytics
```

---

# Technology Stack

* Amazon S3
* AWS Glue
* AWS Glue Catalog
* AWS Glue Jobs
* Amazon Athena
* AWS IAM
* AWS CLI
* Boto3
* Apache Spark
* Python
* SQL
* Git
* GitHub
* VS Code

---

# Project Structure

```text
# Project Structure

```text
aws_retail_sales/
│
├── athena_ddls/
│   ├── create_database.sql
│   ├── raw_sales.sql
│   ├── bronze_sales.sql
│   └── processed_sales.sql
│
├── data_generator/
│   ├── generate_sales.py
│   └── sample_data/
│
├── etl_utils/
│   ├── config.py
│   ├── constants.py
│   ├── logger.py
│   ├── validations.py
│   └── helpers.py
│
├── glue/
│   ├── raw_to_bronze.py
│   ├── bronze_to_processed.py
│   └── common.py
│
├── infra/
│   ├── create_bucket.py
│   ├── create_database.py
│   ├── create_glue_job.py
│   ├── upload_scripts.py
│   ├── deploy_tables.py
│   └── setup_project.py
│
├── prompts/
│   ├── project_notes.md
│   └── learning_notes.md
│
└── README.md
│
└── architecture.png
```

---

# Dataset

Each day, one sales file arrives.

Example:

```text
sales_2026_06_01.csv
sales_2026_06_02.csv
sales_2026_06_03.csv
```

Sample columns:

| Column       | Description         |
| ------------ | ------------------- |
| sale_id      | Sale Identifier     |
| sale_date    | Transaction Date    |
| customer_id  | Customer Identifier |
| product_id   | Product Identifier  |
| city         | Store City          |
| state        | State               |
| category     | Product Category    |
| quantity     | Quantity Sold       |
| unit_price   | Price per Unit      |
| payment_mode | Cash / Card / UPI   |
| store_id     | Store Identifier    |

---

# Data Lake Layout

```text
retail-data-lake/

├── raw/
│
├── bronze/
│
├── scripts/
│
├── ddl/
│
└── athena-results/
```

---

# Data Flow

1. Daily sales files are uploaded to Amazon S3.
2. SQL DDL creates Glue Catalog tables.
3. AWS Glue Job reads raw data.
4. Spark performs cleansing and transformations.
5. Data is written as Parquet into the Bronze layer.
6. Athena queries the processed data.
7. Business users perform analytics.

---

# Transformations

* Remove invalid records
* Remove NULL quantity
* Remove NULL price
* Standardize city names
* Calculate total_amount

```
total_amount = quantity × unit_price
```

* Convert CSV to Parquet

---

# Metadata Management

Instead of relying on Glue Crawlers, metadata is managed through SQL DDL.

Example:

```sql
CREATE EXTERNAL TABLE ...
```

Benefits:

* Explicit schema control
* Version-controlled metadata
* Easier code reviews
* Environment-independent deployments
* No schema inference issues

---

# Development Workflow

```text
VS Code

↓

Python + SQL

↓

Git

↓

Pull Request

↓

CI/CD

↓

Upload Glue Script to Amazon S3

↓

AWS Glue Job

↓

Spark Execution

↓

Athena
```

---

# Environment Strategy

Separate environments are maintained for:

* Development
* QA
* Production

Configuration files are stored separately.

```text
config/

dev.yaml

qa.yaml

prod.yaml
```

---

# Business Queries

Examples include:

* Revenue by City
* Revenue by Category
* Daily Revenue
* Store Performance
* Top Selling Products
* Payment Mode Analysis

---

# AWS Services Covered

| Service          | Purpose              |
| ---------------- | -------------------- |
| Amazon S3        | Data Lake Storage    |
| AWS Glue         | Serverless Spark ETL |
| AWS Glue Catalog | Metadata Repository  |
| AWS Glue Jobs    | ETL Execution        |
| Amazon Athena    | SQL Analytics        |
| IAM              | Security             |
| AWS CLI          | Resource Management  |
| Boto3            | AWS Automation       |

---

# Learning Roadmap

### Phase 1

* Amazon S3
* IAM
* AWS CLI
* Boto3
* Glue Catalog
* Glue Jobs
* Athena

### Phase 2

* Glue Crawlers
* Glue Workflows
* Glue Triggers
* Job Bookmarks

### Phase 3

* Partitioning
* Incremental Processing
* Partition Projection

### Phase 4

* Lake Formation
* EventBridge
* Lambda
* CloudWatch

### Phase 5

* CI/CD
* Infrastructure as Code
* Production Deployment

---

# Future Enhancements

* Bronze → Silver → Gold architecture
* Incremental ETL
* Partition Projection
* Data Quality Validation
* CloudWatch Monitoring
* SNS Notifications
* Infrastructure as Code (Terraform / CloudFormation)
* Automated CI/CD Pipeline
* Unit Testing
* Data Catalog Versioning

---

# Key Learning Outcomes

By completing this project, you will understand:

* Building a Data Lake on AWS
* Production-style AWS Glue development
* Metadata management without Crawlers
* Glue Job architecture
* Apache Spark ETL
* Athena-based analytics
* Git-based development workflow
* Environment promotion (Dev → QA → Prod)
* Best practices used in enterprise Data Engineering teams
