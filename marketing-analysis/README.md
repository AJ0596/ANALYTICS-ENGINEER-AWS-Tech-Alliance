
# Marketing Channel Analysis – AWS Tech Alliance Project

# Overview

This project was completed as part of the **AWS Tech Alliance program** at the University of Illinois Chicago (UIC).  
The Tech Alliance initiative is designed to close skill gaps by offering hands-on experience with real-world, industry-aligned projects using AWS cloud tools.

Over the summer, our team was assigned to work with **Olist**, a B2B e-commerce platform connecting sellers with consumers. We collaborated with the **Marketing & Sales department** to solve strategic problems related to seller acquisition and go-to-market (GTM) planning.

---

# Problem Statement

Olist uses various marketing channels such as **email campaigns, social media, search engine ads, and direct website forms** to attract new sellers.  
However, they lacked visibility into **which channels were most effective** in actually bringing sellers onto the platform.

# Key questions:
- Should Olist invest more in hiring sales reps for email outreach?
- Or should the budget shift toward paid social or search?
- Which channels drive the **best ROI** in terms of seller acquisition?

---

# Objective

To **analyze marketing channel performance** and help Olist:
- Visualize seller acquisition effectiveness per channel
- Understand ROI for each marketing method
- Make **data-driven decisions** on where to allocate future budget
- Realign GTM efforts for higher return on investment

*NOTE:*

**Visualizations were created in Amazon QuickSight to display closed deals, lead distribution, and conversion trends by channel. Visuals are not included here due to dashboard access being within a closed AWS environment.**

---

# Tools & Technologies Used

| Tool | Purpose |
|------|---------|
| **Amazon S3** | Store input `.csv` datasets |
| **AWS Glue (PySpark)** | ETL pipeline: clean, transform, and load data |
| **Amazon RDS (MySQL)** | Cloud-hosted relational database |
| **Amazon QuickSight** | Business Intelligence dashboard for visualizations |
| **SQL** | Create tables, perform joins, calculate KPIs |

---

# Architecture

For the sake of this project, a very straightforward approach was followed

CSV Files (Marketing + Deals)
->
Amazon S3
->
AWS Glue ETL 
->
Amazon RDS (MySQL Database)
->
Amazon QuickSight (Connected to RDS)
->
Interactive Dashboard


---

# Data Sources

# `olist_closed_deals_dataset.csv`
- Includes sellers who **actually signed up** on Olist.
- Key fields: `mql_id`, `seller_id`, `won_date`, `business_segment`, `lead_type`

# `olist_marketing_qualified_leads_dataset.csv`
- Includes **all marketing leads** that showed interest (via email, ads, social, etc.)
- Key fields: `mql_id`, `origin`, `first_contact_date`, `landing_page_id`

---

# Key Visualizations in QuickSight

1. Closed Deals per Marketing Channel  
   → Shows which channels convert the most leads into sellers.

2. Distribution of Qualified Leads by Channel  
   → Helps understand where most leads originate.

3. Lead-to-Deal Conversion Over Time  
   → Visualizes conversion rate trends with a calculated field.


# Recommended GTM strategy

We discovered that email and social media were the most effective channels in acquiring sellers.

Based on this analysis, we recommended:

1. Allocating 40% of the budget to email CRM tools and training reps.

2. Investing 20% in social media campaigns.

3. Distributing the remaining 40% across other underperforming channels (which previously consumed 60% of the budget).

4. This shift in budget realigned Olist’s GTM strategy toward high-performing channels and optimized ROI.

# Result

This strategy helped Olist reduce spending on low-performing channels by 33%, while increasing seller acquisition efficiency across email and social media by over 60%. 


