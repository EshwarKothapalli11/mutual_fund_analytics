
-- Mutual Fund Analytics
-- Analysis 2: Transaction type comparison

USE mutual_fund_analytics;

SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT investor_id) AS unique_investors,
    ROUND(SUM(amount_inr) / 10000000, 2)
        AS total_amount_crore,
    ROUND(AVG(amount_inr), 2)
        AS average_transaction_inr,
    ROUND(AVG(amount_inr) / 1000, 2)
        AS average_transaction_thousand
FROM investor_transactions
GROUP BY transaction_type
ORDER BY SUM(amount_inr) DESC;
