"""
Synthetic FMCG Dataset Generator
---------------------------------
Generates realistic, internally consistent synthetic data for an
FMCG Business Copilot project.

Dataset:
    products.csv
    sales.csv
    inventory.csv
    promotions.csv
    competitor_activity.csv
    pricing.csv
    stores.csv

The data intentionally contains business patterns that an AI agent
should be able to discover through MCP tools + RAG.
"""

from pathlib import Path
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd


# ============================================================
# CONFIG
# ============================================================

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# MASTER DATA
# ============================================================

PRODUCTS = [
    {
        "product_id": "P001",
        "product_name": "Dove Shampoo",
        "category": "Hair Care",
        "brand": "Dove",
        "base_price": 350,
    },
    {
        "product_id": "P002",
        "product_name": "Dove Conditioner",
        "category": "Hair Care",
        "brand": "Dove",
        "base_price": 320,
    },
    {
        "product_id": "P003",
        "product_name": "Lux Soap",
        "category": "Personal Care",
        "brand": "Lux",
        "base_price": 110,
    },
    {
        "product_id": "P004",
        "product_name": "Surf Excel",
        "category": "Home Care",
        "brand": "Surf Excel",
        "base_price": 280,
    },
    {
        "product_id": "P005",
        "product_name": "Vaseline Body Lotion",
        "category": "Skin Care",
        "brand": "Vaseline",
        "base_price": 260,
    },
    {
        "product_id": "P006",
        "product_name": "Axe Body Spray",
        "category": "Personal Care",
        "brand": "Axe",
        "base_price": 250,
    },
    {
        "product_id": "P007",
        "product_name": "Pepsodent Toothpaste",
        "category": "Oral Care",
        "brand": "Pepsodent",
        "base_price": 150,
    },
    {
        "product_id": "P008",
        "product_name": "Horlicks",
        "category": "Nutrition",
        "brand": "Horlicks",
        "base_price": 450,
    },
]


REGIONS = {
    "North": ["Delhi", "Punjab", "Haryana", "Uttar Pradesh"],
    "South": ["Karnataka", "Tamil Nadu", "Kerala", "Telangana", "Andhra Pradesh"],
    "East": ["West Bengal", "Odisha", "Bihar", "Jharkhand"],
    "West": ["Maharashtra", "Gujarat", "Rajasthan", "Goa"],
}


CHANNELS = [
    "Modern Trade",
    "General Trade",
    "E-Commerce",
    "Pharmacy",
]


COMPETITORS = [
    "L'Oreal",
    "P&G",
    "ITC",
    "Nivea",
    "Patanjali",
]


# ============================================================
# HELPERS
# ============================================================

def random_date(start_date, end_date):
    delta = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, delta))


def get_region(state):
    for region, states in REGIONS.items():
        if state in states:
            return region
    return None


# ============================================================
# PRODUCTS
# ============================================================

def generate_products():
    df = pd.DataFrame(PRODUCTS)
    df.to_csv(OUTPUT_DIR / "products.csv", index=False)

    print(f"Created products.csv: {len(df):,} rows")


# ============================================================
# STORES
# ============================================================

def generate_stores(n=500):
    rows = []

    for i in range(1, n + 1):

        region = random.choice(list(REGIONS.keys()))
        state = random.choice(REGIONS[region])

        channel = random.choice(CHANNELS)

        rows.append({
            "store_id": f"S{i:05d}",
            "store_name": f"Store {i:05d}",
            "region": region,
            "state": state,
            "city": f"{state} City {random.randint(1, 10)}",
            "channel": channel,
            "store_size": random.choice([
                "Small",
                "Medium",
                "Large"
            ]),
        })

    df = pd.DataFrame(rows)

    df.to_csv(OUTPUT_DIR / "stores.csv", index=False)

    print(f"Created stores.csv: {len(df):,} rows")

    return df


# ============================================================
# SALES
# ============================================================

def generate_sales(stores, rows_per_product_store=12):

    rows = []

    start_date = date(2025, 4, 1)

    months = [
        ("Q1", 2025, 4),
        ("Q1", 2025, 5),
        ("Q1", 2025, 6),

        ("Q2", 2025, 7),
        ("Q2", 2025, 8),
        ("Q2", 2025, 9),

        ("Q3", 2025, 10),
        ("Q3", 2025, 11),
        ("Q3", 2025, 12),

        ("Q4", 2026, 1),
        ("Q4", 2026, 2),
        ("Q4", 2026, 3),
    ]

    sale_id = 1

    for product in PRODUCTS:

        for _, store in stores.iterrows():

            for quarter, year, month in months:

                # Base demand
                base_units = random.randint(40, 150)

                region_factor = {
                    "North": 1.00,
                    "South": 1.10,
                    "East": 0.85,
                    "West": 1.15,
                }[store["region"]]

                channel_factor = {
                    "Modern Trade": 1.30,
                    "General Trade": 1.00,
                    "E-Commerce": 1.40,
                    "Pharmacy": 0.70,
                }[store["channel"]]

                units = base_units * region_factor * channel_factor

                # ------------------------------------------------
                # IMPORTANT BUSINESS PATTERN
                #
                # Dove Shampoo performs badly in South India
                # during Q3.
                # ------------------------------------------------

                if (
                    product["product_id"] == "P001"
                    and store["region"] == "South"
                    and quarter == "Q3"
                ):
                    units *= 0.81

                # Kerala suffers additional decline
                if (
                    product["product_id"] == "P001"
                    and store["state"] == "Kerala"
                    and quarter == "Q3"
                ):
                    units *= 0.78

                # Slight seasonal variation
                seasonal_factor = random.uniform(0.90, 1.10)

                units *= seasonal_factor

                units = max(1, int(units))

                price = product["base_price"]

                revenue = units * price

                rows.append({
                    "sale_id": f"SALE{sale_id:08d}",
                    "product_id": product["product_id"],
                    "product_name": product["product_name"],
                    "store_id": store["store_id"],
                    "region": store["region"],
                    "state": store["state"],
                    "channel": store["channel"],
                    "quarter": quarter,
                    "year": year,
                    "month": month,
                    "units_sold": units,
                    "unit_price": price,
                    "revenue": round(revenue, 2),
                })

                sale_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(OUTPUT_DIR / "sales.csv", index=False)

    print(f"Created sales.csv: {len(df):,} rows")

    return df


