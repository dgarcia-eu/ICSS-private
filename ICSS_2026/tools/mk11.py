OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/11-Databases/ICSS-2026-11-Databases.qmd"
s = ['''---
title: "<span class='course'>Introduction to Computing for the Social Sciences</span><br><span class='session'>Session 11 &ndash; Databases</span>"
author: "David Garcia<br><span class='semester'>Winter Semester 2026-2027</span>"
format:
  revealjs:
    theme: [default, ../theme/unikn.scss]
    width: 1280
    height: 720
    margin: 0.06
    center: false
    slide-number: c
    show-slide-number: all
    progress: true
    controls: true
    history: true
    logo: ../theme/unikn-logo.png
    footer: "<span class='fbar-left'>Session 11</span><span class='fbar-mid'>Introduction to Computing for the Social Sciences</span><span class='fbar-right'>Winter Semester 2026-2027</span>"
    highlight-style: github
    link-external-newwindow: true
    fig-align: left
---

## Course Outline

:::: {.columns}
::: {.column width="50%"}
::: {.sm}
- Session 1: Introduction
- Session 2: Information Coding
- Session 3: Data Structures
- Session 4: Software
- Session 5: Algorithms
- Session 6: Recursion
- Session 7: Sorting Algorithms
:::
:::

::: {.column width="50%"}
::: {.sm}
- Session 8: Time Complexity
- Session 9: Theoretical Computer Science
- Session 10: Machine Learning
- Session 11: Databases
  - Tutorial: Databases (swap)
  - Exercise: DB + projects Q&A
- Session 12: Parallel Programming
- Session 13: Social Science Applications
- Session 14: Exam Review
:::
:::
::::
''']

def sl(t, b): s.append(f"\n## {t}\n\n{b}\n")

ITEMS = ["Databases", "Relational Databases", "Structured Query Language (SQL)"]
def outline(cur=None, extra=False):
    items = ITEMS + (["NoSQL databases"] if extra else [])
    m = [f"[{t}]{{.current}}" if i+1 == cur else t for i, t in enumerate(items)]
    cls = "{.outline .focus}" if cur else "{.outline}"
    return "::: " + cls + "\n" + "\n".join(f"- {t}" for t in m) + "\n:::"

sl("Overview", outline())
sl("Overview", outline(extra=True) + """

:::: {.columns}
::: {.column width="70%"}
:::

::: {.column width="30%"}
::: {.center-h .sm}
Recommended: Chapter 4
:::

![](figures/book-big-data-social-science.jpg){height="7.4em"}
:::
::::""")

sl("Database example: Flight reservations", """::: {.center-h}
![](figures/example-5.png){height="12.4em"}
:::""")

for n in (6, 7, 8, 9, 10):
    sl("Database example: Vaccine distribution", f"""::: {{.center-h}}
![](figures/example-{n}.png){{height="11.6em"}}
:::""")

sl("Databases", """::: {.sm}
- **What is a database?**
  - Informal definition: an organized collection of data
    - an Excel table is a (very simple) database
    - enables fast access and the ability to access data in a structured way
- **What is a database management system (DBMS)?**
  - software application that enables interaction between the user and the actual database
  - implements defining, creating, querying, updating and administering a database
  - data may be distributed at different locations
  - examples: MySQL, PostgreSQL, Access, Oracle
:::""")

sl("Databases and DBMS", """::: {.definition}
[Definition: Database]{.label}

::: {.sm}
A **database (DB)** is a set of related data and the formal organization and interdependence of these data. Access and manipulation of data are provided through a corresponding **database management system (DBMS)**.
:::
:::

:::: {.columns}
::: {.column width="46%"}
![](figures/icon-database.png){height="5.0em"}
:::

::: {.column width="54%"}
![](figures/hard-drive-platter.png){height="5.0em"}
:::
::::

::: {.center-h .xs}
A frequent icon to symbolize a database, represented by a hard drive disk platter
:::""")

