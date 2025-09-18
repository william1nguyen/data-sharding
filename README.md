# DBLab

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/postgresql-12+-336791.svg)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Project-Learning-orange)](#)

A simple learning project for experimenting with database sharding concepts and large-scale data techniques.

---

## Quick Start (TL;DR)

Copy-paste these 3 lines to start experimenting:

```bash
git clone https://github.com/yourusername/data-sharding.git
cd data-sharding && make start-dev-env
make dev
```

Watch the progress bars as data gets generated and distributed across shards 🚀

## Demo

### Progress Tracking

<img src="docs/demo/progress-tracking.png" alt="Data Generation Progress" width="70%"/>

### Performance Benchmarks

<img src="docs/demo/benchmark-result.png" alt="Benchmark Results" width="70%"/>

### Database Connection Test

<img src="docs/demo/connection-test.png" alt="Database Connection Test" width="70%"/>

### Complete Workflow

<img src="docs/demo/full-process.png" alt="Complete Workflow Demo" width="70%"/>

## Table of Contents

1. [Purpose](#purpose)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Project Structure](#project-structure)
8. [Development Commands](#development-commands)
9. [Notes](#notes)
10. [TODO](#todo)

---

## Purpose

This project helps me understand database sharding fundamentals by:

- **Database Sharding Simulation** - Simple hash-based data distribution across PostgreSQL instances
- **Synthetic Data Generation** - Create realistic test datasets to experiment with
- **Performance Comparison** - Basic benchmarking between single vs sharded database queries
- **Large Dataset Handling** - Learn techniques for processing millions of records efficiently

It's a personal laboratory for understanding how database scaling works in practice.

---

## Features

- Generate user data using Faker library
- Distribute data across configurable number of PostgreSQL shards
- Real-time progress tracking with multiple progress bars
- Simple modulo-based hash sharding implementation
- Basic query performance benchmarking suite
- Docker-based development environment setup
- Batch processing for memory-efficient data handling

---

## Prerequisites

Ensure your development environment is ready:

- Python 3.8+ with pip or uv package manager
- Docker and Docker Compose for database containers
- Basic understanding of PostgreSQL and database concepts
- Terminal/command line familiarity

---

## Installation

### Clone and Setup

```bash
git clone https://github.com/yourusername/data-sharding.git
cd data-sharding
```

### Start Development Environment

```bash
# Start PostgreSQL containers
make start-dev-env

# Run the application
make dev
```

---

## Configuration

### Environment Variables

Set up your database connections in `.env` file:

```bash
# Main database (coordinator)
MAINDB_URL=postgresql://user:password@localhost:5432/maindb

# Shard databases (comma-separated)
SHARD_URLS=postgresql://user:password@localhost:5433/shard0,postgresql://user:password@localhost:5434/shard1

# Data generation settings
MAX_GEN_USERS=10000
```

See [.env.example](.env.example) for complete configuration template.

### Database Schema

Database tables are automatically created using SQL scripts in `/sql`:

- `sql/init-main.sql` - Main database schema
- `sql/init-shard.sql` - Shard database schema

---

## Usage

### Basic Workflow

The main script runs everything automatically:

```bash
make dev
```

This performs:

1. **Connection Testing** - Verifies all database connections
2. **Data Generation** - Creates synthetic users in main database
3. **Data Migration** - Distributes users to shards using hash-based routing
4. **Performance Benchmarking** - Runs query tests on both architectures

### Customizing Data Volume

Control the number of users via environment variable:

```bash
# Generate 50,000 users
MAX_GEN_USERS=50000 make dev

# Generate 1 million users
MAX_GEN_USERS=1000000 make dev
```

### Individual Operations

While the main script runs everything, you can also:

```bash
# Start only the databases
make start-dev-env

# Stop databases when done
make stop-dev-env

# Check Docker containers
docker-compose -f docker-compose.yml -p data-sharding ps
```

## Project Structure

```
data-sharding/
├── src/
│   ├── database.py     # Core sharding logic and operations
│   ├── models.py       # User data model with dataclass
│   ├── env.py         # Environment configuration loader
│   ├── main.py        # Application entry point
│   └── utils/
│       └── progress.py # Progress bar utilities
├── sql/
│   ├── init-main.sql   # Main database schema
│   └── init-shard.sql  # Shard database schema
├── docker-compose.yml  # PostgreSQL containers
├── Makefile           # Development commands
├── .env.example       # Configuration template
└── README.md         # This file
```

---

## Development Commands

### Database Management

```bash
# Start PostgreSQL databases
make start-dev-env

# Stop databases
make stop-dev-env
```

### Application

```bash
# Run the main application
make dev

# Run with custom user count
MAX_GEN_USERS=100000 make dev
```

### Docker Operations

```bash
# View running containers
docker-compose -f docker-compose.yml -p data-sharding ps

# View logs
docker-compose -f docker-compose.yml -p data-sharding logs

# Connect to database directly
docker exec -it data-sharding_maindb_1 psql -U postgres -d maindb
```

---

## Notes

- **Memory Usage** - Large datasets (1M+ users) require sufficient system memory
- **Docker Resources** - Ensure Docker has adequate CPU and memory allocation
- **Progress Tracking** - Each shard gets its own progress bar during migration
- **Hash Distribution** - Uses simple `user_id % shard_count` for data routing
- **Connection Pooling** - Currently uses basic connection management
- **Data Persistence** - Database data persists between container restarts

---

## TODO

- [ ] Add data rollback functionality for testing different sharding scenarios
- [ ] Implement range-based partitioning as alternative to hash-based sharding
- [ ] Create simple connection pooling to handle more concurrent operations
- [ ] Add basic monitoring dashboard for query performance tracking
- [ ] Support for different data types (orders, products, transactions, etc.)
- [ ] Implement data migration tools for resharding experiments
- [ ] Add read replica simulation for read/write separation testing
- [ ] Basic caching layer integration (Redis) for performance comparison
- [ ] Support for testing with different shard counts dynamically
- [ ] Simple backup and restore functionality for experiment snapshots
- [ ] Query optimization techniques and indexing strategy experiments
- [ ] Load testing scenarios with concurrent users simulation
