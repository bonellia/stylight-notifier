# Stylight Assignment Notes

## Test Instructions

1. The modified DDL can be seen in `db_psql.sql` which is tested on PostgreSQL 11.15. Make sure to recover DB state from this file. You may also need to install `libpq5` depending on your PostgreSQL setup. Please refer to resources for a relevant link.
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

Fetches all records, calculates status on backend. No join, simple filtering.

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

## Final Notes

- Due to limited time of the assignment, I have implemented the first two solutions. Please use `main2.py` to use view based approach. This assignment could be completed using countless different combinations. Whether we push the responsibility to database layer or the back-end highly depends on trade-offs we would consider. To briefly elaborate on these considerations, we can mention the following:
  
  - Concurrency (running same operation script on different intervals with the possibility of atomicity concerns being relevant, see [ACID](https://www.geeksforgeeks.org/acid-properties-in-dbms/) for more information.)
  - Readability (having sophisticated SQL queries on the source code might not be preferred, especially without using an ORM library)
  - Memory management (as mentioned above, fetching all records into the memory may be problematic beyond certain thresholds, thus third solution might be mandatory where every action is processed and committed one-by-one with long transactions).

All in all this was a fun-small experiment. Depending on real constraints, the implementation would vary a lot, but for sake of not over-engineering it, I choose not to commit too much time into it.
