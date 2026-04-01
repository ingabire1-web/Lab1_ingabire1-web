# Lab1_ingabire1-web
Individual coding lab

Overview of the whole projeect.
This project ia a two-part graging system built for an institution like ALU showing how student's grades are evaluated and decisions at the end of every grading systems.
The project has a python script that check through and work a student grades from a csv file and a bash shell script that handles archiving and worspace management btn grading sessions.

Below there is a project structure.
📂 your-project-folder/
│
├── grade-evaluator.py       ← Main Python grading program
├── organizer.sh             ← Bash script for archiving and workspace reset
├── grades.csv               ← Your input file (fill this with student data)
│
├── 📂 archive/              ← Auto-created by organizer.sh
│     ├── grades_20251105-170000.csv
│     ├── grades_20251106-090000.csv
│     └── ...                ← Every past batch is stored here with a timestamp
│└── organizer.log            ← Auto-created log file, accumulates every run

How to run the file in the terminal:
# since we have two files which  are of different types one is a pythone file while the other is a shell script file therefore the way of running them is different

1.In the terminal write the following to run a python script
python3 grade-evaluator.py
when prompted, type the name of your CSV file: Your grades.csv must have four columns which are assignment,group,score,weight

2.For a shell file first give it permissions for execution by typing chmod +x organizer.sh
then run it: ./organizer.sh
Finally everything has run sucessfull then know that the final thing you see is that the archive forlder now holds the old batch safely, and a fresh empty grades.csv is ready for the next student 

Thank you for using this platform 