# Characteristics of DBMS, four build-up states
ROWS_EMPTY = [["…"] * 5 for _ in range(8)]
ROWS_FULL = [["Hans","1998","T1","Milk","00111"],
             ["Fred","1999","T1","Tea","00222"],
             ["Hans","1998","T1","Tea","00222"],
             ["Anna","2000","W1","Milk","00111"],
             ["Pat","1998","W1","Tea","00222"],
             ["Hans","1998","T1","Milk","00111"],
             ["Anna","2000","W1","Milk","00111"],
             ["Fred","1999","T1","Milk","00111"]]

def table(rows):
    head = "| Name | Birth | Class | Product | Num |\n|---|---|---|---|---|"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows)
    return "::: {.tbl-grid .xxs}\n" + head + "\n" + body + "\n:::"

CHARS = [
    "**data definition:** create, modify, delete the definitions defining the organization of data, i.e., the relationship among entries in the database",
    "**updating:** insert, modify and delete the actual content, i.e., individual data entries in the database",
    "**retrieval or querying:** return information, given specific query inputs, that can be used by any downstream application",
    "**administration:** user management, data security, performance, data integrity, concurrency, protection against database corruption and system failure",
]
EXTRAS = ["", "", "\n\n::: {.tag .xs}\nProduct = Tea and Birth < 1999 ?\n:::", ""]
for k in range(4):
    rows = ROWS_EMPTY if k == 0 else ROWS_FULL
    bullets = "\n".join(f"- {c}" for c in CHARS[:k+1])
    sl("Characteristics of DBMS", f""":::: {{.columns}}
::: {{.column width="40%"}}
{table(rows)}{EXTRAS[k]}
:::

::: {{.column width="60%"}}
::: {{.center-h .sm}}
**Characteristics of database management systems**
:::

::: {{.xs}}
{bullets}
:::
:::
::::""")

sl("Why to use a database?", """::: {.sm}
- **data independence:** applications (and users) do not need to worry about how data are structured and stored
  - *logical data independence:* protection from changes to the logical structure of the data, e.g. add a new entity or attribute without affecting usage
  - *physical data independence:* protection from physical layout changes, e.g. the user does not have to care about information coding, disk space, etc.
- **standardization**
  - data formats, methods of accessing data, etc. are platform independent
    - recall: problems parsing a `.csv` file with conflict events in Python
  - flexible output schemas serving different users and purposes
- **concurrency**
  - allows simultaneous usage by many users without the problem of conflicting updates
  - robust protocols that avoid database corruption
:::""")

sl("Database Transactions: ACID properties", """::: {.sm}
A **transaction** is a series of data manipulations that must not be interrupted. All operations in a transaction have to be fully performed or completely rewound.

Database transactions have the following properties:

- **A**tomicity
  - each transaction stands on its own; a rewind is possible
- **C**onsistency
  - ensures that any transaction that succeeds maintains the validity of the database
- **I**solation
  - ensures that it does not matter whether we execute our transactions serially or concurrently
- **D**urability
  - requires that any transaction that has completed will survive permanently (also on error, crash, loss of power)
:::""")

sl("Relational Databases", outline(2))

sl("Database Models", """::: {.sm}
**Database models** fundamentally define database structure

- set the logical structure of the database in terms of data storage, organization and manipulation
- ultimately about how the relationship between related information is represented
- examples:
  - **flat model**, a.k.a. spreadsheets:
    - a single, two-dimensional array of data elements
    - members of a row are related, i.e. an "entry"
    - members of a column describe the same property or characteristic
  - **relational model**:
    - representation through sets of linked tables that share a common key
    - intuition: many spreadsheets storing specific pieces of information, linked via a unique key
:::""")

FLAT = [["Hans","1998","T1","Milk","00111","06.03.2020"],
        ["Fred","1999","T1","Tea","00222","06.03.2020"],
        ["Hans","1998","T1","Tea","00222","06.03.2020"],
        ["Anna","2000","W1","Milk","00111","06.03.2020"],
        ["Verena","1998","W1","Tea","00222","07.03.2020"],
        ["Hans","1998","T1","Milk","00111","07.03.2020"],
        ["Anna","2000","W1","Milk","00111","08.03.2020"],
        ["Fred","1999","T1","Milk","00111","08.03.2020"]]
