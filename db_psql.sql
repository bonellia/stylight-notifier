CREATE TABLE t_shops (
    a_id        SERIAL         NOT NULL,
    a_name      VARCHAR(255)    NOT NULL,
    a_online    BOOLEAN         NOT NULL,
    PRIMARY KEY (a_id)
);

CREATE TABLE t_budgets (
    a_shop_id       INT         NOT NULL REFERENCES t_shops (a_id),
    a_month         DATE            NOT NULL,
    a_budget_amount DECIMAL(10,2)   NOT NULL,
    a_amount_spent  DECIMAL(10,2)   NOT NULL,
    PRIMARY KEY (a_shop_id, a_month)
);


INSERT INTO t_shops
    (a_id,  a_name,             a_online)
VALUES
    (1,     'Steve McQueen',    TRUE),
    (2,     'Fashion Quasar',   FALSE),
    (3,     'As Seen On Sale',  TRUE),
    (4,     'H&R',              FALSE),
    (5,     'Meow Meow',        TRUE),
    (6,     'Dole & Cabbage',   FALSE),
    (7,     'George Manly',     TRUE),
    (8,     'Harrison Ford',    FALSE);

INSERT INTO t_budgets
    (a_shop_id, a_month, a_budget_amount, a_amount_spent)
VALUES
    (1, '2020-06-01', 930.00, 725.67),
    (2, '2020-06-01', 990.00, 886.63),
    (3, '2020-06-01', 650.00, 685.91),
    (4, '2020-06-01', 740.00, 746.92),
    (5, '2020-06-01', 630.00, 507.64),
    (6, '2020-06-01', 640.00, 946.32),
    (7, '2020-06-01', 980.00, 640.16),
    (8, '2020-06-01', 790.00, 965.64),
    (1, '2020-07-01', 960.00, 803.67),
    (2, '2020-07-01', 670.00, 715.64),
    (3, '2020-07-01', 890.00, 580.81),
    (4, '2020-07-01', 590.00, 754.93),
    (5, '2020-07-01', 870.00, 505.12),
    (6, '2020-07-01', 700.00, 912.30),
    (7, '2020-07-01', 990.00, 805.15),
    (8, '2020-07-01', 720.00, 504.25);
