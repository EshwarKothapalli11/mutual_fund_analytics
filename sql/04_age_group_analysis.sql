
-- Mutual Fund Analytics
-- Analysis 4: Investor activity by age group

USE mutual_fund_analytics;

SELECT
    age_group,
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT investor_id) AS unique_investors,
    ROUND(SUM(amount_inr) / 10000000, 2) AS total_amount_crore,
    ROUND(AVG(amount_inr), 2) AS average_transaction_inr
FROM investor_transactions
GROUP BY age_group
ORDER BY SUM(amount_inr) DESC;
