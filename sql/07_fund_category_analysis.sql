-- Mutual Fund Analytics
-- Analysis 7: Fund category analysis

USE mutual_fund_analytics;

SELECT
    f.category,
    COUNT(t.transaction_id) AS transaction_count,
    COUNT(DISTINCT t.investor_id) AS unique_investors,
    ROUND(SUM(t.amount_inr) / 10000000, 2) AS total_amount_crore,
    ROUND(AVG(t.amount_inr), 2) AS average_transaction_inr
FROM investor_transactions AS t
JOIN fund_master AS f
    ON t.amfi_code = f.amfi_code
GROUP BY f.category
ORDER BY SUM(t.amount_inr) DESC;