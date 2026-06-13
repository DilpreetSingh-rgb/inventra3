from utils.sales_dashboard import view_sales
import pandas as pd
from sklearn.linear_model import LinearRegression
from utils.inventry import view_products

def get_ai_recommendation(days):

    sales = view_sales()
    products = view_products()

    sales_ = sales[
        ["product_id", "product_name", "quantity", "created_at"]
    ]

    sales_["created_at"] = pd.to_datetime(
        sales_["created_at"]
    ).dt.date

    daily_sales = (
        sales_.groupby(
            ["product_id", "product_name", "created_at"]
        )["quantity"]
        .sum()
        .reset_index()
    )

    recommendations = []

    for pid in daily_sales["product_id"].unique():

        product_data = daily_sales[
            daily_sales["product_id"] == pid
        ]

        product_data = product_data.sort_values(
            "created_at"
        )

        product_data["day"] = range(
            1,
            len(product_data) + 1
        )

        x = product_data[["day"]]
        y = product_data["quantity"]

        model = LinearRegression()
        model.fit(x, y)

        future_days = []

        for i in range(
            len(product_data) + 1,
            len(product_data) + days + 1
        ):
            future_days.append([i])

        predictions = model.predict(
            future_days
        )

        recommendations.append(
            {
                "product_id": pid,
                "product_name": product_data["product_name"].iloc[0],
                "predicted_sales": max(0,round(predictions.sum())),
                "Available_Stock": products[products["id"]==pid]["stock"].iloc[0],
                "required_stock": max(round(predictions.sum()) - products[products["id"]==pid]["stock"].iloc[0], 0),
            }
        )
        
    recommendations = pd.DataFrame(recommendations) # dataframe

    recommendations = recommendations.sort_values(by="required_stock",ascending=False)


    return recommendations