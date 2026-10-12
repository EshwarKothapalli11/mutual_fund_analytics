
-- Mutual Fund Analytics
-- Analysis 6: Payment mode and KYC status

USE mutual_fund_analytics;

SELECT
    payment_mode,
    kyc_status,
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT investor_id) AS unique_investors,
    ROUND(SUM(amount_inr) / 10000000, 2) AS total_amount_crore,
    ROUND(AVG(amount_inr), 2) AS average_transaction_inr
FROM investor_transactions
GROUP BY payment_mode, kyc_status
ORDER BY payment_mode, kyc_status;
