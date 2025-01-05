# Flashcard Tester - Version 2

## Description
This project is an extension of the Flashcard Tester - Simple Version. 
The main additions are:
- Adding Flashcards - User inputs values for the different sides of the cards and confirm changes
- Removing Flashcards - User inputs the value for side1 of the flashcard they would like to remove and confirm changes. (This assumes that all side1 values are unique.)
- Daily Review - Creates a subset of flashcards which the user tends to struggle with according to the following:
  - User gets flashcard correct less than 50% of the time and it has been at least 2 days since it has been in the daily review.
  - User gets flashcard correct between 50% - 75% of the time and it has been at least 2 days since it has been in the daily review.
  - User gets flashcard correct between 75% - 90% of the time and it has been at least 3 days since it has been in the daily review.
  - User gets flashcard correct more than 90% of the time and it has been at least 5 days since it has been in the daily review.

This is a simple flashcard tester which takes flashcards from a CSV file, and allows the user to mark each flashcard as either correct or incorrect and records how many times a flashcard is marked correct/incorrect.
In the event that the user incorrectly marks a card correct or incorrect, the user can go back to the previous card.
The amount of times the user gets a flashcard correct or incorrect is also adjusted when the user chooses to go back to the previous card.
Once all flashcards have been tested, the user has a chance to return to the last card, in case they made a mistake on the last card. 
After all flashcards are tested or the user quits prematurely, the CSV file is over written with the updated scores.

## CSV File Requirements - Flashcards
This code requires the python program to be in the same directory as the CSV file which contains the flashcards the user wants to test.
The CSV file requires at least 5 columns:
- side1 - side of the flashcard
- side2 - side of the flashcard
- side3 ... side# - sides of flashcard (optional)
- corr - # of times tester has gotten the answer correct
- incorr - # of times the tester has gotten the answer incorrect
- prev_corr - boolean - did tester get the answer correct last time?
- last_date - the last date of when the flashcard was tested in the daily review. (In the format MM/DD/YY.)
  
>[!IMPORTANT]
>Last 3 columns must always be correct, incorrect, prev_corr, and last_date. (In that order.)

>[!NOTE]
>By default, the program assumes that there are column names. Thus, the first row will not be tested.

## Adapting the Code
In the code, update the file name to the desired CSV file name ```fc_csv_name = '<filename>.csv'```.

If there are more than 2 sides to the flashcards, the sides that show up on the front and back of the flashcards can be adjusted by changing the lists ```fc_front``` and ```fc_back```.
The list of integers are the indexes for the columns in the CSV file.

```
# Gobal Variables
today = datetime.today()
fc_csv_name = "flashcards.csv"
db = pd.read_csv(fc_csv_name)
rows = db.shape[0] # Number of Rows - Number of flashcards
columns = db.shape[1] # Number of Columns - Number of sides + 4 (corr, incorr, prev_corr, last_date)
date_format = '%m/%d/%Y' # MM/DD/YYYY
all_ids = range(rows)

# Flashcards - Last 4 columns must always be correct, incorrect, and prev_corr, date
corr = columns - 4
incorr = columns - 3
prev_corr = columns - 2
last_date = columns - 1

# EDITABLE VARIABLES
# Sets the front and back of flashcards via sides (side1, side2, etc)
fc_front = [0, 4]
fc_back = [3, 1, 2, 4]
```

> [!IMPORTANT]
> Unlike the prior simple verison, the flashcard CSV file name is a variable, so only the variable ```fc_csv_name``` needs to be updated.
>```
 
