from utils.inventry import view_products

def get_stock_recommendations():

    products = view_products()

    recommendations = []

    for _, product in products.iterrows():

        stock = product["stock"]

        if stock == 0:

            zone = "🔴 Red Zone"
            action = "Restock Immediately"

        elif stock <= 10:

            zone = "🟠 Orange Zone"
            action = "High Priority Restock"

        elif stock <= 20:

            zone = "🟡 Yellow Zone"
            action = "Monitor & Reorder Soon"

        else:

            zone = "🟢 Green Zone"
            action = "Stock Sufficient"

        recommendations.append(
            {
                "Product ID": product["id"],
                "Product": product["name"],
                "Stock": stock,
                "Zone": zone,
                "Recommendation": action
            }
        )

        zone_priority = {
            "🔴 Red Zone": 1,
            "🟠 Orange Zone": 2,
            "🟡 Yellow Zone": 3,
            "🟢 Green Zone": 4
        }

        recommendations.sort(
            key=lambda x: (
                zone_priority[x["Zone"]],
                x["Stock"]
            )
        )


    return recommendations