# Stylight Assignment Notes

1. The modified DDL can be seen in `db_psql.sql` which is tested on PostgreSQL 11.15.

Three approaches:

- **Naive:** Fetches all records, calculates status on backend. Pros are intuitiveness, fast development. Cons: Memory problems on high amount of records.
- **View:** Utilizes SQL views to pass business rules to database layer. No need backend calculations. Fetches view records and takes action accordingly. Pros: Less load on backend server, little to no memory problems expected if implemented well. Cons: Pushes responsibility of applying business rules to DBA, potentially causing more overhead on development time assuming different parties manage back-end and DB.
- **Smart:** Utilizes record fetching one-by-one. Pros: Without fetching all records, starts a transaction and calculates budget on-the-go. Pros: No memory issues for large amount of records. Business rules are enforced on back-end layer. Cons: Transactions may have concurrency concerns if the script is run on schedule frequently.
