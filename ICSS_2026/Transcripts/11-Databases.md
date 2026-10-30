# Session 11: Databases

*Introduction to Computing for the Social Sciences · lecture transcript*

> Companion text for lecture 11. Notation follows
> [the course conventions](00-Conventions.md).
>
> **Reading for this session:** chapter 4, "Databases", of Foster, Ghani,
> Jarmin, Kreuter & Lane (eds.), *Big Data and Social Science* (2017). For SQL
> practice, the W3Schools tutorial: <https://www.w3schools.com/sql/default.asp>.
> Full references at the end.

---

## Contents

<!-- MOTIVATION-TOC:BEGIN -->
0. [Motivating examples](#motivating-examples)
<!-- MOTIVATION-TOC:END -->
1. [Why databases exist: two examples](#1-why-databases-exist-two-examples)
2. [Databases and DBMS](#2-databases-and-dbms)
3. [What a DBMS does](#3-what-a-dbms-does)
4. [Why use a database?](#4-why-use-a-database)
5. [Transactions and ACID](#5-transactions-and-acid)
6. [Database models: flat and relational](#6-database-models-flat-and-relational)
7. [Keys and normal forms](#7-keys-and-normal-forms)
8. [SQL: what kind of language it is](#8-sql-what-kind-of-language-it-is)
9. [Tables, types, schemas and keys in SQL](#9-tables-types-schemas-and-keys-in-sql)
10. [Data definition and manipulation](#10-data-definition-and-manipulation)
11. [Queries: selection, projection, aggregation](#11-queries-selection-projection-aggregation)
12. [Joins](#12-joins)
13. [SQL injection](#13-sql-injection)
14. [Summary](#14-summary)
15. [Check yourself](#15-check-yourself)
16. [References](#16-references)

---

<!-- MOTIVATION-SECTION:BEGIN -->
## Motivating examples

Three candidate openings for this session, each a real situation the
material is the answer to. **One of these will be used in the lecture**;
the others are kept here because they are worth reading anyway.

<!-- MOTIVATION:M11-A:BEGIN -->
### A · The 15 841 cases that fell off the end of a spreadsheet

Between 25 September and 2 October 2020, at the height of the second wave,
the English contact-tracing system lost 15 841 positive COVID-19 test
results. The people who tested positive were told their result, but their
contacts were not traced, an estimated 50 000 people who had been exposed and
were never contacted. The cause was a file format. Laboratories submitted
results as CSV files, and the process that collated them loaded these into
`.xls`, the pre-2007 Excel format, whose worksheets hold a maximum of 65 536
rows. When the file of a lab exceeded that, the rows beyond the limit were
silently discarded. Nothing was logged, nothing failed, and the collation
completed successfully every day.

It is easy to file this under "someone used the wrong tool", and the tabloid
version did. The more useful reading is to ask what a proper database would
have given, item by item, because each item is a topic of this session. Scale
is not the point; silence is. Any storage system has limits, and what matters
is whether exceeding one produces an error or a wrong answer; a database
rejects an insert it cannot perform and tells you, and it does not quietly
keep the first 65 536 rows. Constraints are enforced by the store and not by
the user: a schema declaring that a test result must have a patient
identifier, a date and a valid result code makes malformed data impossible to
insert, while in a spreadsheet the rules live in the head of whoever is doing
the work. Transactions are all or nothing: a load that fails halfway leaves
the database as it was, not partially updated with no record of which part,
and that is atomicity, one of the ACID properties. Concurrency is handled:
multiple labs writing at once is the normal case for a database and a recipe
for lost updates with files on a shared drive. And there is one copy, so the
question of how many positives there were on 28 September has exactly one
answer, rather than one per person who has a copy of the file. None of this
is exotic. It is what a database is, and the reason why the answer to "why
not just use a spreadsheet?" is not snobbery but a list of specific
guarantees you lose.

Section 2 of this session says what a database and a DBMS actually are, and
why the distinction matters. Section 4 gives the reasons to use one, data
independence, standardization and concurrency, and the standardization point
is exactly the CSV-to-`.xls` failure. Section 5 is about transactions and
ACID, which is the formal version of the requirement that it should not be
possible to half-load a file. Sections 6 and 7 present the relational model,
keys and normal forms, that is, how the store itself enforces that a fact is
recorded once and correctly. The question to ask of any research data setup
is whether anyone would find out if it silently lost 5% of the records. If the
answer is no, the format is the problem.
<!-- MOTIVATION:M11-A:END -->
<!-- MOTIVATION:M11-B:BEGIN -->
### B · Two seats, one airplane

One seat left. Two agents, in two cities, click "book" in the same second,
and each program does the obvious and correct thing:

```
free ← read the number of free seats          # both agents read 1
If free > 0
      then write free - 1 as the number of free seats
           issue the ticket
```

Trace the interleaving. Agent A reads 1. Before A writes, agent B also reads
1. Both see a free seat, both write 0, both issue a ticket. The seat has been
sold twice, and the seat count says 0, which is consistent with either one
sale or a hundred. Read the code of either program in isolation and it is
flawless. The defect does not exist in either one; it exists in the
interleaving, and interleavings are not visible in the source of any single
program. This is a race condition, and it is the reason why concurrent
systems are hard in a way that sequential ones are not. It is also not a rare
corner case. It is the normal condition for anything with more than one user,
such as booking systems, ticketing, inventory, appointment slots or vaccine
doses, and any pattern of the form "read a value, decide, write it back" has
this shape.

The database answer is the transaction, a group of operations that must
happen completely or not at all, and that must behave as though nothing else
ran at the same time. The four guarantees go by the acronym ACID. Atomicity
means all of it or none of it, so a booking that fails partway leaves no
trace. Consistency means that a transaction that succeeds leaves the database
valid, so a constraint like "seats sold ≤ capacity" cannot be violated.
Isolation means that the outcome of running transactions concurrently must
equal the outcome of running them one after another in some order, and this
is the property that rules out the interleaving above. Durability means that
once a transaction is confirmed, it survives a crash, a power cut, or the
server catching fire. Isolation is the deep one and worth stating carefully:
it does not say that transactions run one at a time, which would be unusably
slow. It says that the result must be indistinguishable from some serial
order, and the database is free to interleave as aggressively as it likes,
provided that nobody can tell.

Section 5 of this session covers transactions and ACID in full, with this
scenario as the worked case. Section 4 presents concurrency as one of the
three reasons why databases exist, alongside data independence and
standardization. Section 1 introduces the flight-reservation and
vaccine-distribution examples that run through the lecture, both of which
are this problem at scale. The connection forward is that session 12 meets
the same problem in the hardware, two threads incrementing a shared counter,
and reaches for the same solution: any time two things share mutable state,
"check, then act" is unsafe unless something guarantees that it is one step.
<!-- MOTIVATION:M11-B:END -->
<!-- MOTIVATION:M11-C:BEGIN -->
### C · Whose number is right?

This one has no dramatic outcome and no news coverage, which is why it is
worth including: it is what actually happens in research groups. A project
keeps a participant list. It starts as one file. Someone needs it for an
analysis and copies it. Someone else needs a version with the new wave merged
in. A third person keeps the master but is on leave when a participant
withdraws, so the withdrawal is applied to somebody else's copy. Three months
on there are three files. One has the corrected spelling of a name, one has
the new wave, one has the withdrawal, and none has all three. The counts
differ by 47, nobody knows which file is authoritative, and the only way to
find out is to reconcile three files by hand, assuming that the changes are
even recoverable, which they usually are not, because none of them was
recorded as a change. Nobody was careless. Each person did a correct and
necessary thing to the copy in front of them. The failure is architectural:
the same fact was stored in more than one place, so it became possible for
the copies to disagree, and once that is possible it is only a matter of
time.

The answer of the relational model is a design principle, and it is the
through-line of this session: every fact should be stored in exactly one
place. That is what a primary key enforces within a table, one row per
participant, identified by an identifier that never changes even if the name
does. It is what a foreign key enforces between tables, since other tables
refer to that participant rather than repeating their details. And it is what
normalization is for, the systematic removal of the repetition that makes
disagreement possible. The failure modes have names, and the session works
through them. An update anomaly changes a value in one place and not in
another, so that the data contradicts itself, which is exactly the story
above. An insertion anomaly means that you cannot record a fact because there
is nowhere to put it without inventing unrelated data. A deletion anomaly
means that removing one record silently destroys unrelated information that
happened to live in the same row. A shared database does not make people more
careful. It makes the careless outcome structurally impossible: there is one
row for each participant, one place to change the name, and a record of who
changed it and when.

Sections 6 and 7 of this session present the flat versus the relational
model, keys, foreign keys and normal forms, with a worked example of exactly
the repetition above. Section 4 is about data independence and why a single
store beats a folder of files. Section 5 is about transactions, which is the
same argument for simultaneous edits rather than sequential ones. The
question to ask of your own project is how many files you have to edit if a
value changes. If the answer is more than one, you have already built the
failure above; it just has not surfaced yet.
<!-- MOTIVATION:M11-C:END -->
---

<!-- MOTIVATION-SECTION:END -->
## 1. Why databases exist: two examples

The lecture opens with two examples. A flight reservation system has to know,
at every instant, which seats on which flights are free, and it has to answer
that question for thousands of agents at once; two people must not be sold
the same seat, and a booking that fails halfway, with the seat taken but the
payment not charged, must leave no trace. A vaccine distribution system
receives doses at a warehouse, ships them to vaccination centers,
administers them to named people on given dates, and schedules second doses;
the same person appears in several places, the same batch appears in several
places, and everything has to stay consistent as the information flows
through the system. Both examples share the same three problems: many users
at the same time, data that refers to other data, and operations that must
not be left half done. Those three problems are what the rest of this lecture
is about.

---

## 2. Databases and DBMS

Informally, a database is an organized collection of data. An Excel table is
a very simple database, and what makes a collection of data a database is that
it enables fast access and the ability to access the data in a structured
way. A *database management system* (DBMS) is a software application that
enables the interaction between the user and the actual database. It
implements the definition, creation, querying, updating and administration
of a database, the data may be distributed at different locations, and
examples are MySQL, PostgreSQL, Access and Oracle; SQLite, a whole DBMS in a
single file, is the one you will probably use first. Formally, a *database*
(DB) is a set of related data together with the formal organization and
interdependence of these data, and access to and manipulation of the data are
provided through a corresponding DBMS. The distinction matters: the database
is the data plus its organization, and the DBMS is the program that stands
between you and it. When people say "we use Postgres" they are naming the
DBMS, not the database. The familiar cylinder icon of a database, by the way,
is a stylized hard-drive platter, a fossil of the era when a database was
physically a stack of spinning disks.

---

## 3. What a DBMS does

A database management system has four characteristics. *Data definition* is
the creation, modification and deletion of the definitions that define the
organization of the data, that is, the relationships among the entries in
the database. *Updating* is the insertion, modification and deletion of the
actual content, that is, of the individual data entries. *Retrieval* or
*querying* returns information, given specific query inputs, that can be used
by any downstream application. And *administration* covers user management,
data security, performance, data integrity, concurrency, and the protection
against database corruption and system failure. Take the small table used
throughout the lecture:

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
types. Updating is adding Pat's row. Querying is asking for the rows with
`Product = Tea and Birth < 1999`, which returns the tea rows of Hans and Pat
but not the one of Fred, who was born in 1999. Administration is everything
that makes the table survive a power cut and three hundred simultaneous
users.

---

## 4. Why use a database?

There are three reasons to use a database, and each of them solves a problem
you have already met in this course. The first is *data independence*:
applications and users do not need to worry about how the data are
structured and stored. Logical data independence protects them from changes
to the logical structure of the data, so that a new entity or attribute can
be added without affecting existing usage, and physical data independence
protects them from changes of the physical layout, so that the user does not
have to care about information coding, disk space and the like. The second
connects directly to session 2: whether a date is stored as a 32-bit integer
or as a string is exactly the sort of thing you do not want in your analysis
script. The second reason is *standardization*: data formats and methods of
accessing data are platform independent. Recall the problems of parsing a
CSV file with conflict events in Python, where every reader has to guess the
encoding, the separator, the quoting convention and what a missing value
looks like, because a CSV file has no schema. A database has one, and it can
serve flexible output schemas to different users and purposes from the same
stored data. The third reason is *concurrency*: a database allows the
simultaneous usage by many users without the problem of conflicting
updates, using robust protocols that avoid database corruption. This is the
flight booking problem, and it is the subject of the next section and, at
the hardware level, of session 12.

---

## 5. Transactions and ACID

A *transaction* is a series of data manipulations that must not be
interrupted: all the operations in a transaction have to be fully performed
or completely rewound. Database transactions have four properties,
remembered by the acronym ACID. *Atomicity* means that each transaction
stands on its own and that a rewind is possible. *Consistency* ensures that
any transaction that succeeds maintains the validity of the database.
*Isolation* ensures that it does not matter whether we execute our
transactions serially or concurrently. And *durability* requires that any
transaction that has completed survives permanently, also on error, crash or
loss of power. The classic illustration is a bank transfer that subtracts
100 from account A and adds 100 to account B. Atomicity says that the pair
happens completely or not at all, so there is no state of the world in which
the money has left A and not arrived at B. Isolation says that if someone
reads both balances while the transfer runs, they see either the state
before or the state after, never the middle. Durability says that once the
DBMS reports success, pulling the plug does not undo it. Isolation is the
deep one, and it is worth stating in the vocabulary of session 12:
concurrent execution is only acceptable if its result is indistinguishable
from some serial execution.

---

## 6. Database models: flat and relational

*Database models* fundamentally define the structure of a database. They set
its logical structure in terms of data storage, organization and
manipulation, and they are ultimately about how the relationship between
related pieces of information is represented. The *flat model*, also known as
the spreadsheet, is a single two-dimensional array of data elements in which
the members of a row are related, forming an entry, and the members of a
column describe the same property or characteristic. The *relational model*
represents the data through sets of linked tables that share a common key;
the intuition is that of many spreadsheets, each storing a specific piece of
information, linked through a unique key. The lecture shows what is wrong
with the flat model on the purchase table:

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

Data is repeated across the table. That is an inefficient use of space, since
the birth year of Hans is stored three times, and it creates problems when
updating: if the Productnr of Milk is now 00333, you must find and change
every row where the product is Milk, and if you miss one, the table contains
two contradictory facts. That second failure mode is called an *update
anomaly* in the literature, and it is the reason why the relational model
exists. The same data can be stored in three linked tables:

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

Now the Productnr of Milk lives in exactly one cell. Changing it is one
update, and it cannot be done inconsistently.

---

## 7. Keys and normal forms

The *primary key* is the `Nr` column of each table, a value that uniquely
identifies a row. *Foreign keys* reference primary keys, on another table or
on the same table: in `purchase`, the columns `Name` and `Product` are
foreign keys that hold `Nr` values of `Names` and `Product`. A foreign key is
a promise that the DBMS can enforce, because you cannot insert a purchase
that refers to product 7 if there is no product 7. That is *referential
integrity*, and it is one of the things you lose when you keep your data in
spreadsheets. Relational database designs can be standardized using *normal
forms*. In the example above, `Class` is still stored as a string inside
`Names`, and it should be its own table:

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
table, let alone the `purchase` table: renaming class T1 to "Tuesday-1" is a
single-cell edit. The general recipe behind normalization is that every
fact should be stored in exactly one place. When you find yourself repeating
a value, that value probably wants its own table with its own key.

---

## 8. SQL: what kind of language it is

SQL is a special-purpose language specifically developed for managing data
through relational database systems. It consists of three co-dependent
language definitions. The *data definition language* (DDL) defines relational
schemata and creates, alters and deletes tables and their attributes. The
*data manipulation language* (DML) inserts, deletes and modifies the entries
of tables and queries one or more tables. The *data control language* (DCL)
controls the access to the data stored in the database and grants, revokes
and modifies user access rights. SQL is a very high-level programming
language. Its performance is good because the actual operations are well
optimized, there are many different standards but typical DBMSs support
all of them, and its execution is highly parallelizable by construction. SQL
is also a *declarative* language: you define what you want, and the DBMS
takes care of how to do it. You can also write procedural SQL with special
instructions, but it is very inefficient.

This is the sharpest contrast with everything else in the course. In session
4 you wrote how: loop over this, test that, append to the other. In SQL you
state the property that the answer has, and the query planner of the DBMS
chooses the algorithm, that is, which index to use, which join order, and
whether to sort or to hash. That is also why SQL parallelizes so well, as we
will see in session 12: you never committed to an order of operations, so the
system is free to choose one. The flow is always the same: the query goes as
SQL to the DBMS, the DBMS works on the database, and the result comes back.

---

## 9. Tables, types, schemas and keys in SQL

A *table* is a multiset of tuples coding the attributes specified by the
database schema. Tables are also called *relations*, tuples are also called
*rows*, and attributes are also called *columns*. The running example of the
lecture is a product table:

**Product**

| PName | Price | Manufacturer |
|---|---|---|
| Gizmo | $19.99 | GizmoWorks |
| Powergizmo | $29.99 | GizmoWorks |
| SingleTouch | $149.99 | Canon |
| MultiTouch | $203.99 | Hitachi |

Can we have the same row twice? Yes, and the word "multiset" is doing real
work in the definition: a SQL table is a bag, not a set, so duplicate rows
are allowed unless a key or a constraint forbids them. This is one of the
places where SQL departs from the pure relational model of the theory.
Regarding types, SQL has atomic types for characters, such as `CHAR(20)` and
`VARCHAR(50)`, for numbers, such as `INT`, `BIGINT`, `SMALLINT` and `FLOAT`,
and others such as `MONEY` and `DATETIME`. Every attribute must have an atomic
type, and consequently tables in SQL are always flat: cells, in principle,
should not contain lists or matrices. Compare with session 3: a Python list
can contain a list and a dictionary can contain a dictionary, but a SQL cell
cannot. If you want a one-to-many relationship, you do not put a list in a
cell; you make another table. That is the relational model in one sentence.

The *schema* of a table is its name, its attributes and their types. In our
example it is

```
Product: (PName: string, Price: float, Manufacturer: string)
```

A *key* is a minimal subset of attributes that acts as a unique identifier
for the tuples of a relation. It is an implicit constraint on which tuples
can be in the relation: if two tuples in the same table agree on the values
of the key, they must be the same tuple. In the schema the key is underlined,
and in our example it is `PName`. Note the word minimal: `(PName, Price)`
also identifies rows uniquely, but it is not a key, because a proper subset
of it already does.

---

## 10. Data definition and manipulation

The data definition language creates tables. The statement

```sql
CREATE TABLE extable(col1 INTEGER, col2 VARCHAR(50), PRIMARY KEY (col1));
```

initializes an empty table with the specified schema: its name, its
attributes and its keys. The data manipulation language changes their
content. An `INSERT` adds a row,

```sql
INSERT INTO phone_book (name, number) VALUES ('John Doe', '555-1212');
```

so that the phone book with Jane Doe (333-333) and Max Mustermann
(4949-4900) also contains John Doe (555-1212) afterwards. An `UPDATE` changes
existing rows:

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

Read it carefully: `SET C1 = C1 + 1` is an assignment and not an equation,
the same distinction as between `←` and `=` in our pseudocode conventions,
and the `WHERE` clause is the only thing standing between you and updating
every row of the table. `DELETE FROM example WHERE column2 = 'N';` removes
rows, and `DROP TABLE table_name;` removes a whole table; many things can be
dropped, including indices, columns and whole databases. Finally,
`ROLLBACK` discards all the data changes since the last `COMMIT` or
`ROLLBACK`. By default, a set of manipulations is part of a transaction that
is executed and finished when we call `COMMIT`, so `ROLLBACK` is the
atomicity of section 5 made operational: it is the rewind.

---

## 11. Queries: selection, projection, aggregation

SQL *queries* allow us to define what data to receive from a database. The
basic form of a query is

```sql
SELECT <attributes> FROM <one or more relations> WHERE <conditions>
```

*Selection* chooses rows. The query

```sql
SELECT * FROM Product WHERE Manufacturer = 'GizmoWorks'
```

returns the rows of Gizmo and Powergizmo with all their columns. *Projection*
chooses columns, so

```sql
SELECT PName, Price FROM Product WHERE Manufacturer = 'GizmoWorks'
```

returns the same two rows but only the `PName` and `Price` columns. The two
words are worth keeping straight: selection cuts horizontally, choosing rows,
and projection cuts vertically, choosing columns. `WHERE` does the selection
and the attribute list after `SELECT` does the projection, despite the name
of the keyword. *Aggregation* collapses the rows into a summary:

```sql
SELECT AVG(Price) FROM Product WHERE Manufacturer = 'GizmoWorks'
```

| AVG(Price) |
|---|
| $24.99 |

The whole table, after selection, collapses to a single row; other aggregate
functions are `COUNT`, `SUM`, `MIN` and `MAX`. *Grouping* applies the
aggregate to each group separately:

```sql
SELECT Manufacturer, AVG(Price) FROM Product GROUP BY Manufacturer
```

| Manufacturer | AVG(Price) |
|---|---|
| GizmoWorks | $24.99 |
| Canon | $149.99 |
| Hitachi | $203.99 |

`GROUP BY` splits the table into groups and applies the aggregate to each
one, which is the SQL equivalent of a split-apply-combine operation and the
single most useful construct for data analysis. There is more about
aggregation and grouping in the tutorial sessions.

---

## 12. Joins

A *join* resembles a merge or product operation in other languages. The
lecture first shows a manual join,

```sql
SELECT * FROM purchase, Product WHERE purchase.Product = Product.Nr;
```

on a version of the `purchase` table in which the last four rows refer to
two products, 3 and 4, that are not in the `Product` table:

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

The lecture asks three questions about this result. Why are there only four
rows when `purchase` had eight? Because rows 5 to 8 of `purchase` refer to
products 3 and 4, which do not exist in `Product`, so the condition
`purchase.Product = Product.Nr` is never satisfied for them and they are
dropped. This is exactly what an inner join does: unmatched rows disappear
silently, and in real data that silence is dangerous, so always check the row
count of a join against what you expected. Why are there new column names?
Because both tables have a column called `Product`, so the result would be
ambiguous, and SQL qualifies them with the table name as `purchase.Product`
and `Product.Product`. The same happens to `Nr`, which both tables have; a
real DBMS returns both `purchase.Nr` and `Product.Nr`, and the slide shows
only the first for space. And how many rows would we get with `SELECT * FROM
purchase, Product;`? Sixteen, that is, $8 \times 2$: without a `WHERE`
condition, listing two tables in `FROM` produces the Cartesian product, every
row of the first paired with every row of the second, which is why a
forgotten join condition on two large tables is a classic way to bring a
server down, since the product of a million-row table with itself has
$10^{12}$ rows.

References to the keys of other tables are called *foreign keys*, and naming
can be done in a smart way to simplify the expected joins. If we rename the
columns so that the key is called `ProductID` in both tables, and the primary
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
and the intent is explicit. Prefer the explicit `JOIN` syntax: a missing
`WHERE` in the manual form is a silent Cartesian product, whereas a missing
`ON` or `USING` in the explicit form is a syntax error. There are different
kinds of joins, based on set operations. An `INNER JOIN` keeps only the rows
that match in both tables, a `LEFT JOIN` keeps all the rows of the left table
and matches them where possible, a `RIGHT JOIN` keeps all the rows of the
right table, and a `FULL OUTER JOIN` keeps all the rows of both. If values
are missing from one of the columns, they are set to `NULL`. That last
sentence is the practical difference: a `LEFT JOIN` of `purchase` with
`Product` would keep all eight purchases and put `NULL` in the product
columns of rows 5 to 8, which makes the missing products visible instead of
silently dropping them, and when you are doing data analysis that is usually
what you want.

---

## 13. SQL injection

A *SQL injection* is a security attack on a database that inputs SQL code as
user input, for example as a user name. If the database permissions are not
well set, the code could be executed, and it can be used to delete the
database, for illicit data export, or to gain access to other parts of the
system. The mechanism is a program that builds a query by pasting user input
into a string:

```python
query = "SELECT * FROM Students WHERE name = '" + name + "'"
```

If `name` is `Robert'); DROP TABLE Students;--`, the resulting string is no
longer one query but two, and the second one destroys a table. This is the
joke of XKCD 327, *Exploits of a Mom* (<https://xkcd.com/327/>), where a
mother names her son "Robert'); DROP TABLE Students;--" and the school loses
its student records. The fix is never to build queries by string
concatenation, but to use parameterized queries, where the values are passed
separately from the query text and the DBMS never confuses data with code:

```python
cursor.execute("SELECT * FROM Students WHERE name = ?", (name,))
```

This is the same class of bug as the encoding confusions of session 2: something
that is data gets interpreted as instructions. The pattern is worth recognizing, because it recurs everywhere
in computing.

---

## 14. Summary

Databases are the technology to centralize, manage and provide access to
data, and a DBMS is the software that handles the database while we just
operate with it. Relational databases let tables refer to each other, which
gives more efficient storage and updates. And SQL is the most used language
for relational databases.

---

## 15. Check yourself

**1.** In the flat table of section 6, what exactly goes wrong if Milk's Productnr changes and you update only some rows?

<details><summary>Answer</summary>

The table then asserts two contradictory facts, that Milk has the number
00111 and that it has the number 00333, and any query grouping by Productnr
splits Milk into two products. Note that the database itself cannot detect
this, because nothing in the flat model says that those cells have to agree.
In the relational design the situation cannot arise, because the number is
stored once.

</details>

**2.** Is <code>(PName, Manufacturer)</code> a key of <code>Product</code>?

<details><summary>Answer</summary>

It identifies rows uniquely, but it is not a key, because it is not minimal:
`PName` alone already does. A non-minimal set of attributes with the
uniqueness property is called a superkey.

</details>

**3.** Why does declarative SQL parallelize better than an equivalent Python loop?

<details><summary>Answer</summary>

Because the query does not specify an order of operations. A `SELECT … WHERE`
says which rows qualify, not that they must be examined from first to last,
so the DBMS is free to split the table across cores and merge the results. A
Python `for` loop that appends to a list has committed to a sequential order
and, worse, to a shared mutable structure, as we will see in session 12.

</details>

**4.** You join two tables and get more rows than either table had. What happened?

<details><summary>Answer</summary>

The join key is not unique in at least one table. Each row on one side
matched several on the other, so the result has one row per matching pair.
This is correct behavior, but it is almost always a sign that you
misunderstood the grain of your data; check with `SELECT key, COUNT(*) …
GROUP BY key HAVING COUNT(*) > 1`.

</details>

**5.** Which ACID property is violated if a crash mid-transfer leaves money deducted but not credited? And which if a reader sees that intermediate state?

<details><summary>Answer</summary>

The first is atomicity, because the transaction was not all-or-nothing, and
also durability if the partial state survives the crash. The second is
isolation: a concurrent reader observed a state that no serial execution
would ever produce.

</details>

---

## 16. References

- **Foster, I., Ghani, R., Jarmin, R. S., Kreuter, F. & Lane, J. (eds.)
  (2017).** *Big Data and Social Science: A Practical Guide to Methods and
  Tools*. Chapman & Hall/CRC. Chapter 4, "Databases", by Ian Foster and Pascal
  Heus, is the reading for this session.
- **Codd, E. F. (1970).** "A Relational Model of Data for Large Shared Data
  Banks". *Communications of the ACM* 13(6), 377–387. The paper that
  introduced the relational model, relations and keys, and the reasoning of
  sections 6 and 7.
- **Garcia-Molina, H., Ullman, J. D. & Widom, J. (2008).** *Database Systems:
  The Complete Book*, 2nd ed. Pearson. The standard reference; the `Product`
  and `purchase` examples follow its style.
- **Elmasri, R. & Navathe, S. B. (2016).** *Fundamentals of Database Systems*,
  7th ed. Pearson. Normal forms and update anomalies (section 7).
- **Härder, T. & Reuter, A. (1983).** "Principles of Transaction-Oriented
  Database Recovery". *ACM Computing Surveys* 15(4), 287–317. The origin of
  the ACID acronym (section 5).
- **W3Schools SQL tutorial:** <https://www.w3schools.com/sql/default.asp>. The
  practical reference for all the SQL of sections 10 to 12, including the
  join diagrams.
- **Munroe, R.** *Exploits of a Mom*, XKCD 327: <https://xkcd.com/327/>.
  Section 13.
- **OWASP, *SQL Injection*:**
  <https://owasp.org/www-community/attacks/SQL_Injection>. The attack and its
  prevention.
- **SQLite documentation:** <https://www.sqlite.org/>. The DBMS used in the
  tutorial sessions.
