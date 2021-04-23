# Load_Switching_2


## PGE-GEL Capstone Project 


NeoCharge Averaged Switching Characteristics Using State Machine Logic

for 1 second time interval input CSV files (no header)

Input-

Column 1: DateTime

Column 2: Watts
<br />
<br />
<br />
<br />
<br />
**Normal Usage-**

Command: NeoCharge_1sec_Switch.py primary.csv secondary.csv out.csv

Output-

Column 1: DateTime

Column 2: Switched Watts
<br />
<br />
<br />
<br />
<br />
**Advanced Usage-**

Command: NeoCharge_1sec_Switch.py primary.csv secondary.csv out.csv --verbose

Output-

Column 1: DateTime

Column 2: Unix Time

Column 3: Primary Watts

Column 4: Secondary Watts

Column 5: Switched Watts

Column 6: State Space (primary / secondary)

Column 7: State Change (Ture / False)

Column 8: Secondary DateTime

