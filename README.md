## NeoCharge Averaged Switching Characteristics Using State Machine Logic


### PGE-GEL Capstone Project 



for 1 second time interval input CSV files (no header)

Input-

|||
|---|---|
|Column 1|DateTime|
|Column 2|Watts|

<hr /> 

**Normal Usage-**

Command: NeoCharge_1sec_Switch.py primary.csv secondary.csv out.csv

Output-

|||
|---|---|
|Column 1|DateTime|
|Column 2|Switched Watts|
<hr /> 

**Advanced Usage-**

Command: NeoCharge_1sec_Switch.py primary.csv secondary.csv out.csv --verbose

Output-

|||
|---|---|
|Column 1|DateTime|
|Column 2|Unix Time|
|Column 3|Primary Watts|
|Column 4|Secondary Watts|
|Column 5|Switched Watts|
|Column 6|State Space (primary / secondary)|
|Column 7|State Change (True / False)|
|Column 8|Secondary DateTime|