flat_tbl = ("::: {.tbl-grid .xs}\n| Name | Birth | Class | Product | Productnr | Date |\n"
            "|---|---|---|---|---|---|\n"
            + "\n".join("| " + " | ".join(r) + " |" for r in FLAT) + "\n:::")

sl("Flat model example", flat_tbl)
sl("Flat model example", flat_tbl + """

::: {.sm}
**Data is repeated across the table**

- Inefficient use of space
- Problems updating: what if the Productnr of Milk is now 00333?
:::""")

PURCHASE = [["1","06.03.2020","1","1"],["2","06.03.2020","2","2"],
            ["3","06.03.2020","1","2"],["4","06.03.2020","3","1"],
            ["5","07.03.2020","4","2"],["6","07.03.2020","1","1"],
            ["7","08.03.2020","3","1"],["8","08.03.2020","2","1"]]
def purchase_tbl(cls=".xs"):
    return ("::: {.tbl-grid " + cls + "}\n| Nr | Date | Name | Product |\n|---|---|---|---|\n"
            + "\n".join("| " + " | ".join(r) + " |" for r in PURCHASE) + "\n:::")

NAMES_T1 = ("::: {.tbl-grid .xs}\n| Nr | Name | Birth | Class |\n|---|---|---|---|\n"
            "| 1 | Hans | 1998 | T1 |\n| 2 | Fred | 1999 | T1 |\n"
            "| 3 | Anna | 2000 | W1 |\n| 4 | Verena | 1998 | W1 |\n:::")
NAMES_T2 = ("::: {.tbl-grid .xs}\n| Nr | Name | Birth | Class |\n|---|---|---|---|\n"
            "| 1 | Hans | 1998 | 1 |\n| 2 | Fred | 1999 | 1 |\n"
            "| 3 | Anna | 2000 | 2 |\n| 4 | Verena | 1998 | 2 |\n:::")
PRODUCT_T = ("::: {.tbl-grid .xs}\n| Nr | Product | Productnr |\n|---|---|---|\n"
             "| 1 | Milk | 00111 |\n| 2 | Tea | 00222 |\n:::")
CLASSES_T = ("::: {.tbl-grid .xs}\n| Nr | Name |\n|---|---|\n| 1 | T1 |\n| 2 | W1 |\n:::")

for note in ["**Primary key**", "**Foreign keys** reference primary keys<br>(on another table or the same table)"]:
    sl("Building a relational database", f""":::: {{.columns}}
::: {{.column width="46%"}}
::: {{.center-h .xs}}
**Table purchase**
:::

{purchase_tbl()}

::: {{.center-h .xs}}
{note}
:::
:::

::: {{.column width="54%"}}
::: {{.center-h .xs}}
**Table Names**
:::

{NAMES_T1}

::: {{.center-h .xs}}
**Table Product**
:::

{PRODUCT_T}
:::
::::""")

NORM_NOTES = [
    "- Relational database designs can be standardized using **normal forms**\n- For example here: Class should be its own table",
    "Now we can update the name of a class to another one without having to edit the purchase table",
]
for note in NORM_NOTES:
    sl("Relational database: normal form example", f""":::: {{.columns}}
::: {{.column width="42%"}}
::: {{.center-h .xs}}
**Table purchase**
:::

{purchase_tbl(".xxs")}
:::

::: {{.column width="34%"}}
::: {{.center-h .xs}}
**Table Names**
:::

{NAMES_T2}

::: {{.center-h .xs}}
**Table Product**
:::

{PRODUCT_T}
:::

::: {{.column width="24%"}}
::: {{.center-h .xs}}
**Table Classes**
:::

{CLASSES_T}
:::
::::

::: {{.xs}}
{note}
:::""")

sl("Structured Query Language (SQL)", outline(3))

sl("SQL Programming Language", """::: {.sm}
- special-purpose language specifically developed for managing data through relational database systems
- consists of three (co-dependent) language definitions
  - **data definition language (DDL)**
    - define relational schemata
    - create / alter / delete tables and their attributes
  - **data manipulation language (DML)**
    - insert / delete / modify entries in tables
    - query one or more tables
  - **data control language (DCL)**
    - control access to data stored in the database
    - grant / revoke / modify user access rights
:::""")

