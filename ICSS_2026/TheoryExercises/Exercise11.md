# Exercise Sheet 11: Databases

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

> Exercises 1–2 are worked through in the exercise session. The *Additional
> practice* section is for self-study. Worked solutions to every exercise, with
> pointers to the slides and the handout sections that cover the material, are
> in [`Solutions/Exercise11-Solutions.md`](Solutions/Exercise11-Solutions.md); try before you open them.
> Notation: [course conventions](../Transcripts/00-Conventions.md).

---

## Exercise 1: From a flat table to a relational database

You receive the following table from the sales department:

| UserNumber | UserName | PurchaseTime | ProductName | N | ProductID | Delivered |
|---|---|---|---|---|---|---|
| 011011 | Hans | 2020.03.06 11:15:55 | Milk | 1 | 011011 | True |
| 012311 | Hans | 2020.04.07 01:50:50 | Milk | 2 | 011011 | True |
| 011011 | Hans | 2020.05.06 10:05:00 | Coffee | 1 | 215511 | True |
| 405444 | Marie | 2020.12.06 21:15:05 | Coffee | 45 | 215511 | False |
| 556677 | Peter | 2021.03.06 03:50:50 | Coffee | 4 | 215511 | True |

a) Without adding any columns, what combination of columns can you use as a
   **primary key**? Explain the assumptions of your solution.

b) Assuming the table above is the only one of a SQL database, write a query that
   lists all rows that correspond to **delivered purchases of more than one
   unit**.

c) Show how to restructure the above table into the tables of a relational
   database that increases the efficiency of **changing the name of products
   while keeping the same ProductID**. Indicate the primary key of this new table
   and give it a name.

d) Based on your tables of the previous result, write a SQL query that gives the
   delivery status of all purchases of the product named "Milk".

> For (a), remember that a key must be **minimal** and must uniquely identify a
> row *for every possible content of the table*, not just for these five rows.
> Say explicitly what you are assuming about the world for your key to hold.

---

## Exercise 2: Designing a schema

A research project collects data on parliamentary debates. For every **speech**
they record who gave it, when, in which debate, and its full text. Every
**speaker** has a name, a party, a birth year and a constituency. Every **debate**
has a title, a date and a topic. Parties have a name and a founding year, and
speakers can change party over time.

a) Design a relational schema for this data. Give each table a name, list its
   attributes with plausible types, and **underline** (or mark) the primary key.
   Indicate the foreign keys and which table they reference.

b) Explain why storing the party name directly in the speech table would be a bad
   idea, and give a concrete update that would go wrong.

c) The requirement that speakers can change party over time is the hard part.
   Explain why a single `party` column in the speaker table is not enough, and
   propose a solution.

d) Write SQL queries for:

   i) the number of speeches per party;
   ii) all speeches given in debates on the topic "climate" by speakers born
       after 1970;
   iii) the average speech length per party, ordered from longest to shortest.

   *(Assume a column `Length` in the speech table for (iii).)*

> Part (c) is the one to think about longest. Ask yourself what a "fact" is here:
> is "Hans is in party X" a fact about Hans, or a fact about Hans *during a
> period of time*? Where a fact lives determines which table it belongs in.

---

## Additional practice

### A1. ACID in practice

For each scenario, name which ACID property is at stake and what would go wrong
without it.

a) A bank transfer crashes after debiting the sender.
b) Two agents sell the same seat on a flight at the same instant.
c) A power cut hits the server one second after a booking is confirmed.
d) An insert adds a purchase referring to a product that does not exist.

### A2. Normalizing

Here is a table of course enrollments:

| Student | StudentEmail | Course | Lecturer | LecturerOffice | Grade |
|---|---|---|---|---|---|
| Anna | anna@uni.de | ICSS | Garcia | D 233 | 1.7 |
| Ben | ben@uni.de | ICSS | Garcia | D 233 | 2.3 |
| Anna | anna@uni.de | Statistics | Meier | C 105 | 2.0 |

a) List every piece of information that is stored redundantly.
b) Give three distinct anomalies (one insert, one update, one delete) that this
   design permits.
c) Restructure it into a set of tables in which each fact is stored once. Mark
   keys and foreign keys.

### A3. Reading joins

With these two tables:

**Author**

| AuthorID | Name |
|---|---|
| 1 | Lazer |
| 2 | Salganik |
| 3 | Schelling |

**Paper**

| PaperID | Title | AuthorID |
|---|---|---|
| 10 | Computational Social Science | 1 |
| 11 | Bit by Bit | 2 |
| 12 | Meaningful measures | 1 |
| 13 | Anonymous preprint | NULL |

a) How many rows does `SELECT * FROM Author, Paper;` return?
b) How many rows does `SELECT * FROM Author INNER JOIN Paper USING (AuthorID);`
   return? Which rows are lost?
c) Write a query returning every author together with their papers, **including
   authors with no papers**.
d) Write a query returning the number of papers per author, including zeros.

### A4. Writing queries

Using the `Product(PName, Price, Manufacturer)` table from the lecture, write SQL
for each request.

a) All products costing more than $50.
b) The names of products made by Canon or Hitachi.
c) The number of products per manufacturer.
d) The most expensive product.
e) Manufacturers with an average price above $100.

### A5. SQL injection

A web form looks up a student by name with this Python code:

```python
query = "SELECT * FROM Students WHERE name = '" + name + "'"
cursor.execute(query)
```

a) What query results if a user enters `Robert'; DROP TABLE Students;--`?
b) Give a different input that would return **all** rows regardless of the name.
c) Rewrite the code so the attack is impossible, and explain why your version
   works.
d) Would restricting the database user's permissions to `SELECT` only prevent
   every kind of injection attack? Explain.

### A6. Declarative vs procedural

a) Explain, in the terms of session 4, what makes SQL a **declarative** language.
b) Give one reason why declarative code can be *faster* than the loop you would
   have written yourself.
c) Session 12 will say that SQL is "highly parallelizable by construction". Why
   does being declarative help with that?
d) When would you nevertheless prefer to pull the data into Python and loop?

---

## Sources

- Exercise 1 is adapted from the 2024 sheet 11 of this course.
- **Codd, E. F. (1970).** "A Relational Model of Data for Large Shared Data
  Banks". *Communications of the ACM* 13(6), 377–387.: The relational model
  underlying exercises 1c, 2 and A2.
- **Garcia-Molina, H., Ullman, J. D. & Widom, J. (2008).** *Database Systems: The
  Complete Book*, 2nd ed. Pearson.: Source of the `Product` table used in A4 and
  of the join semantics in A3.
- **Elmasri, R. & Navathe, S. B. (2016).** *Fundamentals of Database Systems*,
  7th ed. Pearson.: Normal forms and the anomalies enumerated in A2.
- **Härder, T. & Reuter, A. (1983).** "Principles of Transaction-Oriented
  Database Recovery". *ACM Computing Surveys* 15(4), 287–317.: ACID, A1.
- **W3Schools SQL tutorial:** <https://www.w3schools.com/sql/default.asp>,
  Reference for the SQL syntax in exercises 1b, 1d, 2d and A4.
- **OWASP, *SQL Injection*:**
  <https://owasp.org/www-community/attacks/SQL_Injection>: A5.
- **Munroe, R.** *Exploits of a Mom*, XKCD 327: <https://xkcd.com/327/>: A5(a).
