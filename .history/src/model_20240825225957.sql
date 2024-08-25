-- Step 1: Filter the equitable owner history based on loan account and transaction date
WITH Filtered_Owner_History AS (
    SELECT 
        ae.Id AS Accounting_Entry_Id,
        ae.Transaction_Date,
        ae.Loan_Account_Id,
        aeh.Reallocation_Date,
        aeh.Equitable_Owner_Id,
        -- Assign a row number to select the most recent reallocation date for each accounting entry
        ROW_NUMBER() OVER (
            PARTITION BY ae.Id 
            ORDER BY aeh.Reallocation_Date DESC
        ) AS rn
    FROM 
        Accounting_Entry ae
    JOIN 
        ATH_Equitable_Owner_History aeh 
    ON 
        ae.Loan_Account_Id = aeh.Loan_Account_Id
    WHERE 
        aeh.Reallocation_Date <= ae.Transaction_Date
) 
-- Step 2: Select the relevant accounting entry fields along with the correct equitable owner name
SELECT 
    ae.Id AS Accounting_Entry_Id,
    ae.Transaction_Date,
    ae.Loan_Account_Id,
    ae.Credit_Amount,
    ae.Debit_Amount,
    ae.Credit_GL_Account_Code,
    ae.Debit_GL_Account_Code,
    eo.Name AS Equitable_Owner_Name
FROM 
    Filtered_Owner_History foh
JOIN 
    Accounting_Entry ae 
ON 
    foh.Accounting_Entry_Id = ae.Id
JOIN 
    Equitable_Owner eo 
ON 
    foh.Equitable_Owner_Id = eo.Id
WHERE 
    foh.rn = 1  -- Select the row with the most recent reallocation date for each accounting entry
ORDER BY 
    ae.Transaction_Date,  -- Optional: Order the results by transaction date
    ae.Loan_Account_Id;