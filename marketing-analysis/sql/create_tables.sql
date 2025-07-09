-- Table: olist_qualified_leads
CREATE TABLE olist_qualified_leads (
    mql_id VARCHAR(255) PRIMARY KEY,
    first_contact_date TIMESTAMP,
    landing_page_id VARCHAR(255) NOT NULL,
    origin VARCHAR(255)
);

-- Table: olist_closed_deals
CREATE TABLE olist_closed_deals (
    mql_id VARCHAR(255),
    seller_id VARCHAR(255) NOT NULL,
    sdr_id VARCHAR(255) NOT NULL,
    sr_id VARCHAR(255) NOT NULL,
    won_date TIMESTAMP,
    business_segment VARCHAR(255),
    lead_type VARCHAR(255),
    lead_behaviour_profile VARCHAR(255),
    business_type VARCHAR(255),
    FOREIGN KEY (mql_id) REFERENCES olist_qualified_leads(mql_id)
);

-- Indexes
CREATE INDEX idx_origin ON olist_qualified_leads(origin);
CREATE INDEX idx_won_date ON olist_closed_deals(won_date);
CREATE INDEX idx_business_segment ON olist_closed_deals(business_segment);
