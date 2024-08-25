# Project Athena Technical Challenge

🚀️ 🚀️ 🚀️Athena Technical Challenge   ---- Olivia 👀️

---

## Load Data Into Suitable Database Model

**Data Sources**：
CSV Files

- Accounting_Entry
- Equitable_Owner
- Equitable_Owner_History

Tables(MySQL):

- Accounting_Entry
- Equitable_Owner
- ATH_Equitable_Owner_History
- Loan_Account

**Loading Data**：

* Data PreProcess: data_preprocess.py()
* Create Database:   `create database athena_challege;`
*  Create Tables:
```
CREATE TABLE Equitable_Owner (
    Id varchar(18) primary key,
    Name varchar(255) not null);

CREATE TABLE Loan_Account(
  Id varchar(18) primary key);

CREATE table ATH_Equitable_Owner_History(
    Equitable_Owner_History_Id int auto_increment primary key,
    Reallocation_Date Date not null, 
    From_Equitable_Owner_Id varchar(18) null, 
    Equitable_Owner_Id varchar(18) not null,
    Loan_Account_Id varchar(18) not null,
    CONSTRAINT fk_from
        FOREIGN KEY (From_Equitable_Owner_Id) REFERENCES Equitable_Owner(Id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_to
        FOREIGN KEY (Equitable_Owner_Id) REFERENCES Equitable_Owner(Id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_loan
        FOREIGN KEY (Loan_Account_Id) REFERENCES Loan_Account(Id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
 );

CREATE TABLE Accounting_Entry (
    Id VARCHAR(18) primary key,
    Transaction_Date DATE not null,
    Loan_Account_Id VARCHAR(18) not null,
    Credit_Amount NUMERIC not null,
    Credit_GL_Account_code VARCHAR(10) not null,
    Debit_Amount NUMERIC not null,
    Debit_GL_Account_code VARCHAR(10) not null,
    CONSTRAINT fk_loan_account
        FOREIGN KEY (Loan_Account_Id) REFERENCES Loan_Account(Id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

* Load Data: Import Data  -> Check Schema Mapping -> Preview Data ....

**Note:** Cuz Equitable_Owner_History first row  'From_Equitable_Owner_Id' is null,  before we load data to MySQL table, we need `set foreign_key_checks=0` otherwise, it will show following **error**.
*sql error [1452] [23000]: cannot add or update a child row: a foreign key constraint fails (`athena_challenge`.`ath_equitable_owner_history`, constraint `fk_from` foreign key (`from_equitable_owner_id`) references `equitable_owner` (`id`) on delete set null on update cascade)*

## Build a new model

**Build a new which assigns the correct equitable owner name for each accounting entry, given:**

* equitable owner record reallocation date is the same as the accounting entry transaction date or,
* equitable owner record reallocation date is the most recent to the accounting entry transaction date
* note: there will only ever be a single equitable owner record for a loan id and reallocation date

Please run **"model.sql:"**

## Stretching (If Tech Stack Includes: DBT)

##### How would you test that this model is behaving predictably in a production environment?

* Unit Tests and Data validation:
    **Schema Test**: we can create a dbt test yml file:eg: 
    ```
        models:
            - name: accounting_entries
                columns:
                - name: loan_account_id
                    tests:
                    - not_null
                    - unique
                - name: transaction_date
                    tests:
                    - not_null
                - name: equitable_owner_name
                    tests:
                    - not_null 
    ```
    **Custom SQL Tests**:
    ```--- tests/check_correct_owner.sql:
    SELECT
      COUNT(*)
    FROM {{ ref('accounting_entries') }}
    WHERE transaction_date < reallocation_date
    AND correct_equitable_owner IS NOT NULL;
    ```
    **Run Command: dbt test --select XXX**;




##### How would you deploy this model to create a dataset that would be accessible for analytics?

###### Set Up DBT Project and Environment:
* Connect DBT Code Repo:
* First initial Project with appropriate  environments 
* Define model.yml; source.yml; 
* Design and Build the Data Model and some macro functions can be reused:
    **models/model.sql**

```
WITH Filtered_Owner_History AS (
    SELECT 
        ae.id AS accounting_entry_id,
        ae.transaction_date,
        ae.loan_account_id,
        aeh.reallocation_date,
        aeh.equitable_owner_id,
        ROW_NUMBER() OVER (
            PARTITION BY ae.id 
            ORDER BY aeh.reallocation_date DESC
        ) AS rn
    FROM 
        {{ ref('accounting_entry') }} ae
    JOIN 
        {{ ref('ath_equitable_owner_history') }} aeh 
    ON 
        ae.loan_account_id = aeh.loan_account_id
    WHERE 
        aeh.reallocation_date <= ae.transaction_date
)
SELECT 
    ae.id AS accounting_entry_id,
    ae.transaction_date,
    ae.loan_account_id,
    ae.credit_amount,
    ae.debit_amount,
    ae.credit_gl_account_code,
    ae.debit_gl_account_code,
    eo.name AS correct_equitable_owner
FROM 
    Filtered_Owner_History foh
JOIN 
    {{ ref('accounting_entry') }} ae 
ON 
    foh.accounting_entry_id = ae.id
JOIN 
    {{ ref('equitable_owner') }} eo 
ON 
    foh.equitable_owner_id = eo.id
WHERE 
    foh.rn = 1;
```

###### Finally:
then we can deploy it as a job and trigger every data:
  * Command: dbt run --select models.* (if we have other models)
  * Schedule: we can trigger by api as part of pipeline or schedule it every day


Note:
   * We can use BI tools to connect Data warehouse to visualization.
   * We can limit different users with different access permissions to DW
