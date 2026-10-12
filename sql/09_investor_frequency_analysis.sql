-- Mutual Fund Analytics
-- Analysis 9: Investor transaction frequency

USE mutual_fund_analytics;

SELECT
    CASE
        WHEN transaction_count = 1 THEN '1 transaction'
        WHEN transaction_count BETWEEN 2 AND 5 THEN '2-5 transactions'
        WHEN transaction_count BETWEEN 6 AND 10 THEN '6-10 transactions'
        ELSE '11+ transactions'
    END AS frequency_group,
    COUNT(*) AS investor_count,
    ROUND(AVG(transaction_count), 2) AS average_transactions
FROM (
    SELECT
        investor_id,
        COUNT(*) AS transaction_count
    FROM investor_transactions
    GROUP BY investor_id
) AS investor_frequency
GROUP BY frequency_group
ORDER BY MIN(transaction_count);