# ============================================================
# INVENTORY
# ============================================================

def generate_inventory(stores):

    rows = []

    inventory_id = 1

    for product in PRODUCTS:

        for _, store in stores.iterrows():

            availability = random.uniform(0.80, 1.00)

            # IMPORTANT:
            # Dove Shampoo + Kerala has inventory problem
            if (
                product["product_id"] == "P001"
                and store["state"] == "Kerala"
            ):
                availability = random.uniform(0.55, 0.68)

            # Rest of South India slightly affected
            elif (
                product["product_id"] == "P001"
                and store["region"] == "South"
            ):
                availability = random.uniform(0.82, 0.94)

            stock_capacity = random.randint(200, 1200)

            available_stock = int(stock_capacity * availability)

            rows.append({
                "inventory_id": f"INV{inventory_id:07d}",
                "product_id": product["product_id"],
                "store_id": store["store_id"],
                "region": store["region"],
                "state": store["state"],
                "stock_capacity": stock_capacity,
                "available_stock": available_stock,
                "availability_pct": round(
                    availability * 100, 2
                ),
            })

            inventory_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(OUTPUT_DIR / "inventory.csv", index=False)

    print(f"Created inventory.csv: {len(df):,} rows")

    return df


# ============================================================
# PROMOTIONS
# ============================================================

def generate_promotions():

    rows = []

    promotion_id = 1

    for product in PRODUCTS:

        for region in REGIONS:

            # Normal promotion
            discount_q2 = random.choice([
                5,
                10,
                15
            ])

            discount_q3 = random.choice([
                5,
                10,
                15
            ])

            # IMPORTANT BUSINESS PATTERN
            # Dove promotion falls sharply in South India
            if product["product_id"] == "P001" and region == "South":
                discount_q2 = 15
                discount_q3 = 5

            for quarter, discount in [
                ("Q2", discount_q2),
                ("Q3", discount_q3)
            ]:

                rows.append({
                    "promotion_id": f"PROMO{promotion_id:05d}",
                    "product_id": product["product_id"],
                    "region": region,
                    "quarter": quarter,
                    "discount_pct": discount,
                    "promotion_type": random.choice([
                        "Price Discount",
                        "Bundle",
                        "Buy One Get One",
                        "Retailer Incentive"
                    ]),
                })

                promotion_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_DIR / "promotions.csv",
        index=False
    )

    print(
        f"Created promotions.csv: {len(df):,} rows"
    )

    return df


# ============================================================
# COMPETITOR ACTIVITY
# ============================================================

def generate_competitor_activity():

    rows = []

    activity_id = 1

    for competitor in COMPETITORS:

        for region in REGIONS:

            # Base activity
            discount = random.randint(5, 15)

            activity_level = random.choice([
                "Low",
                "Medium",
                "High"
            ])

            # IMPORTANT:
            # Competitor launches aggressive campaign
            # in South India against Dove
            if competitor == "L'Oreal" and region == "South":

                discount = 20
                activity_level = "High"

                campaign = (
                    "Aggressive shampoo discount campaign "
                    "across South India modern trade"
                )

            else:

                campaign = random.choice([
                    "Retail promotion",
                    "Digital campaign",
                    "Influencer campaign",
                    "Retailer incentive",
                    "New product launch",
                ])

            rows.append({
                "activity_id": f"COMP{activity_id:05d}",
                "competitor": competitor,
                "region": region,
                "quarter": "Q3",
                "discount_pct": discount,
                "activity_level": activity_level,
                "campaign": campaign,
            })

            activity_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_DIR / "competitor_activity.csv",
        index=False
    )

    print(
        f"Created competitor_activity.csv: {len(df):,} rows"
    )

    return df


# ============================================================
# PRICING
# ============================================================

def generate_pricing():

    rows = []

    pricing_id = 1

    for product in PRODUCTS:

        for region in REGIONS:

            price = product["base_price"]

            # Small regional variation
            price *= random.uniform(0.97, 1.03)

            rows.append({
                "pricing_id": f"PRICE{pricing_id:05d}",
                "product_id": product["product_id"],
                "region": region,
                "list_price": round(price, 2),
                "currency": "INR",
            })

            pricing_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_DIR / "pricing.csv",
        index=False
    )

    print(
        f"Created pricing.csv: {len(df):,} rows"
    )

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("\nGenerating synthetic FMCG dataset...\n")

    generate_products()

    stores = generate_stores(
        n=500
    )

    sales = generate_sales(
        stores
    )

    generate_inventory(
        stores
    )

    generate_promotions()

    generate_competitor_activity()

    generate_pricing()

    print("\n--------------------------------")
    print("Dataset generation completed.")
    print("--------------------------------\n")

    print(f"Files generated in: {OUTPUT_DIR.resolve()}\n")

    for file in sorted(OUTPUT_DIR.glob("*.csv")):

        df = pd.read_csv(file)

        print(
            f"{file.name:<30} "
            f"{len(df):>10,} rows"
        )


if __name__ == "__main__":
    main()