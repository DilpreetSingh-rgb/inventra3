import streamlit as st
from utils.user import add_user


import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo



from utils.inventry import (
    add_product,
    view_products,
    update_product,
    delete_product
)

from utils.billing import (
    get_products,
    get_bill_no,
    save_bill
)

from utils.invoice import generate_invoice

from utils.sales_dashboard import (
    get_total_products,
    get_total_stock,
    get_today_sales,
    get_today_revenue,
    get_low_stock_items,
    get_inventory,
    view_sales,
    get_empty_stock_items,
    get_revenue_trend
)

from utils.stock_recomendation import get_stock_recommendations

from utils.recommendation import get_ai_recommendation

from utils.supplier import add_supplier,view_suppliers,update_supplier,delete_supplier

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Inventra",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------------- LOAD CSS ---------------- #
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ==========================
# CUSTOM CSS
# ==========================
st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.welcome-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-top: 60px;
}

.welcome-title {
    font-size: 42px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 10px;
}

.welcome-subtitle {
    font-size: 18px;
    color: #64748b;
    margin-bottom: 30px;
}

.stTextInput input {
    border-radius: 10px;
    padding: 10px;
}

.stButton button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

.stTextInput input {
    color: black !important;
}

.stTextInput input::placeholder {
    color: gray !important;
    opacity: 1 !important;
}

label {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SESSION STATE
# ==========================
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ==========================
# WELCOME PAGE
# ==========================
if st.session_state.user_name is None:

    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-title">
            🛒 Inventra
        </div>
        <div class="welcome-subtitle">
            AI-Powered Billing & Inventory Management System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    name = st.text_input(
        "👤 Enter Your Name",
        placeholder="Dilpreet Singh"
    )

    if st.button("Start Business"):

        if not name.strip():

            st.error(
                "Please enter your name"
            )

        else:

            add_user(name)

            st.session_state.user_name = name

            st.rerun()

    st.stop()
# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🛒 Inventra")

page = st.sidebar.radio(
    "Go to",
    [      
        "🧾 Billing",
        "📦 Inventory Management",
        "📈 Sales Dashboard",
        "💡 Stock Recommendations",
        "🔮 Demand Forecasting",
        "🚚 Supplier Management"
    ]
)

if page == "📦 Inventory Management":
    
    # ── Header ──────────────────────────────────────────────────────────────
    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%A, %d %B %Y · %H:%M"
    )
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>📦 Inventory Management</h1>
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    operation = st.selectbox(
        "Select Operation",
        [
            "View Products",
            "Add Product",
            "Update Product",
            "Delete Product"
        ]
    )

    # 1. ADD PRODUCT

    if operation == "Add Product":

        st.subheader("➕ Add Product")

        name = st.text_input("Product Name")

        price = st.number_input(
            "Price",
            min_value=0.0,
            step=1.0
        )

        stock = st.number_input(
            "Stock Quantity",
            min_value=0,
            step=1
        )

        if st.button("Add Product"):

            if not name:
                st.error("Please enter Product Name")
            
            else:
                try:

                    add_product(
                        name,                        
                        price,
                        stock,
                    )

                    st.success("✅ Product Added Successfully")

                except Exception as e:
                    st.error(f"Error: {e}")

    # 2. View Products 

    elif operation == "View Products":

        st.subheader("📋 Product List")
        
        products = view_products()
        st.dataframe(
            products,
            hide_index=True,
            use_container_width=True
        )
        
    # UPDATE PRODUCT

    elif operation == "Update Product":

        st.subheader("✏️ Update Product")
    
        product_id = st.text_input("Product ID")
    
        update_name = st.checkbox("Update Name")
        update_price = st.checkbox("Update Price")
        update_stock = st.checkbox("Update Stock")
    
        data = {}
    
        if update_name:
            data["name"] = st.text_input("New Product Name")
    
        if update_price:
            data["price"] = st.number_input(
                "New Price",
                min_value=0.0,
                step=1.0
            )
    
        if update_stock:
            data["stock"] = st.number_input(
                "New Stock",
                min_value=0,
                step=1
            )
    
        if st.button("Update Product"):
        
            if not product_id:
                st.error("Enter Product ID")
    
            elif not data:
                st.error("Select at least one field to update")
    
            else:
                try:
                
                    update_product(product_id, data)
    
                    st.success("✅ Product Updated Successfully")
    
                except Exception as e:
                    st.error(f"Error: {e}")

    # DELETE PRODUCT

    elif operation == "Delete Product":

        st.subheader("🗑️ Delete Product")

        product_id = st.text_input(
            "Enter Product ID"
        )

        if st.button("Delete Product"):

            if not product_id:
                st.error("Enter Product ID")

            else:
                try:

                    delete_product(product_id)

                    st.success("✅ Product Deleted Successfully")

                except Exception as e:
                    st.error(f"Error: {e}")   