sl("SQL Programming Language", """::: {.sm}
- SQL is a very **high-level** programming language
  - performance is good because the actual operations are optimized well
  - many different standards, but typical DBMS support all
  - execution is highly parallelizable by construction
- SQL is a **declarative** language
  - You define *what* you want, the DBMS takes care of *how* to do it
  - You can also do "procedural SQL" with special instructions, but it is very inefficient
:::

::: {.center-h}
![](figures/11-sql-flow.svg){height="5.4em"}
:::""")

PRODUCT_SQL_ROWS = [["Gizmo","$19.99","GizmoWorks"],["Powergizmo","$29.99","GizmoWorks"],
                    ["SingleTouch","$149.99","Canon"],["MultiTouch","$203.99","Hitachi"]]
def product_sql(hl=""):
    cls = ".tbl-product" + (" ." + hl if hl else "")
    return ("::: {.tbl-name}\nProduct\n:::\n\n::: {" + cls + "}\n"
            "| PName | Price | Manufacturer |\n|---|---|---|\n"
            + "\n".join("| " + " | ".join(r) + " |" for r in PRODUCT_SQL_ROWS)
            + "\n:::")

TABLES_DEF = """::: {.definition}
[Tables]{.label}
A multiset of tuples coding the attributes specified by the database schema.
:::

::: {.sm}
- Tables are also called **relations**
- Tuples are also called **rows**
- Attributes are also called **columns**
:::"""

TABLE_SLIDES = [("", None), ("hl-relation", "Table (relation)"), ("hl-row", "Row (tuple)"),
                ("hl-row", "Row (tuple)"), ("hl-col", "Column (attribute)"),
                ("hl-schema", "Schema")]
for k, (hl, cap) in enumerate(TABLE_SLIDES):
    extra = ""
    if k == 3:
        extra = "\n\n::: {.tag .xs}\nCan we have the same row twice?\n:::"
    capline = f"\n\n::: {{.center-h .sm}}\n**{cap}**\n:::" if cap else ""
    sl("Tables in SQL", f""":::: {{.columns}}
::: {{.column width="48%"}}
{TABLES_DEF}{extra}
:::

::: {{.column width="52%"}}
{product_sql(hl)}{capline}
:::
::::""")

sl("SQL Data types", """::: {.sm}
- **Data Types**
  - atomic types:
    - characters: `CHAR(20)`, `VARCHAR(50)`
    - numbers: `INT`, `BIGINT`, `SMALLINT`, `FLOAT`
    - others: `MONEY`, `DATETIME`, …
  - every attribute (column) must have an **atomic** type
    - consequently tables in SQL are always **flat**: cells (in principle) should not contain lists or matrices
:::""")

sl("SQL Schema", """::: {.sm}
- **Table Schema**
  - the schema of a table is its name, attributes and their types
    - in our example:<br>`Product: (Pname: string, Price: float, Manufacturer: string)`
  - a **key** is a minimal subset of attributes that acts as a unique identifier for tuples in a relation
    - an implicit constraint on which tuples can be in a relation
      - if two tuples in the same table agree on the values of the key, they must be the same tuple!
    - notation: in the schema the key is <u>underlined</u> &ndash; `Pname` in our example
:::""")

sl("SQL data definition language", """::: {.sm}
- **CREATE:**
:::

```sql
CREATE TABLE extable(col1 INTEGER, col2 VARCHAR(50), PRIMARY KEY (col1));
```

::: {.center-h}
::: {.tbl-name}
extable
:::

::: {.tbl-product}
| col1 | col2 |
|---|---|
| &nbsp; | &nbsp; |
:::
:::

::: {.center-h .sm}
Initializes an empty table with the specified schema: name, attributes and keys
:::""")

sl("SQL data manipulation language", """::: {.sm}
- **INSERT**
:::

```sql
INSERT INTO phone_book (name, number) VALUES ('John Doe', '555-1212');
```

:::: {.columns}
::: {.column width="48%"}
::: {.tbl-name}
phone_book
:::

::: {.tbl-product}
| name | number |
|---|---|
| Jane Doe | 333-333 |
| Max Mustermann | 4949-4900 |
:::

::: {.center-h .xs}
*before*
:::
:::

::: {.column width="48%"}
::: {.tbl-name}
phone_book
:::

::: {.tbl-product}
| name | number |
|---|---|
| Jane Doe | 333-333 |
| Max Mustermann | 4949-4900 |
| **John Doe** | **555-1212** |
:::

::: {.center-h .xs}
*after*
:::
:::
::::""")

