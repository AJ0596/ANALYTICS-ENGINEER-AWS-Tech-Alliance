# Interactive Sales Dashboard – AWS Tech Alliance Project

# Overview

This project was completed as part of the AWS Tech Alliance program at the University of Illinois Chicago (UIC).
The Tech Alliance initiative is designed to close skill gaps by offering hands-on experience with real-world, industry-aligned projects using AWS cloud tools.

Over the summer, our team was assigned to work with Olist, a B2B e-commerce platform connecting sellers with consumers. We collaborated with the Marketing & Sales department to solve strategic problems related to seller acquisition and go-to-market (GTM) planning.

---

# Problem Statement

Sellers on the Olist platform faced several key challenges:

- They lacked real-time insight into how they were performing.
- All performance tracking was manual, using Excel sheets downloaded from multiple sources.
- Business decisions were reactive due to the absence of centralized, trustworthy data.

---

# Objective

To build a centralized, interactive sales dashboard for sellers that enables them to:

- View total orders and revenue per seller
- Track unique customers and product performance
- Monitor delivery KPIs like on-time %, average delays, and late deliveries
- Analyze cancellation and return rates
- Visualize trends and performance by region, product category, and time

---

*Note*:  

All visualizations were created using **Amazon QuickSight**, powered by a live database view. Dashboards are not included here due to access limitations within the private AWS environment.

---

## Tools & Technologies Used

| Tool               | Purpose                                                      |
|--------------------|--------------------------------------------------------------|
| Amazon S3          | Store input `.csv` datasets                                  |
| AWS Glue (PySpark) | ETL pipeline to clean, transform, and load data              |
| Amazon RDS (MySQL) | Cloud-hosted relational database for the data warehouse      |
| Amazon QuickSight  | Interactive BI dashboard for seller KPIs                     |
| SQL (Views)        | Build performant, aggregated views for visualization         |
| DBeaver            | Schema design and live querying of MySQL database            |

---

# Architecture

CSV Files (Orders + Products + Sellers + Customers + Order Items)
->
Amazon S3
->
AWS Glue (ETL Job in PySpark)
->
Amazon RDS (MySQL Warehouse with Star Schema)
->
SQL View (seller_performance_view)
->
Amazon QuickSight (Connected to View)
->
Interactive Sales Dashboard

# Data Sources

- **olist_orders_dataset.csv**  
  Includes each order placed on Olist, along with timestamps and delivery details.

- **olist_order_items_dataset.csv**  
  Includes line-level details for each product in the order (price, freight, seller).

- **olist_customers_dataset.csv**  
  Contains customer ID, unique ID, and location.

- **olist_products_dataset.csv**  
  Contains product category and physical dimensions (used to analyze delivery performance for heavy items).

- **olist_sellers_dataset.csv**  
  Includes seller ID, location, and zip code.

---

# Key Visualizations in QuickSight

- Total Orders & Revenue per Seller 
  → Helps identify high-performing sellers over time.

- Seller Performance by Region  
  → Understand which regions face more delivery delays or cancellations.

- Product Category vs Revenue 
  → Analyze how different categories contribute to seller sales.

- On-Time vs Late Deliveries
  → Track average delivery delays and logistics issues.

- Cancellation & Return Rates  
  → Identify product types or sellers with fulfillment challenges.

---

# SQL View – seller_performance_view

All core metrics were pre-aggregated in a centralized SQL view to optimize dashboard performance.

This view:
- Reduces query load on QuickSight
- Aggregates all KPIs at the seller-product-month level
- Enables real-time insights with scheduled refreshes

---

# Result

This solution delivered real business value for the Olist Sales team:

- Manual reporting effort reduced by 100%
- Logistics delays decreased by over 70% through better inventory visibility 
- As a result, sellers using the dashboard improved their revenue by an average of 35%

# Contact

Feel free to reach out at:
  Email: sneela7@uic.edu/saiajayneel@gmail.com
  Ph: +1 312 792 5326

