[WIP SEBI]
For class equivalence, we have 4 parameters and these 4 parameters can be classified in the following categories

| Parameter        | Valid Class                                     | Invalid Classes                                                                                         |
| ---------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Email**        | Correct format (`john.doe@example.com`), unique | Incorrect format (`johndoeexample.com`, `john.doe@com`), already registered                             |
| **Username**     | 3-20 characters (`john123`, `user_name`)        | Too short (< 3 characters, e.g., `ab`), too long (> 20 characters, e.g., `thisusernameiswaytoolong123`) |
| **Birth Date**   | Format `YYYY-MM-DD`, past date (`1990-05-10`)   | Incorrect format (`1990/05/10`), future date (`2090-05-10`)                                             |
| **Phone Number** | Valid prefix (`+40 712345678` for Romania)      | Invalid prefix (`+99 712345678`), mismatched country (`country="Romania"` but number starts with `+33`) |