sl("SQL data manipulation language", """::: {.sm}
- **UPDATE**
:::

```sql
UPDATE Table1 SET C1 = C1 + 1 WHERE C2 = 'a';
```

:::: {.columns}
::: {.column width="44%"}
::: {.tbl-name}
Table1
:::

::: {.tbl-product}
| C1 | C2 |
|---|---|
| 1 | a |
| 2 | b |
| 3 | a |
| 4 | x |
:::

::: {.center-h .xs}
*before*
:::
:::

::: {.column width="44%"}
::: {.tbl-name}
Table1
:::

::: {.tbl-product}
| C1 | C2 |
|---|---|
| **2** | a |
| 2 | b |
| **4** | a |
| 4 | x |
:::

::: {.center-h .xs}
*after*
:::
:::
::::""")

sl("SQL data manipulation language", """::: {.sm}
- **DELETE**
:::

```sql
DELETE FROM example WHERE column2 = 'N';
```

::: {.sm}
- **DROP**
:::

```sql
DROP TABLE table_name;
```

::: {.sm}
  - Many things can be dropped: indices, columns, whole databases…
- **ROLLBACK**
  - Discards all data changes since the last `COMMIT` or `ROLLBACK`
  - By default, a set of manipulations are part of a *transaction* that is executed and finished when we call `COMMIT`
:::

::: {.source}
SQL tutorial: <https://www.w3schools.com/sql/default.asp>
:::""")

sl("SQL Queries", """::: {.sm}
SQL **queries** allow us to define what data to receive from a database.
:::

::: {.example style="width:82%;margin:0.8em auto"}
[Basic form of a SQL query:]{.label}

```sql
SELECT <attributes> FROM <one or more relations> WHERE <conditions>
```
:::""")

sl("SQL Queries: selection", """::: {.sm}
**selection example:**
:::

```sql
SELECT * FROM Product WHERE Manufacturer = 'Gizmo Works'
```

""" + product_sql("hl-select"))

sl("SQL Queries: selection + projection", """::: {.sm}
**selection + projection example:**
:::

```sql
SELECT Pname, Price FROM Product WHERE Manufacturer = 'Gizmo Works'
```

""" + product_sql("hl-project"))

sl("Aggregation in SQL", """```sql
SELECT AVG(Price) FROM Product WHERE Manufacturer = 'Gizmo Works'
```

:::: {.columns}
::: {.column width="62%"}
""" + product_sql() + """
:::

::: {.column width="38%"}
<br><br>

::: {.tbl-product}
| AVG(Price) |
|---|
| $24.99 |
:::
:::
::::""")

sl("Grouping and aggregating in SQL", """```sql
SELECT AVG(Price) FROM Product GROUP BY Manufacturer
```

:::: {.columns}
::: {.column width="58%"}
""" + product_sql() + """
:::

::: {.column width="42%"}
<br><br>

::: {.tbl-product}
| Manufacturer | AVG(Price) |
|---|---|
| GizmoWorks | $24.99 |
| Canon | $149.99 |
| Hitachi | $203.99 |
:::
:::
::::

::: {.center-h .xs}
More about aggregation and grouping in the tutorial sessions
:::""")

PURCHASE_J = [["1","06.03.2020","1","1"],["2","06.03.2020","2","2"],
              ["3","06.03.2020","1","2"],["4","06.03.2020","3","1"],
              ["5","07.03.2020","4","3"],["6","07.03.2020","1","3"],
              ["7","08.03.2020","3","4"],["8","08.03.2020","2","4"]]
def purchase_j(cols=("Nr","Date","Name","Product")):
    head = "| " + " | ".join(cols) + " |\n|" + "---|"*len(cols)
    return ("::: {.tbl-product .xs}\n" + head + "\n"
            + "\n".join("| " + " | ".join(r) + " |" for r in PURCHASE_J) + "\n:::")