elif page == "🧾 Billing":
    
    # ── Header ──────────────────────────────────────────────────────────────
    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%A, %d %B %Y · %H:%M"
    )
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>🧾 Billing</h1>
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    products = get_products()

    if "bill_items" not in st.session_state:
        st.session_state.bill_items = []

    if not products:

        st.warning("No products found")

    else:

        
        
        selected_product = st.selectbox(
            "Search Product",
            [p["name"] for p in products]
        )
        
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1
        )
        if st.button("Add Product"):
        
            product = next(
                p for p in products
                if p["name"] == selected_product
            )
        
            total = product["price"] * quantity
        
            st.session_state.bill_items.append(
                {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "quantity": quantity,
                    "unit_price": product["price"],
                    "total": total,
                    "stock": product["stock"]
                }
            )
        
            st.success(
                f"{product['name']} added to bill"
            )

        invoice_rows = []
        grand_total = 0

        for i, item in enumerate(
            st.session_state.bill_items,
            start=1
        ):

            invoice_rows.append(
                {
                    "Sr No": i,
                    "Product": item["product_name"],
                    "Qty": item["quantity"],
                    "Price": item["unit_price"],
                    "Total": item["total"]
                }
            )

            grand_total += item["total"]
        col1, col2 = st.columns(2)
        
        with col1:
        
            if st.button("🔄 New Bill"):
        
                st.session_state.bill_items = []
        
                st.rerun()
        
        with col2:
        
            st.info(
                f"Bill Number: {get_bill_no()}"
            )
            if invoice_rows:
                    
                st.write("### Bill Preview")
                st.write("### Current Items")

                for i, item in enumerate(
                    st.session_state.bill_items
                ):

                    col1, col2 = st.columns([5,1])

                    with col1:
                    
                        st.write(
                            f"{item['product_name']} | "
                            f"Qty: {item['quantity']} | "
                            f"₹{item['total']}"
                        )

                    with col2:
                    
                        if st.button(
                            "❌",
                            key=f"delete_{i}"
                        ):

                            st.session_state.bill_items.pop(i)

                            st.rerun()
                st.dataframe(
                    pd.DataFrame(invoice_rows),
                    use_container_width=True,
                    hide_index=True
                )

                st.write("### Remove Product")

                remove_index = st.selectbox(
                    "Select Product To Remove",
                    range(len(st.session_state.bill_items)),
                    format_func=lambda x:
                    f"{st.session_state.bill_items[x]['product_name']} "
                    f"(Qty: {st.session_state.bill_items[x]['quantity']})"
                )

                if st.button("❌ Remove Selected Product"):
                
                    st.session_state.bill_items.pop(
                        remove_index
                    )

                    st.rerun()

        st.metric(
            "Grand Total",
            f"₹{grand_total}"
        )

        if st.button("Generate Bill"):

            if not st.session_state.bill_items:

                st.error(
                    "Add at least one product"
                )

            else:

                stock_error = False

                for item in st.session_state.bill_items:

                    product = next(
                        p for p in products
                        if p["id"] == item["product_id"]
                    )
                
                    current_stock = product["stock"]
                
                    if item["quantity"] > current_stock:
                    
                        st.error(
                            f"Insufficient stock for {item['product_name']}"
                        )
                
                        stock_error = True

                if not stock_error:

                    bill_no = get_bill_no()

                    save_bill(
                        bill_no,
                        st.session_state.bill_items
                    )

                    pdf_file = generate_invoice(
                        bill_no,
                        invoice_rows,
                        grand_total
                    )

                    st.success(
                        f"✅ {bill_no} Generated Successfully"
                    )

                    st.write(
                        f"Grand Total: ₹{grand_total}"
                    )

                    with open(pdf_file, "rb") as file:

                        st.download_button(
                            label="📥 Download Invoice",
                            data=file,
                            file_name=pdf_file,
                            mime="application/pdf"
                        )
                    st.session_state.bill_items = []


