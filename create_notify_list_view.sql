CREATE VIEW notify_list AS
SELECT *
FROM (SELECT a_shop_id       as shop_id,
             a_month         as period,
             a_budget_amount as budget_max,
             a_amount_spent  as budget_spent,
             a_name          as shop_name,
             a_online        as listed
      FROM t_budgets
               JOIN (SELECT * FROM t_shops WHERE a_online = true) AS ts
                    ON t_budgets.a_shop_id = ts.a_id) as online_listings
WHERE online_listings.period >= date_trunc('month', CURRENT_DATE);