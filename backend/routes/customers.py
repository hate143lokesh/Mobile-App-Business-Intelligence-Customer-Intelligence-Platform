
from fastapi import APIRouter, Query, HTTPException
import pandas as pd
from pathlib import Path
from typing import Literal

router = APIRouter()

# ==================================================
# 1. LOAD CUSTOMER DATASET
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "Ecommerce_cleaned.csv"
)

try:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    customers_df = pd.read_csv(DATA_PATH)

    print("Customer dataset loaded successfully!")

except Exception as e:
    raise RuntimeError(
        f"Failed to load customer dataset: {str(e)}"
    ) from e


# ==================================================
# 2. CUSTOMERS API
# Pagination + Filtering + Sorting
# ==================================================

@router.get("/customers")
def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),

    device_type: int | None = Query(None, ge=0, le=2),
    purchased: int | None = Query(None, ge=0, le=1),

    sort_by: Literal[
        "revenue", "unit_price", "quantity"
    ] = Query("revenue"),

    order: Literal["asc", "desc"] = Query("desc")
):
    try:
        filtered_df = customers_df.copy()

        # Device type filter
        if device_type is not None:
            filtered_df = filtered_df[
                filtered_df["device_type"] == device_type
            ]

        # Purchase status filter
        if purchased is not None:
            filtered_df = filtered_df[
                filtered_df["purchased"] == purchased
            ]

        # Sorting
        filtered_df = filtered_df.sort_values(
            by=sort_by,
            ascending=(order == "asc")
        )

        total_records = len(filtered_df)

        # Pagination
        start = (page - 1) * limit
        end = start + limit

        paginated_data = filtered_df.iloc[start:end]

        records = (
            paginated_data.astype(object)
            .where(pd.notna(paginated_data), None)
            .to_dict(orient="records")
        )

        return {
            "success": True,
            "message": "Customer records retrieved successfully",
            "pagination": {
                "page": page,
                "limit": limit,
                "total_records": total_records,
                "total_pages": (
                    total_records + limit - 1
                ) // limit
            },
            "filters": {
                "device_type": device_type,
                "purchased": purchased
            },
            "sorting": {
                "sort_by": sort_by,
                "order": order
            },
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve customer records: {str(e)}"
        )


# ==================================================
# 3. CUSTOMER SUMMARY API
# ==================================================

@router.get("/customers/summary")
def get_customer_summary():
    try:
        total_records = len(customers_df)

        total_purchases = int(
            (customers_df["purchased"] == 1).sum()
        )

        total_non_purchases = int(
            (customers_df["purchased"] == 0).sum()
        )

        conversion_rate = (
            (total_purchases / total_records) * 100
            if total_records > 0 else 0
        )

        purchased_df = customers_df[
            customers_df["purchased"] == 1
        ]

        total_revenue = float(
            purchased_df["revenue"].fillna(0).sum()
        )

        average_order_value = (
            total_revenue / total_purchases
            if total_purchases > 0 else 0
        )

        return {
            "success": True,
            "message": "Customer summary generated successfully",
            "summary": {
                "total_records": total_records,
                "total_purchases": total_purchases,
                "total_non_purchases": total_non_purchases,
                "purchase_conversion_rate": round(
                    conversion_rate, 2
                ),
                "total_revenue": round(total_revenue, 2),
                "average_order_value": round(
                    average_order_value, 2
                )
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate customer summary: {str(e)}"
        )


# ==================================================
# 4. DEVICE TYPE ANALYTICS API
# ==================================================

@router.get("/customers/analytics/device")
def get_device_analytics():
    try:
        device_summary = (
            customers_df.groupby("device_type")
            .agg(
                total_records=("purchased", "count"),
                total_purchases=("purchased", "sum"),
                total_revenue=("revenue", "sum")
            )
            .reset_index()
        )

        device_summary["conversion_rate"] = (
            device_summary["total_purchases"]
            / device_summary["total_records"] * 100
        )

        records = (
            device_summary.round(2)
            .to_dict(orient="records")
        )

        return {
            "success": True,
            "message": "Device analytics generated successfully",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate device analytics: {str(e)}"
        )


# ==================================================
# 5. PRODUCT CATEGORY ANALYTICS API
# ==================================================

@router.get("/customers/analytics/category")
def get_category_analytics():
    try:
        category_summary = (
            customers_df.groupby("product_category")
            .agg(
                total_records=("purchased", "count"),
                total_purchases=("purchased", "sum"),
                total_revenue=("revenue", "sum")
            )
            .reset_index()
        )

        category_summary["conversion_rate"] = (
            category_summary["total_purchases"]
            / category_summary["total_records"] * 100
        )

        records = (
            category_summary.round(2)
            .to_dict(orient="records")
        )

        return {
            "success": True,
            "message": "Category analytics generated successfully",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate category analytics: {str(e)}"
        )


# ==================================================
# 6. MARKETING CHANNEL ANALYTICS API
# ==================================================

@router.get("/customers/analytics/channel")
def get_channel_analytics():
    try:
        channel_summary = (
            customers_df.groupby("marketing_channel")
            .agg(
                total_records=("purchased", "count"),
                total_purchases=("purchased", "sum"),
                total_revenue=("revenue", "sum")
            )
            .reset_index()
        )

        channel_summary["conversion_rate"] = (
            channel_summary["total_purchases"]
            / channel_summary["total_records"] * 100
        )

        records = (
            channel_summary.round(2)
            .to_dict(orient="records")
        )

        return {
            "success": True,
            "message": "Marketing channel analytics generated successfully",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate channel analytics: {str(e)}"
        )


# ==================================================
# 7. MONTHLY REVENUE ANALYTICS API
# ==================================================

@router.get("/customers/analytics/monthly")
def get_monthly_analytics():
    try:
        monthly_summary = (
            customers_df.groupby("visit_month")
            .agg(
                total_records=("purchased", "count"),
                total_purchases=("purchased", "sum"),
                total_revenue=("revenue", "sum")
            )
            .reset_index()
            .sort_values(by="visit_month")
        )

        monthly_summary["conversion_rate"] = (
            monthly_summary["total_purchases"]
            / monthly_summary["total_records"] * 100
        )

        records = (
            monthly_summary.round(2)
            .to_dict(orient="records")
        )

        return {
            "success": True,
            "message": "Monthly analytics generated successfully",
            "data": records
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate monthly analytics: {str(e)}"
        )
