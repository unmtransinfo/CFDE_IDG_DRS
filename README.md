# DrugCentral DRS API <img align="right" src="/doc/images/cfde_logo.png" height="120">

A RESTful API providing access to the DrugCentral database with support for JSON, CSV, and TSV export formats.

**Live API:** https://uxn2ycvimg.us-east-2.awsapprunner.com

## Overview

The DrugCentral DRS (Data Repository Service) API provides programmatic access to comprehensive drug information from the DrugCentral database. This API enables researchers, developers, and data scientists to query drug structures, activities, targets, products, and synonyms through a standardized REST interface.

## Base URL

```
https://uxn2ycvimg.us-east-2.awsapprunner.com
```

## Quick Start

### Check API Status

```bash
curl https://uxn2ycvimg.us-east-2.awsapprunner.com/
```

Response:
```json
{"status": "ok"}
```

### Get Data in JSON Format

```bash
# Get 5 structures
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/structures?limit=5"

# Get activities with pagination
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/act_table_full?skip=10&limit=20"
```

### Export Data in CSV Format

```bash
# Export structures as CSV
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/structures/csv?limit=100" -o structures.csv

# Export target components as CSV
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/target_component/csv?limit=50" -o targets.csv
```

### Export Data in TSV Format

```bash
# Export products as TSV
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/product/tsv?limit=100" -o products.tsv

# Export synonyms as TSV
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/synonyms/tsv?limit=200" -o synonyms.tsv
```

## Available Endpoints

### JSON Endpoints

All JSON endpoints support pagination via `skip` and `limit` parameters (default limit: 10).

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/` | Health check | `curl https://uxn2ycvimg.us-east-2.awsapprunner.com/` |
| `/structures` | Chemical structures | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/structures?limit=5"` |
| `/act_table_full` | Activity data | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/act_table_full?limit=5"` |
| `/target_component` | Target components | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/target_component?limit=5"` |
| `/product` | Drug products | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/product?limit=5"` |
| `/synonyms` | Drug synonyms | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/synonyms?limit=5"` |

### CSV Export Endpoints

All CSV endpoints support pagination via `skip` and `limit` parameters (default limit: 1000).

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/structures/csv` | Export structures as CSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/structures/csv?limit=100" -o structures.csv` |
| `/act_table_full/csv` | Export activities as CSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/act_table_full/csv?limit=100" -o activities.csv` |
| `/target_component/csv` | Export targets as CSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/target_component/csv?limit=100" -o targets.csv` |
| `/product/csv` | Export products as CSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/product/csv?limit=100" -o products.csv` |
| `/synonyms/csv` | Export synonyms as CSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/synonyms/csv?limit=100" -o synonyms.csv` |

### TSV Export Endpoints

All TSV endpoints support pagination via `skip` and `limit` parameters (default limit: 1000).

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/structures/tsv` | Export structures as TSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/structures/tsv?limit=100" -o structures.tsv` |
| `/act_table_full/tsv` | Export activities as TSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/act_table_full/tsv?limit=100" -o activities.tsv` |
| `/target_component/tsv` | Export targets as TSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/target_component/tsv?limit=100" -o targets.tsv` |
| `/product/tsv` | Export products as TSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/product/tsv?limit=100" -o products.tsv` |
| `/synonyms/tsv` | Export synonyms as TSV | `curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/synonyms/tsv?limit=100" -o synonyms.tsv` |

## CSV/TSV Export Feature

The API provides memory-efficient streaming export of data in CSV and TSV formats:

- **Streaming Implementation**: Uses Python generators to stream data without loading entire datasets into memory
- **Automatic Timestamps**: Downloaded files include timestamps in filenames (e.g., `structures_20231219_143022.csv`)
- **Proper Content Headers**: Sets appropriate Content-Type and Content-Disposition headers for browser downloads
- **Type Handling**: Correctly handles datetime objects (ISO format) and NULL values (empty strings)
- **Pagination Support**: Use `skip` and `limit` parameters to control data ranges

## Query Parameters

### Pagination

All endpoints support pagination:

- `skip` - Number of records to skip (default: 0)
- `limit` - Maximum number of records to return
  - JSON endpoints: default 10
  - CSV/TSV endpoints: default 1000

Example:
```bash
# Get records 100-200
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/structures?skip=100&limit=100"

# Export first 5000 structures as CSV
curl "https://uxn2ycvimg.us-east-2.awsapprunner.com/structures/csv?limit=5000" -o structures.csv
```

## Technical Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (DrugCentral)
- **ORM**: SQLAlchemy
- **Hosting**: AWS App Runner
- **Container Registry**: Amazon ECR

## Deployment

For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Developer Information

**Lead Developer**: Praveen Kumar, PhD (University of New Mexico)

**Principal Investigators**:
- Christophe Lambert, PhD (University of New Mexico)
- Jeremy Yang, PhD (University of New Mexico)

## Project Context

This API is part of the Illuminating the Druggable Genome (IDG) Data Coordinating Center (DCC) initiative, which develops tools and workflows for integration, harmonization, and FAIRification of IDG resources within the Common Fund Data Ecosystem (CFDE).

## License

This project is part of the CFDE IDG DCC and follows the applicable licensing terms.

## Acknowledgments

This work is supported by the NIH Common Fund through the Illuminating the Druggable Genome (IDG) program.

---

## Original Documentation

# CFDE_DRS_API <img align="right" src="/doc/images/cfde_logo.png" height="120">

The Illuminating the Druggable Genome (IDG) Data Coordinating Center
(DCC) develops code, tools, and workflows for integration, harmonization
and FAIRification of IDG resources for access and interoperability
in the Common Fund Data Ecosystem (CFDE).

Lead developer for the DRS API components is Praveen Kumar, PhD, of UNM.

The CFDE IDG DCC team is led by PIs Christophe Lambert, PhD, and Jeremy
Yang, PhD, of UNM.

## Data Repository Service (DRS) API

The Data Repository Service (DRS) API provides a generic interface to data repositories so data consumers, including workflow systems, can access data in a single, standardized way regardless of where it's stored or how it's managed. The primary functionality of DRS is to map a logical ID to a means for physically retrieving the data represented by the ID.

## Cloud Workspace Integration and Interoperability

DRS APIs are designed for integration and interoperability with the
Galaxy cloud workspace system, and being developed in cooperation with
the CFDE Cloud Workspace Implementation Center (CWIC). Moreover, DRS and
other industry and community standards are being employed for interoperability
with CFDE centers and resources of the NIH Common Fund and beyond.
