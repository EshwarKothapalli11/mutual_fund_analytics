
-- Mutual Fund Analytics
-- Analysis 5: State-wise transaction analysis

USE mutual_fund_analytics;

SELECT
    state,
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT investor_id) AS unique_investors,
    ROUND(SUM(amount_inr) / 10000000, 2) AS total_amount_crore,
    ROUND(AVG(amount_inr), 2) AS average_transaction_inr
FROM investor_transactions
GROUP BY state
ORDER BY SUM(amount_inr) DESC;