elif page == "📈 Sales Dashboard":

    # ── Header ──────────────────────────────────────────────────────────────
    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%A, %d %B %Y · %H:%M"
    )
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>📈 Sales Dashboard</h1>
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_products = get_total_products()
    total_stock = get_total_stock()
    today_sales = get_today_sales()
    revenue = get_today_revenue()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Products",
            total_products
        )

    with c2:
        st.metric(
            "Total Stock",
            total_stock
        )

    with c3:
        st.metric(
            "Today's Sales",
            today_sales
        )

    with c4:
        st.metric(
            "Revenue",
            f"₹{revenue}"
        )

    report = st.selectbox(
        "Select Report",
        [
            "Overview",
            "Low Stock Items",
            "View Sales",
            "Empty Stock Items",
            "Revanue Analysis"
        ]
    )

    if report == "Low Stock Items":

        low_stock = get_low_stock_items()

        st.subheader(
            "⚠ Low Stock Products"
        )

        st.dataframe(
            low_stock,
            use_container_width=True,
            hide_index=True
        )
    elif report == "Overview":

        inventory = pd.DataFrame(
            get_inventory()
        )

        if inventory.empty:

            st.warning(
                "No products found"
            )

        else:


            low_stock_count = len(
                inventory[
                    inventory["stock"] < 10
                ]
            )

            inventory_value = (
                inventory["price"]
                * inventory["stock"]
            ).sum()

            out_of_stock = len(
                inventory[
                    inventory["stock"] == 0
                ]
            )

            col1, col2 = st.columns(2)

            with col1:
                
                st.metric(
                    "Inventory Value",
                    f"₹{inventory_value:,.2f}"
                )

            with col2:

                st.metric(
                    "Low Stock Items",
                    low_stock_count
                )

                st.metric(
                    "Out Of Stock",
                    out_of_stock
                )

            st.divider()

            st.subheader(
                "Inventory Preview"
            )

            st.dataframe(
                inventory,
                use_container_width=True,
                hide_index=True
            )

            st.subheader(
                "Stock Distribution"
            )

            chart_data = inventory[
                ["name", "stock"]
            ].set_index("name")

            st.bar_chart(
                chart_data
            )

    elif report == "View Sales":

        st.subheader("📋 Sales List")
        
        products = view_sales()
        st.dataframe(
            products,
            hide_index=True,
            use_container_width=True
        )        

    elif report == "Empty Stock Items":

        Empty_stock = get_empty_stock_items()
        st.subheader(
        "⚠ Empty Stock Products"
        )
        st.dataframe(
        Empty_stock,
        use_container_width=True,
        hide_index=True
        )

    elif report == "Revanue Analysis":
        
        st.title(
        "📈 Revenue Analytics"
        )

        days = st.slider(
            "Select Days",
            min_value=1,
            max_value=90,
            value=30
        )

        revenue_df = get_revenue_trend(
            days
        )

        total_revenue = (
            revenue_df["revenue"]
            .sum()
        )

        st.metric(
            "Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

        st.line_chart(
            revenue_df.set_index("date")
        )        



elif page == "💡 Stock Recommendations":

    # ── Header ──────────────────────────────────────────────────────────────
    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%A, %d %B %Y · %H:%M"
    )
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>💡 Stock Recommendations</h1>
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    recommendations = get_stock_recommendations()

    st.dataframe(
        recommendations,
        hide_index=True,
        use_container_width=True
    )


