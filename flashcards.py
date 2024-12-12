# Flashcard App - Samantha Song - started 2024.12.05
# An extension of my Simple Flashcard Tester
# Basic Screen - Click Buttons or Press Keys
# Flashcard (FC) - database
#   side_1 - english
#   side_2 - hirigana / katakana
#   side_3 - romanji
#   side_4 - kanji
#   side_5 - type (noun, verb, adj, etc)
#   correct - times guessed correctly
#   incorrect - times guessed incorrectly
#   prev_corr - True or False - was the FC guessed correctly most recently
#   last_date - Date - since last daily review

# Import packages
from datetime import datetime
import pandas as pd

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

# Start Program
def start_program():
    while True:
        try:
            print("Press [1] to add a flashcard.")
            print("Press [2] to remove a flashcard.")
            print("Press [3] to test all flashcards.")
            print("Press [4] to do a daily review.")
            print("Press [s] to save your progress.")
            print("Press [q] to quit.")
            option = input("What would you like to do: ")
            if option == '1':
                add_fc()
            elif option == '2':
                remove_fc()
            elif option == '3':
                test_all()
            elif option == '4':
                daily_ids = daily_review()
                test_all(test_ids=daily_ids)
            elif option.lower() == 's':
                # Write updated data to new csv
                db.to_csv(fc_csv_name, index=False) 
            elif option.lower() == 'q':
                return 0
            else:
                raise ValueError
        except ValueError:
            print("Press [1] to add a flashcard.")
            print("Press [2] to remove a flashcard.")
            print("Press [3] to test all flashcards.")
            print("Press [4] to do a daily review.")
            print("Press [s] to save your progress.")
            print("Press [q] to quit.")


# Add single Flashcard - does not write to csv file - need to do elsewhere
def add_fc():
    global rows
    global db
    column_names = db.columns.tolist()
    new_fc = []
    for col in range(columns - 5):
        new_side = input("Please type what you would like for " + column_names[col] + ": ")
        new_fc.append(new_side)
    print(new_fc)
    new_fc.extend([0, 0, False, today.strftime(date_format)])
    while True:
        try:
            add_fc_yn = input("Would you like to add this flashcard? Y/N: ")
            if add_fc_yn.lower() == 'y':
                db.append(new_fc)
                rows = db.shape[0]
                break
            elif add_fc_yn.lower() == 'n':
                print("This flashcard will not be added.")
                break
            else:
                raise ValueError
        except ValueError:
            print("Please type [Y]es or [N]o.")


# Remove single Flashcard - does not write to csv file - need to do elsewhere
def remove_fc():
    global rows
    global db
    to_remove = input("Please type side1 of the flashcard you would like to remove: ")
    for ind in range(rows):
        if db.iloc[ind, 0] == to_remove:
            print(db.iloc[ind])
            while True:
                try:
                    check = input("Is this the flashcard you want to remove? Y/N: ")
                    if check.lower() == 'y':
                        db = db.drop(ind)
                        rows = db.shape[0]
                        print("This flashcard was removed.")
                    elif check.lower() == 'n':
                        print("This flashcard will not be removed.")
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please type [Y]es or [N]o.")


