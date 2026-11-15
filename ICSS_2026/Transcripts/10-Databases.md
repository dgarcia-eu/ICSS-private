# Session 10: Databases

<style>
figure, .figure, .float { margin: 1.4em 0 1.8em 0; }
figure img, .float img { display: block; max-width: 100%; }
figcaption, .figcaption, .figure p.caption { margin-top: 0.3em; font-size: 0.88em; color: #555; }
details { margin: -0.5em 0 2.2em 0; }
</style>

*Introduction to Computing for the Social Sciences · lecture transcript*

**Reading for this session:** chapter 4, "Databases", of Foster, Ghani,
Jarmin, Kreuter & Lane (eds.), *Big Data and Social Science* (2017). For SQL
practice, the W3Schools tutorial at <https://www.w3schools.com/sql/default.asp>.
Full references at the end.

---

## Contents

1. [Databases](#databases)
2. [Relational databases](#relational-databases)
3. [Structured Query Language (SQL)](#sql)

---

<!-- MOTIVATION-SECTION:BEGIN -->
## Motivating examples

<!-- MOTIVATION:M10-A:BEGIN -->
### A · The 15,841 cases that fell off the end of a spreadsheet

Between 25 September and 2 October 2020, during the second wave of the
pandemic, the English contact-tracing system lost 15,841 positive COVID-19
test results. The people who tested positive were told their result but their
contacts were not traced. An estimated 50,000 people had been exposed and
were never contacted. The cause was a file format. Laboratories submitted
results as CSV files and the process that collated them loaded these files
into `.xls`, the Excel format from before 2007, whose worksheets hold a
maximum of 65,536 rows. When the file of a laboratory exceeded that limit,
the rows beyond it were discarded without any warning. Nothing was logged and
nothing failed, so the collation completed successfully every day.

It is easy to conclude that someone used the wrong tool. It is more useful to
ask what a database would have given in this situation, because each of the
following guarantees is a topic of this session:

- **Errors instead of silence.** Any storage system has limits, and what
  matters is whether exceeding a limit produces an error or a wrong answer. A
  database rejects an insert that it cannot perform and reports it, while the
  spreadsheet kept the first 65,536 rows and reported nothing.
- **Constraints enforced by the system.** A schema can declare that a test
  result must have a patient identifier, a date and a valid result code, so
  that malformed data cannot be inserted. In a spreadsheet these rules exist
  only in the head of the person who is doing the work.
- **Transactions.** A load is performed completely or not at all, so a load
  that fails halfway leaves the database as it was before instead of
  partially updated. This property is called atomicity and it is one of the
  ACID properties.
- **Concurrency.** Several laboratories writing at the same time is the
  normal case for a database, while with files on a shared drive it often
  leads to lost updates.
- **One copy.** The question of how many positive cases there were on 28
  September has one answer, instead of one answer per person who has a copy
  of the file.

These guarantees are what makes a database different from a spreadsheet, and
you lose them when you keep your data in a spreadsheet.

In this session you will learn what a database and a database management
system are, and the reasons to use one, namely data independence,
standardization and concurrency. We will learn about transactions and the
ACID properties, which state formally that it should not be possible to load
half of a file. We will also learn about the relational model, keys and
normal forms, i.e. how the database itself enforces that a fact is recorded
once and correctly. For your own research data, ask yourself whether anyone
would find out if 5% of the records were lost without a warning. If nobody
would find out, the format in which you keep the data is a problem.

<!-- MOTIVATION:M10-A:END -->
<!-- MOTIVATION:M10-B:BEGIN -->
### B · Two seats, one airplane

There is one seat left on a flight. Two agents in two cities click "book" in
the same second, and each program does the following, which looks correct:

```
free ← read the number of free seats          # both agents read 1
If free > 0
      then write free - 1 as the number of free seats
           issue the ticket
```

Let's trace what happens when the two programs run at the same time. Agent A
reads 1 and, before A writes, agent B also reads 1. Both see a free seat, so
both write 0 and both issue a ticket. The seat has been sold twice and the
seat count says 0, which would be the same after one sale or after a hundred
sales. If you read the code of either program on its own, you will not find a
mistake. The defect is not in either program. Instead, it is in the order in
which their steps are interleaved, which you cannot see in the source code of
any single program. This is called a race condition, and it is the reason why
concurrent systems are harder to get right than sequential ones. It is also
not a rare case, because it can happen in any system with more than one user,
such as booking systems, ticketing, inventory, appointment slots or vaccine
doses. Any program of the form "read a value, decide, write it back" can fail
in this way.

The answer of databases is the *transaction*, a group of operations that must
happen completely or not at all, and that must behave as if nothing else ran
at the same time. Transactions give four guarantees that are known by the
acronym ACID:

- **Atomicity** means that all of the transaction happens or none of it, so a
  booking that fails partway leaves no trace.
- **Consistency** means that a transaction that succeeds leaves the database
  valid, so a constraint like "seats sold ≤ capacity" cannot be violated.
- **Isolation** means that the outcome of running transactions concurrently
  must equal the outcome of running them one after another in some order.
  This is the property that rules out the interleaving above.
- **Durability** means that once a transaction is confirmed, it survives a
  crash, a power cut, or the server catching fire.

Isolation needs to be stated carefully, because it does not say that
transactions run one at a time, which would be far too slow. Instead, it says
that the result must be indistinguishable from the result of some serial
order, so the database can interleave the operations as much as it wants as
long as nobody can tell the difference.

In this session you will learn about transactions and the ACID properties,
and about concurrency as one of the three reasons to use a database, together
with data independence and standardization. We will start with the examples
of flight reservations and vaccine distribution, which both have this problem
at a large scale. If you share a data file that several people edit at the
same time, you have the same problem at a small scale.

<!-- MOTIVATION:M10-B:END -->
<!-- MOTIVATION:M10-C:BEGIN -->
### C · Whose number is right?

This example has no dramatic outcome and no news coverage, but it is what
often happens in research groups. A project keeps a list of participants,
which starts as one file. Someone needs it for an analysis and copies it.
Someone else needs a version with the new wave merged in. A third person
keeps the master file but is on leave when a participant withdraws, so the
withdrawal is applied to the copy of somebody else. Three months later there
are three files. One has the corrected spelling of a name, one has the new
wave and one has the withdrawal, but none has all three changes. The counts
differ by 47 and nobody knows which file is the right one. The only way to
find out is to reconcile the three files manually, and this is often
impossible because none of the changes was recorded as a change. Nobody was
careless, because each person did a correct and necessary thing to the copy
that they had. The failure is in how the data was organized. The same fact
was stored in more than one place, so the copies could disagree, and after
some time they did.

The answer of the relational model is a design principle that we will follow
through this session, namely that every fact should be stored in exactly one
place. Within a table, a primary key enforces this with one row per
participant, identified by an identifier that never changes even if the name
does. Between tables, a foreign key enforces it because other tables refer to
that participant instead of repeating their details. Normalization is the
systematic removal of the repetition that makes disagreement possible. The
failures that repetition allows have names:

- An **update anomaly** changes a value in one place and not in another, so
  the data contradicts itself. This is what happened in the story above.
- An **insertion anomaly** means that you cannot record a fact because there
  is nowhere to put it without inventing unrelated data.
- A **deletion anomaly** means that removing one record also destroys
  unrelated information that was stored in the same row.

A shared database does not make people more careful. Instead, it prevents the
outcome above, because there is one row for each participant, one place to
change the name, and a record of who changed it and when.

In this session you will learn about the flat and the relational model, keys,
foreign keys and normal forms, with an example of the same kind of
repetition. We will also learn why a single store is better than a folder of
files, and how transactions deal with edits that happen at the same time. For
your own project, ask yourself how many files you have to edit if one value
changes. If the answer is more than one, the same failure can happen to you
even if you have not noticed it yet.

<!-- MOTIVATION:M10-C:END -->

---

<!-- MOTIVATION-SECTION:END -->
## 1. Why databases exist: two examples {#databases}
We start with two examples. A flight reservation system has to know at every
moment which seats on which flights are free, and it has to answer that
question for thousands of agents at the same time. Two people must not be
sold the same seat. A booking that fails halfway, for example with the seat
taken but the payment not charged, must leave no trace. A vaccine
distribution system receives doses at a warehouse, ships them to vaccination
centers, administers them to named people on given dates, and schedules
second doses. The same person and the same batch appear in several places,
and everything has to stay consistent as the information moves through the
system. Both examples share three problems, namely that many users work at
the same time, that data refers to other data, and that operations must not
be left half done. The rest of this session is about how databases solve
these three problems.

---

## 2. Databases and DBMS

Informally, a database is an organized collection of data. An Excel table is
a very simple database. What makes a collection of data a database is that it
enables fast access and the ability to access the data in a structured way. A
*database management system* (DBMS) is a software application that enables
the interaction between the user and the actual database. It implements the
definition, creation, querying, updating and administration of a database,
and the data may be distributed at different locations. Examples of DBMSs are
MySQL, PostgreSQL, Access and Oracle. Another example is SQLite, which is a
whole DBMS in a single file and probably the first one that you will use.

Formally, a *database* (DB) is a set of related data together with the formal
organization and interdependence of these data. Access to the data and its
manipulation are provided through a corresponding DBMS. The distinction
matters, because the database is the data plus its organization, while the
DBMS is the program that you use to reach the data. For example, when people
say "we use Postgres" they are naming the DBMS and not the database. The
usual icon of a database is a cylinder, which is a stylized hard-drive
platter from the time when a database was physically a stack of spinning
disks.

---

## 3. What a DBMS does

A database management system has four characteristics:

- **Data definition** is the creation, modification and deletion of the
  definitions that define the organization of the data, i.e. the
  relationships among the entries in the database.
- **Updating** is the insertion, modification and deletion of the actual
  content, i.e. of the individual data entries.
- **Retrieval** or **querying** returns information for specific query
  inputs, which can be used by any downstream application.
- **Administration** covers user management, data security, performance, data
  integrity, concurrency, and the protection against database corruption and
  system failure.

We can see the four characteristics in the small table below, which we will
use as an example.

| Name | Birth | Class | Product | Num |
|---|---|---|---|---|
| Hans | 1998 | T1 | Milk | 00111 |
| Fred | 1999 | T1 | Tea | 00222 |
| Hans | 1998 | T1 | Tea | 00222 |
| Anna | 2000 | W1 | Milk | 00111 |
| Pat | 1998 | W1 | Tea | 00222 |
| Hans | 1998 | T1 | Milk | 00111 |
| Anna | 2000 | W1 | Milk | 00111 |
| Fred | 1999 | T1 | Milk | 00111 |

Data definition is deciding that there are these five columns with these
types. Updating is, for example, adding the row of Pat. Querying is asking
for the rows with `Product = Tea and Birth < 1999`, which returns the tea
rows of Hans and Pat but not the one of Fred, because Fred was born in 1999.
Administration is everything that makes the table survive a power cut and the
simultaneous work of three hundred users.

---

## 4. Why use a database?

There are three reasons to use a database:

- **Data independence** means that applications and users do not need to
  worry about how the data are structured and stored. *Logical data
  independence* protects them from changes to the logical structure of the
  data, so a new entity or attribute can be added without affecting existing
  usage. *Physical data independence* protects them from changes of the
  physical layout, so the user does not have to care about information
  coding, disk space and similar details. For example, we learned in the
  Information Coding session that a date can be stored as a 32-bit integer or
  as a string, and you do not want to deal with that difference in your
  analysis script.
- **Standardization** means that data formats and methods of accessing data
  are platform independent. Recall the problems of parsing a CSV file with
  conflict events in Python. Every reader has to guess the encoding, the
  separator, the quoting convention and what a missing value looks like,
  because a CSV file has no schema. A database has a schema, and it can serve
  flexible output schemas to different users and purposes from the same
  stored data.
- **Concurrency** means that a database allows the simultaneous usage by many
  users without the problem of conflicting updates, using robust protocols
  that avoid database corruption. This is the problem of the flight booking
  example, and we will see next how transactions solve it.

---

## 5. Transactions and ACID

A *transaction* is a series of data manipulations that must not be
interrupted, i.e. all the operations in a transaction have to be fully
performed or completely rewound. Database transactions have four properties
that are remembered by the acronym ACID:

- **Atomicity** means that each transaction stands on its own and that a
  rewind is possible.
- **Consistency** ensures that any transaction that succeeds maintains the
  validity of the database.
- **Isolation** ensures that it does not matter whether we execute our
  transactions serially or concurrently.
- **Durability** requires that any transaction that has completed survives
  permanently, also in case of an error, a crash or a loss of power.

A common example is a bank transfer that subtracts 100 from account A and
adds 100 to account B. Atomicity says that the two operations happen
completely or not at all, so there is no state in which the money has left A
and has not arrived at B. Isolation says that if someone reads both balances
while the transfer runs, they see either the state before or the state after
the transfer but never the state in the middle. Durability says that once the
DBMS reports success, a loss of power does not undo the transfer. Isolation
is the hardest of the four properties to state precisely. It means that a
concurrent execution is only acceptable if its result is indistinguishable
from the result of some serial execution.

You can see atomicity at work in the third part of the practical Python
examples, where a transfer that crashes halfway loses money without a
transaction and is rolled back with one.

---

## 6. Database models: flat and relational {#relational-databases}
*Database models* define the structure of a database. They set its logical
structure in terms of data storage, organization and manipulation, and they
are ultimately about how the relationship between related pieces of
information is represented. We will learn about two models:

- The **flat model**, also known as the spreadsheet, is a single
  two-dimensional array of data elements. The members of a row are related
  and form an entry, while the members of a column describe the same property
  or characteristic.
- The **relational model** represents the data through sets of linked tables
  that share a common key. You can think of it as many spreadsheets that each
  store a specific piece of information and that are linked through a unique
  key.

We can see the problem of the flat model in the purchase table below.

| Name | Birth | Class | Product | Productnr | Date |
|---|---|---|---|---|---|
| Hans | 1998 | T1 | Milk | 00111 | 06.03.2020 |
| Fred | 1999 | T1 | Tea | 00222 | 06.03.2020 |
| Hans | 1998 | T1 | Tea | 00222 | 06.03.2020 |
| Anna | 2000 | W1 | Milk | 00111 | 06.03.2020 |
| Verena | 1998 | W1 | Tea | 00222 | 07.03.2020 |
| Hans | 1998 | T1 | Milk | 00111 | 07.03.2020 |
| Anna | 2000 | W1 | Milk | 00111 | 08.03.2020 |
| Fred | 1999 | T1 | Milk | 00111 | 08.03.2020 |

Data is repeated across the table. This is an inefficient use of space,
because for example the birth year of Hans is stored three times. It also
creates problems when updating. For example, if the Productnr of Milk is now
00333, you must find and change every row where the product is Milk. If you
miss one row, the table contains two contradictory facts. This second problem
is called an *update anomaly* and it is the reason why the relational model
exists. The same data can be stored in the three linked tables below.

**Table `purchase`**

| Nr | Date | Name | Product |
|---|---|---|---|
| 1 | 06.03.2020 | 1 | 1 |
| 2 | 06.03.2020 | 2 | 2 |
| 3 | 06.03.2020 | 1 | 2 |
| 4 | 06.03.2020 | 3 | 1 |
| 5 | 07.03.2020 | 4 | 2 |
| 6 | 07.03.2020 | 1 | 1 |
| 7 | 08.03.2020 | 3 | 1 |
| 8 | 08.03.2020 | 2 | 1 |

**Table `Names`**

| Nr | Name | Birth | Class |
|---|---|---|---|
| 1 | Hans | 1998 | T1 |
| 2 | Fred | 1999 | T1 |
| 3 | Anna | 2000 | W1 |
| 4 | Verena | 1998 | W1 |

**Table `Product`**

| Nr | Product | Productnr |
|---|---|---|
| 1 | Milk | 00111 |
| 2 | Tea | 00222 |

Now the Productnr of Milk is stored in exactly one cell. Changing it is one
update, so it cannot be done inconsistently.

---

## 7. Keys and normal forms

The *primary key* of each table is its `Nr` column, i.e. a value that
uniquely identifies a row. *Foreign keys* reference primary keys on another
table or on the same table. For example, in `purchase` the columns `Name` and
`Product` are foreign keys that hold `Nr` values of `Names` and `Product`.
The DBMS can enforce a foreign key. For example, you cannot insert a purchase
that refers to product 7 if there is no product 7. This is called
*referential integrity* and you lose it when you keep your data in
spreadsheets.

Relational database designs can be standardized using *normal forms*. In the
example above, `Class` is still stored as a string inside `Names` and it
should be its own table, as shown below.

**Table `Names`**

| Nr | Name | Birth | Class |
|---|---|---|---|
| 1 | Hans | 1998 | 1 |
| 2 | Fred | 1999 | 1 |
| 3 | Anna | 2000 | 2 |
| 4 | Verena | 1998 | 2 |

**Table `Classes`**

| Nr | Name |
|---|---|
| 1 | T1 |
| 2 | W1 |

Now we can update the name of a class without having to edit the `Names`
table or the `purchase` table. For example, renaming class T1 to "Tuesday-1"
is an edit of a single cell. The general idea behind normalization is that
every fact should be stored in exactly one place. When you find yourself
repeating a value, that value should probably have its own table with its own
key.

---

## 8. SQL: what kind of language it is {#sql}
SQL is a special-purpose language specifically developed for managing data
through relational database systems. It consists of three co-dependent
language definitions:

- The **data definition language** (DDL) defines relational schemata. It
  creates, alters and deletes tables and their attributes.
- The **data manipulation language** (DML) inserts, deletes and modifies the
  entries of tables and queries one or more tables.
- The **data control language** (DCL) controls the access to the data stored
  in the database. It grants, revokes and modifies user access rights.

SQL is a very high-level programming language. Its performance is good
because the actual operations are well optimized. There are many different
standards of SQL, but a typical DBMS supports all of them. The execution of
SQL is also highly parallelizable by construction. SQL is a *declarative*
language, which means that you define what you want and the DBMS takes care
of how to do it. You can also write procedural SQL with special instructions,
but it is very inefficient.

This is different from the programs that we have written so far in this
course. In the Software session we learned about imperative programming,
where you write how to compute the result, for example loop over this list,
test that condition and append to that other list. In SQL you state the
property that the answer has and the query planner of the DBMS chooses the
algorithm, i.e. which index to use, in which order to join the tables, and
whether to sort or to hash. This is also why SQL parallelizes so well,
because you never committed to an order of operations and the system is free
to choose one. The flow is always the same. First, the query goes as SQL to
the DBMS. Then, the DBMS works on the database. Finally, the result comes
back.

---

## 9. Tables, types, schemas and keys in SQL

A *table* is a multiset of tuples coding the attributes specified by the
database schema. Tables are also called *relations*, tuples are also called
*rows*, and attributes are also called *columns*. Our example in the rest of
this session is the product table below.

**Product**

| PName | Price | Manufacturer |
|---|---|---|
| Gizmo | $19.99 | GizmoWorks |
| Powergizmo | $29.99 | GizmoWorks |
| SingleTouch | $149.99 | Canon |
| MultiTouch | $203.99 | Hitachi |

Can we have the same row twice? Yes, because a multiset, unlike a set, can
contain the same element more than once. A SQL table therefore allows
duplicate rows unless a key or a constraint forbids them. This is one of the
points where SQL differs from the pure relational model of the theory.

SQL has atomic types for characters, such as `CHAR(20)` and `VARCHAR(50)`,
for numbers, such as `INT`, `BIGINT`, `SMALLINT` and `FLOAT`, and others such
as `MONEY` and `DATETIME`. Every attribute must have an atomic type, and
consequently tables in SQL are always flat, i.e. cells should in principle
not contain lists or matrices. Compare this with what we learned in the Data
Structures session, where a Python list can contain a list and a dictionary
can contain a dictionary, while a SQL cell cannot contain either of them. If
you want a one-to-many relationship, you do not put a list in a cell.
Instead, you make another table, which is the main idea of the relational
model.

The *schema* of a table is its name, its attributes and their types. In our
example it is the following:

```
Product: (PName: string, Price: float, Manufacturer: string)
```

A *key* is a minimal subset of attributes that acts as a unique identifier
for the tuples of a relation. It is an implicit constraint on which tuples
can be in the relation, i.e. if two tuples in the same table agree on the
values of the key, they must be the same tuple. In the schema the key is
underlined, and in our example it is `PName`. The word minimal is important
in this definition. For example, `(PName, Price)` also identifies rows
uniquely, but it is not a key because a proper subset of it, namely `PName`,
already identifies them.

---

## 10. Data definition and manipulation

The data definition language creates tables. The following statement
initializes an empty table with the specified schema, i.e. its name, its
attributes and its keys:

```sql
CREATE TABLE extable(col1 INTEGER, col2 VARCHAR(50), PRIMARY KEY (col1));
```

The data manipulation language changes the content of tables. An `INSERT`
statement adds a row, for example:

```sql
INSERT INTO phone_book (name, number) VALUES ('John Doe', '555-1212');
```

Before this statement the phone book contained Jane Doe (333-333) and Max
Mustermann (4949-4900), and after it the phone book also contains John Doe
(555-1212). An `UPDATE` statement changes existing rows, for example:

```sql
UPDATE Table1 SET C1 = C1 + 1 WHERE C2 = 'a';
```

| before | | | after | |
|---|---|---|---|---|
| **C1** | **C2** | | **C1** | **C2** |
| 1 | a | | **2** | a |
| 2 | b | | 2 | b |
| 3 | a | | **4** | a |
| 4 | x | | 4 | x |

Read this statement carefully, because `SET C1 = C1 + 1` is an assignment
and not an equation. This is the same distinction as between `←` and `=` in
our pseudocode conventions. The `WHERE` clause restricts the update to the
rows where `C2` is `'a'`, and without it the statement would update every row
of the table. `DELETE FROM example WHERE column2 = 'N';` removes rows and
`DROP TABLE table_name;` removes a whole table. Many things can be dropped,
including indices, columns and whole databases. Finally, `ROLLBACK` discards
all the data changes since the last `COMMIT` or `ROLLBACK`. By default, a set
of manipulations is part of a transaction that is executed and finished when
we call `COMMIT`. Therefore, `ROLLBACK` is how the rewind of an atomic
transaction is done in practice.

---

## 11. Queries: selection, projection, aggregation

SQL *queries* allow us to define what data to receive from a database. The
basic form of a query is the following:

```sql
SELECT <attributes> FROM <one or more relations> WHERE <conditions>
```

*Selection* chooses rows. For example, the query

```sql
SELECT * FROM Product WHERE Manufacturer = 'GizmoWorks'
```

returns the rows of Gizmo and Powergizmo with all their columns. *Projection*
chooses columns, so the query

```sql
SELECT PName, Price FROM Product WHERE Manufacturer = 'GizmoWorks'
```

returns the same two rows but only the `PName` and `Price` columns. It is
easy to confuse the two terms. Selection chooses rows and is done by the
`WHERE` clause, while projection chooses columns and is done by the attribute
list after `SELECT`, despite the name of the keyword. *Aggregation* reduces
the rows to a summary, for example:

```sql
SELECT AVG(Price) FROM Product WHERE Manufacturer = 'GizmoWorks'
```

| AVG(Price) |
|---|
| $24.99 |

After the selection, the whole table is reduced to a single row. Other
aggregate functions are `COUNT`, `SUM`, `MIN` and `MAX`. *Grouping* applies
the aggregate to each group separately, for example:

```sql
SELECT Manufacturer, AVG(Price) FROM Product GROUP BY Manufacturer
```

| Manufacturer | AVG(Price) |
|---|---|
| GizmoWorks | $24.99 |
| Canon | $149.99 |
| Hitachi | $203.99 |

`GROUP BY` splits the table into groups and applies the aggregate to each
one. This is the SQL equivalent of a split-apply-combine operation and one of
the most useful constructs for data analysis. There is more about aggregation
and grouping in the tutorial sessions. The second part of the practical
Python examples compares a `GROUP BY` in the database with fetching all the
rows and aggregating them in Python.

---

## 12. Joins

A *join* resembles a merge or product operation in other languages. We start
with a manual join,

```sql
SELECT * FROM purchase, Product WHERE purchase.Product = Product.Nr;
```

on a version of the `purchase` table in which the last four rows refer to
two products, 3 and 4, that are not in the `Product` table.

**purchase**

| Nr | Date | Name | Product |
|---|---|---|---|
| 1 | 06.03.2020 | 1 | 1 |
| 2 | 06.03.2020 | 2 | 2 |
| 3 | 06.03.2020 | 1 | 2 |
| 4 | 06.03.2020 | 3 | 1 |
| 5 | 07.03.2020 | 4 | 3 |
| 6 | 07.03.2020 | 1 | 3 |
| 7 | 08.03.2020 | 3 | 4 |
| 8 | 08.03.2020 | 2 | 4 |

**Product**

| Nr | Product | Productnr |
|---|---|---|
| 1 | Milk | 00111 |
| 2 | Tea | 00222 |

**Result:**

| Nr | Date | Name | purchase.Product | Product.Product | Productnr |
|---|---|---|---|---|---|
| 1 | 06.03.2020 | 1 | 1 | Milk | 00111 |
| 2 | 06.03.2020 | 2 | 2 | Tea | 00222 |
| 3 | 06.03.2020 | 1 | 2 | Tea | 00222 |
| 4 | 06.03.2020 | 3 | 1 | Milk | 00111 |

We can ask three questions about this result:

- **Why are there only four rows when `purchase` had eight?** Rows 5 to 8 of
  `purchase` refer to products 3 and 4, which do not exist in `Product`. The
  condition `purchase.Product = Product.Nr` is never satisfied for them, so
  they are dropped. This is what an inner join does. Unmatched rows disappear
  without a warning, which is dangerous in real data, so you should always
  check the row count of a join against what you expected.
- **Why are there new column names?** Both tables have a column called
  `Product`, so the result would be ambiguous. SQL therefore qualifies them
  with the table name as `purchase.Product` and `Product.Product`. The same
  happens to `Nr`, which both tables have. A real DBMS returns both
  `purchase.Nr` and `Product.Nr`, and the table above shows only the first
  one to save space.
- **How many rows would we get with `SELECT * FROM purchase, Product;`?** We
  would get sixteen rows, i.e. $8 \times 2$. Without a `WHERE` condition,
  listing two tables in `FROM` produces the Cartesian product, in which every
  row of the first table is paired with every row of the second. A forgotten
  join condition on two large tables can therefore overload a server, because
  for example the product of a million-row table with itself has $10^{12}$
  rows.

References to the keys of other tables are called *foreign keys*, and columns
can be named in a way that simplifies the expected joins. If we rename the
columns so that the key is called `ProductID` in both tables and the primary
key of `purchase` becomes `ID`, the join can be written explicitly:

```sql
SELECT * FROM purchase INNER JOIN Product USING (ProductID);
```

**Result:**

| ID | Date | Name | ProductID | Product | Productnr |
|---|---|---|---|---|---|
| 1 | 06.03.2020 | 1 | 1 | Milk | 00111 |
| 2 | 06.03.2020 | 2 | 2 | Tea | 00222 |
| 3 | 06.03.2020 | 1 | 2 | Tea | 00222 |
| 4 | 06.03.2020 | 3 | 1 | Milk | 00111 |

This is the same result as the manual join, but the shared key appears once
and the intent is explicit. You should prefer the explicit `JOIN` syntax,
because a missing `WHERE` in the manual form produces a Cartesian product
without any warning, whereas a missing `ON` or `USING` in the explicit form
is a syntax error.

There are different kinds of joins, based on set operations:

- An **`INNER JOIN`** keeps only the rows that match in both tables.
- A **`LEFT JOIN`** keeps all the rows of the left table and matches them
  with rows of the right table where possible.
- A **`RIGHT JOIN`** keeps all the rows of the right table and matches them
  with rows of the left table where possible.
- A **`FULL OUTER JOIN`** keeps all the rows of both tables.

If values are missing from one of the columns, they are set to `NULL`. For
example, a `LEFT JOIN` of `purchase` with `Product` would keep all eight
purchases and put `NULL` in the product columns of rows 5 to 8. This makes
the missing products visible instead of dropping them, which is usually what
you want when you are doing data analysis.

---

## 13. SQL injection

A *SQL injection* is a security attack on a database that inputs SQL code as
user input, for example as a user name. If the database permissions are not
well set, the code could be executed. It can be used to delete the database,
for illicit data export, or to gain access to other parts of the system. The
attack works on a program that builds a query by pasting user input into a
string, for example:

```python
query = "SELECT * FROM Students WHERE name = '" + name + "'"
```

If `name` is `Robert'); DROP TABLE Students;--`, the resulting string is no
longer one query but two, and the second one destroys a table. This is the
joke of XKCD 327, *Exploits of a Mom* (<https://xkcd.com/327/>), where a
mother names her son `Robert'); DROP TABLE Students;--` and the school loses
its student records. The solution is to never build queries by string
concatenation. Instead, use parameterized queries, where the values are
passed separately from the query text so that the DBMS does not confuse data
with code:

```python
cursor.execute("SELECT * FROM Students WHERE name = ?", (name,))
```

A SQL injection happens when something that is data is interpreted as
instructions. This is similar to the encoding problems that we learned about
in the Information Coding session, where data was also interpreted in a way
that was not intended.

---

## 14. Summary

Databases are the technology to centralize, manage and provide access to
data. A DBMS is the software that handles the database while we just operate
with it. Relational databases let tables refer to each other, which makes
storage and updates more efficient. SQL is the most used language for
relational databases.

---

## 15. Why does this matter? Practical Python examples

Check the [practical Python examples in this Jupyter notebook](https://github.com/dgarcia-eu/ICSS/blob/main/PythonExamples/Examples10-Databases.ipynb).
There, you will see lookups in a table of half a million users become
hundreds to thousands of times faster with an index, a `GROUP BY` in the
database that returns eight rows instead of moving half a million rows to
Python, and a bank transfer that crashes halfway and is rolled back by a
transaction.

---

## 16. Check yourself

**1.** In the flat purchase table, what exactly goes wrong if the Productnr of Milk changes and you update only some rows?

<details><summary>Answer</summary>

The table then states two contradictory facts, namely that Milk has the
number 00111 and that it has the number 00333. Any query that groups by
Productnr then splits Milk into two products. The database itself cannot
detect this, because nothing in the flat model says that those cells have to
agree. In the relational design this situation cannot happen, because the
number is stored once.

</details>

**2.** Is <code>(PName, Manufacturer)</code> a key of <code>Product</code>?

<details><summary>Answer</summary>

It identifies rows uniquely, but it is not a key because it is not minimal,
i.e. `PName` alone already identifies the rows. A non-minimal set of
attributes that identifies rows uniquely is called a superkey.

</details>

**3.** Why does declarative SQL parallelize better than an equivalent Python loop?

<details><summary>Answer</summary>

A SQL query does not specify an order of operations. For example, a
`SELECT … WHERE` says which rows qualify but it does not say that they must
be examined from first to last, so the DBMS is free to split the table across
cores and merge the results. A Python `for` loop that appends to a list has
committed to a sequential order and also to a shared structure that changes
at every step. We will learn why this is a problem in the Parallel
Programming session.

</details>

**4.** You join two tables and get more rows than either table had. What happened?

<details><summary>Answer</summary>

The join key is not unique in at least one of the tables. Each row on one
side matched several rows on the other side, so the result has one row per
matching pair. This is correct behavior, but it often means that you
misunderstood what one row of your data represents. You can check it with
`SELECT key, COUNT(*) … GROUP BY key HAVING COUNT(*) > 1`.

</details>

**5.** Which ACID property is violated if a crash mid-transfer leaves money deducted but not credited? And which if a reader sees that intermediate state?

<details><summary>Answer</summary>

The first case violates atomicity, because the transaction was not performed
completely or not at all. It also violates durability if the partial state
survives the crash. The second case violates isolation, because a concurrent
reader observed a state that no serial execution would produce.

</details>

---

## 17. References

- **Foster, I., Ghani, R., Jarmin, R. S., Kreuter, F. & Lane, J. (eds.)
  (2017).** *Big Data and Social Science: A Practical Guide to Methods and
  Tools*. Chapman & Hall/CRC. Chapter 4, "Databases", by Ian Foster and Pascal
  Heus, is the reading for this session.
- **Codd, E. F. (1970).** "A Relational Model of Data for Large Shared Data
  Banks". *Communications of the ACM* 13(6), 377–387. The paper that
  introduced the relational model, relations and keys.
- **Garcia-Molina, H., Ullman, J. D. & Widom, J. (2008).** *Database Systems:
  The Complete Book*, 2nd ed. Pearson. The standard reference. The `Product`
  and `purchase` examples follow its style.
- **Elmasri, R. & Navathe, S. B. (2016).** *Fundamentals of Database Systems*,
  7th ed. Pearson. Normal forms and update anomalies.
- **Härder, T. & Reuter, A. (1983).** "Principles of Transaction-Oriented
  Database Recovery". *ACM Computing Surveys* 15(4), 287–317. The origin of
  the ACID acronym.
- **W3Schools SQL tutorial:** <https://www.w3schools.com/sql/default.asp>. The
  practical reference for the SQL statements, queries and joins of this
  session, including the join diagrams.
- **Munroe, R.** *Exploits of a Mom*, XKCD 327: <https://xkcd.com/327/>.
  The SQL injection example.
- **OWASP, *SQL Injection*:**
  <https://owasp.org/www-community/attacks/SQL_Injection>. The attack and its
  prevention.
- **SQLite documentation:** <https://www.sqlite.org/>. The DBMS used in the
  tutorial sessions.