elif page == "🔮 Demand Forecasting":

    # ── Header ──────────────────────────────────────────────────────────────    
    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%A, %d %B %Y · %H:%M"
    )
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>🔮 Demand Forecasting</h1>
                <p>
                    Predict future product demand and
                    generate intelligent inventory recommendations.
                </p>
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    days = st.slider( "Forecast Period (Days)", min_value=1, max_value=30, value=7 )

    if st.button( "Generate Forecast", use_container_width=True ): 
        with st.spinner( "Analyzing sales history..." ):
            recommendations = get_ai_recommendation(days)

            st.dataframe(
                recommendations,
                hide_index=True,
                use_container_width=True
            )


elif page == "🚚 Supplier Management":
    
    # ── Header ──────────────────────────────────────────────────────────────
    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%A, %d %B %Y · %H:%M"
    )
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <h1>🚚 Supplier Management</h1>
            </div>
            <div class="timestamp">{now}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    operation = st.selectbox(
        "Select Operation",
        [
            "View suppliers",
            "Add suppliers",
            "Update supplier",
            "Delete supplier"
        ]
    )

    # 1. ADD supplier

    if operation == "Add suppliers":

        st.subheader("➕ Add supplier")

        name = st.text_input("supplier Name")

        phone_no = st.text_input(
        "Phone Number",
        max_chars=10
        )

        address = st.text_input("supplier address")

        if st.button("Add supplier"):

            if not name:
                st.error("Please enter supplier Name")
            elif not phone_no:
                st.error("Please enter supplier Phone Number")
            elif not address:
                st.error("Please enter supplier Address")
            
            else:
                try:

                    add_supplier(
                        name,                        
                        phone_no,
                        address,
                    )

                    st.success("✅ Product Added Successfully")

                except Exception as e:
                    st.error(f"Error: {e}")

    # 2. View supplier

    elif operation == "View suppliers":

        st.subheader("📋 Supplier List")
        
        suppliers = view_suppliers()
        st.dataframe(
            suppliers,
            hide_index=True,
            use_container_width=True
        )
        
    # UPDATE supplier

    elif operation == "Update supplier":

        st.subheader("✏️ Update Supplier")
    
        supplier_id = st.text_input("supplier ID")
    
        update_name = st.checkbox("Update Name")
        update_phone = st.checkbox("Update Phone Number")
        update_address = st.checkbox("Update Address")
    
        data = {}
    
        if update_name:
            data["name"] = st.text_input("New Product Name")
    
        if update_phone:
            data["phone_no"] = st.text_input("Phone Number",max_chars=10)

        if update_address:
            data["address"] = st.text_input("supplier address")
    
        if st.button("Update supplier"):
        
            if not supplier_id:
                st.error("Enter Supplier ID")
    
            elif not data:
                st.error("Select at least one field to update")
    
            else:
                try:
                
                    update_supplier(supplier_id, data)
    
                    st.success("✅ Supplier Updated Successfully")
    
                except Exception as e:
                    st.error(f"Error: {e}")

    # DELETE supplier

    elif operation == "Delete supplier":

        st.subheader("🗑️ Delete Supplier")

        supplier_id = st.text_input(
            "Enter Supplier ID"
        )

        if st.button("Delete Supplier"):

            if not supplier_id:
                st.error("Enter Supplier ID")

            else:
                try:

                    delete_supplier(supplier_id)

                    st.success("✅ Supplier Deleted Successfully")

                except Exception as e:
                    st.error(f"Error: {e}")   

