# Stylight Assignment Notes

## Test Instructions

1. The modified DDL can be seen in `db_psql.sql` which is tested on PostgreSQL 11.15.
2. An dotenv file with the name `.env` should be provided with `DATABASE_URL` entry. Example:

    ```env
    DATABASE_URL=postgres://postgres:postgres@localhost:5555/stylight
    ```

3. Create a virtual environment

   ```bash
   python3 -m venv venv 
   ```

4. Activate the environment

   ```bash
   source venv/bin/activate
   ```

5. Install the dependencies

   ```bash
   pip install *r requirements.txt 
   ```

6. Run the script

   ```bash
   python main.py
   ```

## Solutions

Although they mainly achieve the same thing, this solution highlights three different approaches:

### 1. Fetch and Process (Naive)

Fetches all records, calculates status on backend. No join, no filtering.

- **Pros:** Intuitiveness, fast development.
- **Cons:** Memory problems on high amount of records, overall inefficiency.

### 2. SQL View (Lazy)

Utilizes SQL views to pass business rules to database layer. No need backend calculations. Fetches view records and takes action accordingly.

- **Pros:** Less load on backend server, little to no memory problems expected if implemented well.
- **Cons:** Pushes responsibility of applying business rules to DBA, potentially causing more overhead on development time assuming different parties manage back-end and DB.

### 3. Transactions (Smart)

Utilizes record fetching one-by-one. Without fetching all records, starts a transaction and calculates budget on-the-go.

- **Pros:** No memory issues for large amount of records. Business rules are enforced on back-end layer.
- **Cons:** Transactions may have concurrency concerns if the script is run on schedule frequently and takes long to finish.