# Test all Flashcards (FC)
# Pass in indexes of FC to test, full set, list of sides for front and back
# Returns the following:
#   1 - No Flashcards to test
#   2 - All Flashcards have been tested
#   3 - Tester choses to end test without testing all Flashcards
# Tests all flashcards based on test_ids and test_set
def test_all(test_ids=all_ids, test_set=db, front=fc_front, back=fc_back):
    # End if there are no Flashcards to test
    if len(test_ids) == 0:
        print("There are no flashcards to test")
        return 1
    # Test all Flashcards in set one by one unless tester exits (corr/incorr keep progress)
    # Number of tested flashcards - can change if tester makes a mistake
    num_test = 0
    # Start on front side f
    front_side = True
    while num_test <= len(test_ids):
        print("\n\n")
        # Allows tester to fix previous mistake if not the first card
        if num_test > 0:
            print("Press [b] to return to previous flashcard.\n")

        # If all flashcards have been tested, check if mistake was made on last fc
        if num_test == len(test_ids):
            print("\nPress [enter] to complete the test.\n\n")
            while True: 
                try:
                    option = input("What would you like to do: ")
                    # If tester chooses to end the session prematurely
                    if option.lower() == 'q':
                        return 3
                    # If tester made a mistake on the previous FC
                    # Index will automatically be last index - has not yet been updated
                    elif option.lower() == 'b':
                        print("Showing the previous flashcard.")
                        prev_prev_corr = test_set.iloc[index, prev_corr]
                        if prev_prev_corr == True:
                            test_set.iloc[index, corr] -= 1
                        else:
                            test_set.iloc[index, incorr] -= 1
                        num_test -= 1
                        front_side = True
                        break
                    elif option.lower() == '':
                        # Once all FC have been tested - finish test session
                        print("You have completed all the flashcards in this set.")
                        return 2
                    else:
                        raise ValueError
                except ValueError:
                    print("Please choose to [q]uit, go [b]ack to the last flashcard, or [enter] to complete")

        # Makes it easier to go back if a mistake was made
        index = test_ids[num_test]

        # Prints Front Side
        if front_side == True:
            for side in front:
                print(str(test_set.iloc[index, side]))
        # Prints Back Side
        else:
            for side in back:
                print(str(test_set.iloc[index, side]))
        print("\nPress [f] if you were incorrect.")
        print("Press [j] if you were correct.")
        print("Press [enter] to flip the card.")
        print("Press [q] to end the session.\n")

        # Wait on each flashcard until tester gets them correct or incorrect
        while True: 
            try:
                option = input("What would you like to do: ")
                # If tester chooses to end the session prematurely
                if option.lower() == 'q':
                    return 3
                # If tester made a mistake on the previous FC
                elif option.lower() == 'b' and num_test > 0:
                    print("Showing the previous flashcard.")
                    prev_index = index - 1
                    prev_prev_corr = test_set.iloc[prev_index, prev_corr]
                    if prev_prev_corr == True:
                        test_set.iloc[prev_index, corr] -= 1
                    else:
                        test_set.iloc[prev_index, incorr] -= 1
                    num_test -= 1
                    front_side = True
                    break
                # Tester gets the flashcard Incorrect
                elif option.lower() == 'f':
                    print("You got this flashcard incorrect.")
                    # Update Incorrect and Last Correct
                    test_set.iloc[index, incorr] += 1
                    test_set.iloc[index, prev_corr] = False
                    test_set.iloc[index, last_date] = today.strftime(date_format)
                    num_test += 1
                    front_side = True
                    break
                # Tester gets the flashcard Correct
                elif option.lower() == 'j':
                    print("You got this flashcard correct!")
                    # Update Correct and Last Correct
                    test_set.iloc[index, corr] += 1
                    test_set.iloc[index, prev_corr] = True
                    test_set.iloc[index, last_date] = today.strftime(date_format)
                    num_test += 1
                    front_side = True
                    break
                # Tester flips the flashcard
                elif option.lower() == '':
                    front_side = not front_side
                    break
                else:
                    raise ValueError
            except ValueError:
                print("\nPress [f] if you were incorrect.")
                print("Press [j] if you were correct.")
                print("Press [enter] to flip the card.")
                print("Press [q] to end the session.\n")
        # Print both sides?
    # Once all FC have been tested - finish test session
    print("-------------------------------------")
    print("\nYou have completed all the flashcards in this set.")
    return 2


# Daily Review (DR)
#   Dependent on % correct and time since last DR
def daily_review(test_set=db):
    daily_set = []
    for index in range(rows):
        fc = test_set.iloc[index]
        # Number of times a FC has been tested
        num_tested = fc.iloc[corr] + fc.iloc[incorr]
        # FC has never been tested, add to daily_set list
        if num_tested == 0:
            daily_set.append(index)
        # Dependent on % correct and time since last 
        else:
            # Percentage that a FC has been guessed correctly
            perc_corr = fc.iloc[corr] / num_tested
            # Days since last time FC was tested
            last_date_str = fc.iloc[last_date]
            last_date_obj = datetime.strptime(last_date_str, date_format)
            days_since = (today - last_date_obj).days
            if perc_corr >= 0.90 and days_since >= 5:
                daily_set.append(index)
            elif perc_corr >= 0.75 and days_since >= 3:
                daily_set.append(index)
            elif perc_corr >= 0.50 and days_since >= 2:
                daily_set.append(index)
            elif perc_corr <= 0.50 and days_since >= 1:
                daily_set.append(index)
    # Returns list of indexes to test from full list
    return daily_set


start_program()
