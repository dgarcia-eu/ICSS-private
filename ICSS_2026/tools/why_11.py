TITLE = "Half a million rows, one lookup, a thousand times faster"
HOOK = ("An index turns a scan of the whole table into a jump, the database filters before the data moves, "
        "and a transaction keeps the money from vanishing when the program crashes halfway.")

CELLS = [
("md", """# Half a million rows, one lookup, a thousand times faster

A database is not a file that happens to hold a table. It answers questions in a
different way than a loop over rows, it decides where the work happens, and it
guarantees that half-done changes never become visible. This notebook shows all
three with SQLite, which is built into Python, on a table of half a million users."""),

("code", """import sqlite3, time
import numpy as np

rng = np.random.default_rng(0)
N = 500_000
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (user_id INTEGER, country TEXT, score REAL)")
countries = np.array(["DE", "FR", "IT", "ES", "PL", "NL", "AT", "CH"])
rows = zip(rng.permutation(N).tolist(),                       # user ids in random order
           countries[rng.integers(0, 8, N)].tolist(),
           rng.normal(50, 10, N).round(1).tolist())
db.executemany("INSERT INTO users VALUES (?, ?, ?)", rows)
db.commit()
print(db.execute("SELECT COUNT(*) FROM users").fetchone()[0], "rows")"""),

("md", """## 1. Finding one user

We look up 200 users by their id, first as the table is, then after creating an
index on `user_id`. `EXPLAIN QUERY PLAN` shows what the database does in each
case."""),

("code", """ids = rng.integers(0, N, 200).tolist()

def lookups():
    t0 = time.perf_counter()
    for i in ids:
        db.execute("SELECT score FROM users WHERE user_id = ?", (i,)).fetchone()
    return time.perf_counter() - t0

print("plan:", db.execute("EXPLAIN QUERY PLAN SELECT score FROM users WHERE user_id = ?", (1,)).fetchone()[-1])
t_scan = lookups()
print(f"200 lookups without index: {t_scan:.2f} s")

db.execute("CREATE INDEX idx_user ON users(user_id)")
print("plan:", db.execute("EXPLAIN QUERY PLAN SELECT score FROM users WHERE user_id = ?", (1,)).fetchone()[-1])
t_index = lookups()
print(f"200 lookups with index:    {t_index:.4f} s   ({t_scan / t_index:.0f}x faster)")"""),

("md", """Without the index the plan says `SCAN`: every lookup reads the whole table, half a
million rows, to find one. With the index it says `SEARCH ... USING INDEX`: the
database walks a tree of ids, a few dozen comparisons, and jumps to the row. The
lookups become hundreds to thousands of times faster, and the factor grows with the
table. This is the binary search tree and the hash table of session 3 again, kept up
to date by the database on every insert so that you never have to think about it.
A query that filters on a column without an index is the single most common reason
a database "is slow"."""),

("md", """## 2. Where the work happens

We want the average score per country. One way is to fetch every row into Python
and aggregate there; the other is to ask the database for the answer. Both are
correct. Count what crosses the boundary between the database and your program."""),

("code", """t0 = time.perf_counter()
all_rows = db.execute("SELECT country, score FROM users").fetchall()
sums, counts = {}, {}
for country, score in all_rows:
    sums[country] = sums.get(country, 0) + score
    counts[country] = counts.get(country, 0) + 1
in_python = {c: round(sums[c] / counts[c], 3) for c in sorted(sums)}
t_py = time.perf_counter() - t0
print(f"fetch everything, aggregate in Python: {t_py:.2f} s, {len(all_rows):,} rows moved")

t0 = time.perf_counter()
in_sql = dict(db.execute("SELECT country, ROUND(AVG(score), 3) FROM users GROUP BY country").fetchall())
t_sql = time.perf_counter() - t0
print(f"GROUP BY in the database:              {t_sql:.2f} s, {len(in_sql)} rows moved")
print("same answer:", in_python == in_sql)"""),

("md", """The database returns eight rows instead of half a million and is about twice as
fast even here, where nothing travels further than memory; the gap widens with a real database on another machine, where every
moved row travels over a network. The rule of the lecture is *bring the computation
to the data*: say what you want in SQL, and let the database decide how to compute
it. The mistake to avoid is the opposite one, pulling a million rows into pandas in
order to keep a hundred."""),

("md", """## 3. The transfer that crashes halfway

Two accounts, and a transfer of 30 from Anna to Ben that fails after the debit and
before the credit, which is what a crash, a lost connection or a bug in the middle
of an update looks like. First without a transaction, then with one."""),

("code", """def transfer(conn, amount, crash):
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE name = 'Anna'", (amount,))
    if crash:
        raise RuntimeError("connection lost")
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE name = 'Ben'", (amount,))

def total(conn):
    return conn.execute("SELECT SUM(balance) FROM accounts").fetchone()[0]

for mode in ["autocommit", "transaction"]:
    conn = sqlite3.connect(":memory:", isolation_level=None if mode == "autocommit" else "DEFERRED")
    conn.execute("CREATE TABLE accounts (name TEXT, balance REAL)")
    conn.execute("INSERT INTO accounts VALUES ('Anna', 100), ('Ben', 100)")
    conn.commit()
    try:
        transfer(conn, 30, crash=True)
        conn.commit()
    except RuntimeError:
        if mode == "transaction":
            conn.rollback()
    print(f"{mode:<12} after the crash: total = {total(conn):.0f}   "
          f"{conn.execute('SELECT name, balance FROM accounts').fetchall()}")"""),

("md", """In autocommit mode every statement is final on its own: the debit is written, the
credit never happens, and 30 units of money no longer exist anywhere. Inside a
transaction the debit is only provisional until `commit`, and the `rollback` after
the failure restores the state before the transfer began. That is atomicity, the A
of ACID: either the whole transfer happens or none of it does. The other three
letters make the same promise under concurrent users, against invalid states, and
across a power cut. A CSV file promises none of this."""),

("md", """**What we used:** [what a DBMS does](../Transcripts/11-Databases.md#3-what-a-dbms-does),
[transactions and ACID](../Transcripts/11-Databases.md#5-transactions-and-acid),
[tables, types, schemas and keys](../Transcripts/11-Databases.md#9-tables-types-schemas-and-keys-in-sql)
and [queries: selection, projection, aggregation](../Transcripts/11-Databases.md#11-queries-selection-projection-aggregation)
from session 11, and [binary search trees](../Transcripts/03-DataStructures.md#6-binary-trees-and-binary-search-trees)
from session 3."""),
]
