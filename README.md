# Matjar — Synthetic Dataset & ML Pipeline

Synthetic dataset generator and ML pipeline for [Matjar](https://github.com/OmarHashad1/Matjar), an AI-powered e-commerce platform (NestJS, FastAPI, Next.js). Since the platform hasn't launched yet and has no real user data, this repo generates realistic synthetic data matching the production Prisma schema, then trains and validates two ML systems ahead of real data becoming available.

## What this repo does

1. **Generates synthetic data** — Categories, Brands, Products, Product Variants, Users, UserEvents, Orders, and DailyProductMetrics, matching Matjar's real database schema field-for-field so the pipeline transfers cleanly once real data exists.

2. **Trains two separate ML systems**, both intended to run as part of the FastAPI `ml-service` in the main Matjar monorepo:
   - **Recommendation system** — collaborative filtering (`implicit`) trained on `UserEvent` data, producing per-user recommendations for `RecommendationCache`
   - **Demand forecasting** — trained on `DailyProductMetrics`, predicting future product demand for `DemandForecast`

## Structure

```
matjar-synthetic-data/
├── README.md
├── requirements.txt
│
├── data_generation/
│   ├── generate_categories.py
│   ├── generate_brands.py
│   ├── generate_products.py
│   ├── generate_product_variants.py
│   ├── generate_users.py
│   ├── generate_user_events.py
│   ├── generate_orders.py
│   └── generate_daily_metrics.py
│
├── data/
│   └── output/
│       ├── categories.csv
│       ├── brands.csv
│       ├── products.csv
│       └── ...
│
├── recommendation/
│   ├── config/
│   │   ├── config.yml
│   │   └── config.py
│   ├── processing/
│   │   ├── data_manager.py
│   │   └── features.py
│   ├── pipeline.py
│   ├── train_pipeline.py
│   └── predict.py
│
├── forecasting/
│   ├── config/
│   │   ├── config.yml
│   │   └── config.py
│   ├── processing/
│   │   ├── data_manager.py
│   │   └── features.py
│   ├── pipeline.py
│   ├── train_pipeline.py
│   └── predict.py
│
├── app/
│   ├── main.py
│   ├── api.py
│   └── schemas.py
│
└── notebooks/
    └── research.ipynb
```

## Data generation order

Tables are generated in dependency order, since later tables reference earlier ones by foreign key:

1. `Category` — no dependencies
2. `Brand` — no dependencies
3. `Product` — depends on Category, Brand
4. `ProductVariant` — depends on Product
5. `User` — no dependencies
6. `UserEvent` — depends on User, Product
7. `Order` / `OrderItem` — depends on User, ProductVariant
8. `DailyProductMetrics` — aggregated from UserEvent and Order data

## Why synthetic data

Matjar is pre-launch, so no real behavioral or transactional data exists yet. This repo lets the ML pipeline be built, tested, and validated now — matching the real schema — so it's ready to run against real data the moment the platform goes live. Synthetic data here is a stand-in for missing data, not an enhancement over real data — once Matjar has real users, this pipeline should be re-validated against real data.

## Tech stack

- Python, pandas, numpy
- `implicit` (collaborative filtering for recommendations)
- FastAPI (serving both models)
- `uv` (package management, matching the main Matjar repo)

## Status

🚧 In progress — synthetic data generation underway.

## Related

Main platform repo: [OmarHashad1/Matjar](https://github.com/OmarHashad1/Matjar)