sl("SQL manual join", """::: {.sm}
- A **join** resembles a merge or product operation in other languages
:::

```sql
SELECT * FROM purchase, Product WHERE purchase.Product = Product.Nr;
```

:::: {.columns}
::: {.column width="52%"}
::: {.tbl-name}
purchase
:::

""" + purchase_j() + """
:::

::: {.column width="48%"}
::: {.tbl-name}
Product
:::

::: {.tbl-product .xs}
| Nr | Product | Productnr |
|---|---|---|
| 1 | Milk | 00111 |
| 2 | Tea | 00222 |
:::
:::
::::""")

sl("SQL manual join", """```sql
SELECT * FROM purchase, Product WHERE purchase.Product = Product.Nr;
```

::: {.sm}
**Result:**
:::

::: {.tbl-product .xs}
| Nr | Date | Name | purchase.Product | Product.Product | Productnr |
|---|---|---|---|---|---|
| 1 | 06.03.2020 | 1 | 1 | Milk | 00111 |
| 2 | 06.03.2020 | 2 | 2 | Tea | 00222 |
| 3 | 06.03.2020 | 1 | 2 | Tea | 00222 |
| 4 | 06.03.2020 | 3 | 1 | Milk | 00111 |
:::

::: {.xs}
- Why are there now only four rows when purchase had 8?
- Why are there new column names?
- How many rows would we get with `SELECT * FROM purchase, Product;`?
:::""")

sl("Better naming of columns", """:::: {.columns}
::: {.column width="52%"}
::: {.tbl-name}
purchase
:::

""" + purchase_j(("ID","Date","Name","ProductID")) + """
:::

::: {.column width="48%"}
::: {.tbl-name}
Product
:::

::: {.tbl-product .xs}
| ProductID | Product | Productnr |
|---|---|---|
| 1 | Milk | 00111 |
| 2 | Tea | 00222 |
:::
:::
::::

::: {.xs}
- References to keys of other columns are called **foreign keys**
- Naming can be done in a smart way to simplify expected joins
:::""")

sl("SQL INNER JOIN", """```sql
SELECT * FROM purchase INNER JOIN Product USING (ProductID);
```

::: {.sm}
**Result:**
:::

::: {.tbl-product .xs}
| Nr | Date | Name | ProductID | Product | Productnr |
|---|---|---|---|---|---|
| 1 | 06.03.2020 | 1 | 1 | Milk | 00111 |
| 2 | 06.03.2020 | 2 | 2 | Tea | 00222 |
| 3 | 06.03.2020 | 1 | 2 | Tea | 00222 |
| 4 | 06.03.2020 | 3 | 1 | Milk | 00111 |
:::""")

sl("SQL other JOIN operations", """::: {.imgrow .middle}
![](figures/join-inner.png){height="5.2em"}
![](figures/join-left.png){height="5.2em"}
![](figures/join-full-outer.png){height="5.2em"}
:::

::: {.sm}
- There are different kinds of joins based on **set operations**
- If values are missing from one of the columns, they are set to `NULL`
:::

::: {.source}
More on the SQL tutorial: <https://www.w3schools.com/sql/default.asp>
:::""")

sl("SQL injections", """::: {.imgrow .middle}
![](figures/xkcd-bobby-tables.jpg){height="5.6em"}
![](figures/drop-table-plates.png){height="5.6em"}
:::

::: {.sm}
- A **SQL injection** is a security attack on a database that inputs SQL code as user input (e.g. a user name)
- If the database permissions are not well set, it could be executed
- It can be used to delete the database, for illicit data export, or to gain access to other parts of the system
:::

::: {.source}
XKCD 327, *Exploits of a Mom*: <https://xkcd.com/327/>
:::""")

sl("Summary", """::: {.sm}
- **Databases**
  - Technology to centralize, manage and provide access to data
  - A DBMS is software that handles the DB while we just operate with it
- **Relational Databases**
  - When tables refer to each other: more efficient storage and update
- **Structured Query Language (SQL)**
  - The most used language for relational databases
:::""")

open(OUT, "w").write("".join(s))
print("slides:", "".join(s).count("\n## "))
