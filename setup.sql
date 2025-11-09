
-- SQL to set up the SHIPMENTS table in Snowflake
-- This script should be run in your Snowflake account before executing the notebook.

CREATE OR REPLACE TABLE SHIPMENTS (
    PO_NUMBER VARCHAR,
    STATUS VARCHAR,
    EXPECTED_DELIVERY_DATE DATE
);

INSERT INTO SHIPMENTS (PO_NUMBER, STATUS, EXPECTED_DELIVERY_DATE) VALUES
('PO12345', 'Delayed', '2025-11-20'),
('PO67890', 'Delivered', '2025-10-20'),
('PO11223', 'In Transit', '2025-11-01');

-- Verify Data Setup (Optional)
SELECT * FROM SHIPMENTS;
