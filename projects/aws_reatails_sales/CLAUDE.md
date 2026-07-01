# CLAUDE.md — aws_reatails_sales

This file captures my (Claude's) working understanding of the project. It is
meant to be a living document that we grow as the project evolves from low to
high complexity. Keep it accurate to the **actual code**, not just the README's
aspirations.

> Note: the folder name `aws_reatails_sales` is a typo for "retail_sales". The
> data lake bucket and DDLs use the correct spelling `retail-data-lake-dev` /
> `retail_dev`.

---

## 1. Project Goal

Build a **production-style AWS Data Lake for retail sales analytics** — the
deliberate contrast being: do it with hand-written Python + SQL under version
control, **not** with Glue Studio / Crawlers clicking. The learning objective is
as much about software-engineering discipline (config-driven, environment-aware,
metadata-as-code) as it is about the AWS services themselves.

Business scenario: a retailer receives **one daily sales CSV per day** from
stores across India. The pipeline must land it in S3, catalog it with SQL DDL,
transform it with Spark (Glue), write optimized Parquet, and expose it to Athena
for business questions (daily revenue, revenue by city/category, top products,
store performance, payment-mode analysis).

**Target topology: a Kappa lakehouse** (stream-first), with **medallion layers
(Bronze → Silver → Gold) maintained *inside* it**. See §2A for the architecture
decision and the phased path there. The current code is still batch (raw layer)
— we bridge to Kappa incrementally, Iceberg first.

---

## 2A. Architecture Decision — Kappa Lakehouse (not "instead of" medallion)

Key clarification the design rests on: **medallion and Kappa answer different
questions and are not alternatives.**

- **Medallion (Bronze/Silver/Gold)** = a *data-refinement layering* convention
  ("how raw/clean/curated is this data?").
- **Kappa / Lambda** = a *processing topology* ("batch, stream, or both?").

So we do **medallion layers within a Kappa pipeline**: Bronze = raw events off
Kafka landed as-is; Silver = cleaned/deduped/typed (`MERGE` upserts); Gold =
aggregated marts. The layering survives; each layer is maintained by a
*streaming* job reading an immutable log, not a nightly batch.

**Why Kappa over Lambda:** Lambda forces two implementations of every transform
(batch + speed layer) that must stay identical — a maintenance tax. Kappa
collapses to one streaming path; "reprocess history" is done by **replaying
Kafka / rebuilding the Iceberg table**, not a separate batch layer. Iceberg is
what makes Kappa practical on a lake. (Pragmatic note: pure Kappa is rare;
occasional batch backfills are fine — we are Kappa-*leaning*, not dogmatic.)

### Component roles (target stack)

| Component | Role in the Kappa lakehouse |
|---|---|
| **Kafka (MSK)** | Immutable, replayable event log — the heart of Kappa; single source of truth. |
| **Iceberg** | Lakehouse table format: ACID `MERGE` upserts, schema evolution, time travel, replay/reprocessing. Enables Kappa on the lake. |
| **Glue / Spark Structured Streaming** | Single streaming compute path — one codebase, no batch/stream duplication. (Flink is the alt.) |
| **Lambda + SQS/SNS** | Event glue: S3/Kafka triggers, DLQs, fan-out, alerting, DQ gates. Not a processing layer. |
| **Redshift** | Serving/BI layer — Spectrum over Gold Iceberg, or COPY Gold marts in. |
| **Athena** | Ad-hoc query over the same Iceberg tables. |

### Target architecture

```
 Store events ──▶ Kafka topic (sales.raw)      ◀── immutable log, replayable
                        │
                        ▼
        Spark Structured Streaming (Glue Streaming job)
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                 ▼
   Iceberg BRONZE   Iceberg SILVER   Iceberg GOLD
   (raw append)     (clean/dedup/     (aggregates:
                     MERGE upsert)     revenue by city/cat)
                        │                 │
                        ▼                 ▼
                   Athena (adhoc)    Redshift (BI/serving)

 Side channels:  S3 event ▶ Lambda ▶ SQS ▶ (DLQ) ▶ SNS ▶ alerts
```

### Production precedent

Netflix (created Iceberg for stream-first reprocessing), Apple, Adobe, Expedia,
Stripe — Kafka + Iceberg lakehouses with streaming upserts. Mirrors AWS's own
reference: MSK → Glue Streaming/Flink → Iceberg on S3 → Athena + Redshift
Spectrum.

### Honest caution (learning project)

Kappa is harder than batch medallion: exactly-once, watermarking/late data,
state management, Kafka ops, Iceberg maintenance (compaction, snapshot expiry).
That's the point (user already knows medallion), but it's why we **phase it, not
big-bang it** — see the migration path in §8.

---

## 2. Current State (as of 2026-07-01)

Recent git history: `Project Scope and Readme`, `raw layer completed`,
`utility scripts`, `fixed sample data`, `project dependencies`.

**Implemented:**
- Synthetic data generation ([data_generator/](data_generator/)) — pandas-based,
  reproducible (seed 42), 5 days × 1000 rows over `2026-06-01..05`.
- AWS client factory ([infra/common.py](infra/common.py)) — boto3 session +
  s3/glue/athena/iam clients, `bucket_exists`.
- Environment + table config loaders
  ([infra/config_loader.py](infra/config_loader.py)).
- S3 bucket / folder provisioning + upload helpers
  ([infra/util_functions.py](infra/util_functions.py)).
- Athena DDL executor ([infra/execute_ddl.py](infra/execute_ddl.py)).
- **Raw layer** DDL only ([athena_ddls/raw_sales.sql](athena_ddls/raw_sales.sql)) —
  external table over CSV with OpenCSVSerde, partitioned `year/month/day`.

**Not yet implemented (empty or missing):**
- [glue/](glue/) — empty. No `raw_to_bronze` / `bronze_to_silver` Spark jobs.
- [etl_utils/](etl_utils/) — empty. No shared logger/validations/helpers.
- `athena_ddls/` — only `raw_sales.sql`; no `create_database`, `bronze`,
  `silver`, `gold` DDLs.
- No Bronze/Silver/Gold transforms, no Glue job creation, no Athena analytics
  queries, no CI/CD, no IaC, no tests.

**The [prompts/scripts list](prompts/scripts%20list)** enumerates the intended
infra scripts (create_bucket, create_folders, upload_scripts, upload_ddls,
upload_source_data, create_database, deploy_tables, create_glue_jobs,
setup_project) — a roadmap, mostly still consolidated inside `util_functions.py`.

---

## 3. Directory Map

```
aws_reatails_sales/
├── athena_ddls/          # SQL DDL (metadata-as-code). Only raw_sales.sql today
├── config/               # Per-env Python config modules (dev.py). qa/prod TBD
├── data_generator/       # Synthetic CSV generator + master data + sample_data/
├── etl_utils/            # (empty) intended shared ETL helpers
├── glue/                 # (empty) intended Spark ETL jobs
├── infra/                # boto3 automation: clients, config load, deploy, DDL
├── metadata/             # sales.json — per-dataset pipeline metadata
├── prompts/              # planning notes / script inventory
├── requirements.txt      # pandas>=2.2.0, boto3>=1.38.0
└── README.md
```

---

## 4. Configuration Model

- **Environment config**: `config/<env>.py` (only `dev.py` exists). Loaded
  dynamically by `config_loader.load_environment("dev")` via `importlib`.
  Holds AWS region/account, bucket name, all S3 prefixes (raw/bronze/silver/
  gold/scripts/ddl/athena-results/temp), Glue settings (v5.0, G.1X, 2 workers,
  role `AWSGlueServiceRole-Retail`), Athena workgroup, and local dir names.
- **Table/dataset config**: JSON per dataset. `config_loader` expects them in a
  `table_configs/` directory, **but the only such file today lives in
  `metadata/sales.json`** — this is a known mismatch to resolve. `sales.json`
  declares catalog DBs per layer, source/storage buckets+prefixes, partition
  columns, load type, and paths to DDL/DML scripts.

### Known inconsistencies to reconcile as we build
1. `config_loader.TABLE_CONFIG_DIR = table_configs/` vs actual file in
   `metadata/`. Loader functions (`load_all_table_configs`, `get_table_names`)
   will find nothing until this is aligned.
2. DDL hardcodes database `retail_dev` and bucket `retail-data-lake-dev`, while
   `metadata/sales.json` names databases `retail_raw/bronze/silver/gold` and
   bucket `retail-data-lake`. Pick one naming convention.
3. `execute_ddl.py` runs DDL against Athena `Database: "default"` and only
   executes `raw_sales.sql`; there is no `CREATE DATABASE` step yet.
4. `util_functions.py` `__main__` uses `os.system` + a hardcoded partition path
   and relative dir — deployment path assumes CWD = repo root, not the project
   folder. Fragile; revisit when we harden deploy.

---

## 5. Data Contract (sales)

Generated columns (see `data_generator/generate_sales.py` +
`master_data.py`): `sale_id, sale_date, customer_id, product_id, product_name,
category, quantity, unit_price, discount_pct, total_amount, city, state,
store_id, payment_mode`.

- Raw table types everything as **STRING** (OpenCSVSerde), partitioned by
  `year/month/day` — casting happens downstream (Bronze).
- `total_amount = round(quantity * unit_price * (1 - discount_pct/100), 2)`.
  Note: the generator already computes `total_amount`, whereas the README frames
  it as a Bronze transformation (`quantity × unit_price`, no discount). Decide
  whether Bronze recomputes/validates it.
- 5 categories with price ranges, 10 products, 10 India metro stores, 5 payment
  modes, discounts in {0,5,10,15,20}.

---

## 6. Data Flow

**Current (batch, transitional):**
1. Daily CSV lands in S3 `raw/year=/month=/day=/`.
2. SQL DDL registers Glue Catalog tables (metadata-as-code, no Crawler).
3. Glue Spark job Raw→Bronze: cleanse, cast, standardize, write Parquet.
4. Athena queries serve business analytics.

**Target (Kappa lakehouse — see §2A):**
1. Store events published to Kafka topic `sales.raw` (replayable log).
2. Glue Structured Streaming reads the log continuously.
3. Iceberg Bronze (raw append) → Silver (`MERGE` upsert, dedup/clean) → Gold
   (incremental aggregates).
4. Lambda/SQS/SNS handle triggering, DLQ retries, DQ gates, alerting.
5. Athena (ad-hoc) + Redshift (BI/serving) query Gold Iceberg.
6. Reprocessing = replay Kafka / rebuild the Iceberg table (not a batch layer).

---

## 7. How to Run (current)

```bash
# from repo root, with AWS creds configured for us-east-1
pip install -r requirements.txt

# regenerate sample data
python data_generator/generate_sales.py

# provision bucket/folders + upload scripts/ddls/data (review __main__ first)
python infra/util_functions.py

# deploy raw DDL to Athena
python infra/execute_ddl.py
```

Sensitive/placeholder values: `config/dev.py` has `AWS_ACCOUNT_ID` and
`GLUE_CATALOG_NAME` placeholders/real-looking IDs — treat as environment-specific.

---

## 8. Roadmap — Kappa Migration Path (low → high complexity)

The axis we grow along. Bridge from the **current batch state** (CSV → Glue →
Athena, raw layer done) to the **Kappa lakehouse target (§2A)** incrementally —
Iceberg first, then streaming. Each phase is independently demoable.

- **P1 Foundations (in progress, batch):** S3, IAM, Boto3, Glue Catalog, Athena,
  raw layer. → Finish: `CREATE DATABASE` DDL, reconcile config/metadata dirs,
  make deploy scripts robust (split out of `util_functions.py` per `scripts
  list`).
- **Phase A — Iceberg first, still batch:** convert Bronze/Silver from Parquet
  to **Iceberg** with Glue *batch*. Learn `MERGE`, schema evolution, time
  travel *without* streaming complexity. Low-risk, high-value.
- **Phase B — Introduce Kafka:** `data_generator` becomes a Kafka producer
  emitting sales events (instead of daily CSVs). Land raw → Iceberg Bronze via a
  Glue **Streaming** job (Spark Structured Streaming).
- **Phase C — Event glue:** S3/Kafka → **Lambda** → **SQS** (with DLQ) →
  **SNS** for triggering, retries, alerting; add data-quality gates.
- **Phase D — Streaming Silver/Gold:** `MERGE`-based upserts into Silver,
  incremental aggregates into Gold Iceberg tables.
- **Phase E — Serving + platform:** **Redshift** Spectrum over Gold Iceberg (or
  COPY Gold marts in); prove reprocessing by replaying Kafka into a rebuilt
  table. Plus CI/CD, IaC (Terraform/CDK), unit tests, catalog versioning.

> Original README phases (P2 Bronze ETL, P3 partitioning/incremental, P4
> orchestration, P5 Silver/Gold+platform) still hold as sub-goals — they now map
> onto the Iceberg/streaming phases above.

---

## 9. Conventions & Notes for Future Work

- **Metadata-as-code**: prefer explicit SQL DDL over Crawlers; keep DDL
  version-controlled and env-parameterized (`${DATA_LAKE_BUCKET}`,
  `${RAW_PREFIX}`, `${BRONZE_PREFIX}` placeholders already supported in
  `execute_ddl.py`).
- **Config-driven**: no hardcoding — route new values through `config/<env>.py`
  and dataset JSON.
- **Environment promotion**: dev → qa → prod via separate config modules
  (only `dev` exists so far).
- Match existing code style: module-level section banners (`# ===== ... =====`),
  docstrings on functions, boto3 client factories from `infra/common.py`.
- When adding a new layer, update: DDL, dataset metadata JSON, Glue job, and
  **this file**.

---

_Keep this document in sync as the project grows. When behavior and this file
disagree, fix the code or fix the doc — don't leave them divergent._
