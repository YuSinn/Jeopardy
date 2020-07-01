import pandas as pd
from datetime import  datetime
import random
from time import sleep

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 20)

jeopardy_df = pd.read_csv('jeopardy.csv')

#Here we rename the wrong format columns
jeopardy_df = jeopardy_df.rename(
    columns ={
        " Show Number": "Show_Number",
        " Air Date": "Airdate",
        " Round": "Round",
        " Category": "Category",
        " Value": "Value",
        " Question": "Question",
        " Answer": "Answer",
          
    })
def check(data, list):
    #We put all the words to lower in the list also in the question and we check if all the words from the list are in the questions and return true
    check = lambda x: all( word.lower() in x.lower() for word in list)
    #Here we are applying the lambda function to each question and returns the question that result as True after check
    return jeopardy_df.loc[jeopardy_df["Question"].apply(check)]

#We test the functionabilty of our check_question
checked = check(jeopardy_df,["King", "England"])
#We print what the function returns
#(checked["Question"])
#We print the amount of questions where King and England were found
#print(checked["Question"].count())

def value_list(data):
    #we put in a list all value after $
    return lambda x: float(x[1:].replace(',','')) if x != "None" else 0
    
#We create the new column with only the float values
jeopardy_df["Float Value List"] = jeopardy_df["Value"].apply(value_list(jeopardy_df["Value"]))

#We filter only the question that contains the word King/king
checked_2 = check(jeopardy_df,["King"])

#We calculate the average of the filtred list
#print(checked_2["Float Value List"].mean())

#With this function we will return the count of unique answers
def get_answer_count(data):
    return data["Answer"].value_counts()

#In prisnt we get the amount for of answers for the filtred word
#print(get_answer_count(checked_2))

#In this line we create a colomn Date time in format Date time from string
jeopardy_df["Date time"] = jeopardy_df.Airdate.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

checked_3 = check(jeopardy_df, ["Computer"])

#Creating dataframe that contains only questions from 90s
checked_computer_90s = checked_3[(checked_3["Date time"] >= datetime(1990, 1, 1))\
                               & (checked_3["Date time"] <= datetime(1999,12,31))]
#Creating dataframe that contains only questions from 00s
checked_computer_00s = checked_3[(checked_3["Date time"] > datetime(1999, 12, 31))\
                               & (checked_3["Date time"] <= datetime(2009,12,31))]

#print('Questions of 90s that contain the word "Computer": '+str(checked_computer_90s.Question.count())+'\n'\
#     +'Questions of 00s that contain the word "Computer": '+str(checked_computer_00s.Question.count()))

#Setting a function to return a dataframe with the column round and the category that we want
def round_category_type(type,category):

    return jeopardy_df[(jeopardy_df["Round"] == type) & (jeopardy_df["Category"] == category.upper())]

def round_type(type):

    return jeopardy_df[(jeopardy_df["Round"] == type)]

#the user introduce the category that he want to be filtrated
#what=input('What category do you want to filtrate?\n')

#Single_Jeopardy = round_category_type("Jeopardy!",what)
#Double_Jeopardy = round_category_type("Double Jeopardy!",what)
#Final_Jeopardy = round_category_type("Final Jeopardy!",what)

#Here we are creating one function that find the category with most specific(searched) category
def what_round():
    if (Single_Jeopardy.Category.count() > Double_Jeopardy.Category.count()):
        if (Single_Jeopardy.Category.count() > Final_Jeopardy.Category.count()):
             print("This type of category appears more in the Jeopardy! round.") 
        else:
             print("This type of category appears more in the Final Jeopardy! round.")
    elif (Final_Jeopardy.Category.count() > Double_Jeopardy.Category.count()):
            print("This type of category appears more in the Final Jeopardy! round.")
    else:
         print("This type of category appears more in the Double Jeopardy! round.")

#Calling the what_round() to discover in what round our chosen category appears more frequently  
#what_round()

def quiz():
    y_or_n=input("Are you interested to participate in this quiz?\n")
    round = 1
    count = 1
    amount = 0
    answer_ask = ["May I know your answer?\n", "What's the answer?\n", "Ohh, a difficult one...Tell me the answer!\n", "And the answer is...\n"] 
    answer_correct = ["Perfect!!!\n", "You are right!!!\n", "I am sorry but your answer it's correct!\n", "Great, your answer is correct!\n"]
    answer_incorrect =["I am sorry, but it's the wrong answer\n", "We have to stop, the answer is incorrect\n", "I am so sorry, you were a good Jeopardian\n"]
    while (y_or_n == 'Yes'):
        if(round == 1):
            Jeopardy = round_type("Jeopardy!")
            print("Time for Jeopardy!\n")
            sleep(1)
            print("Let's go for the round number "+str(count)+"\n")
            sleep(0.7)
            print("Here is the question")
            while(count < 3):
                index = random.randint(0, Jeopardy["Show Number"].count())
                question = Jeopardy.Question.iloc[index]
                answer = Jeopardy.Answer.iloc[index]
                print(question)
                print(answer)
                print("")
                sleep(1)
                user_input = input(random.choice(answer_ask))
                if(answer.lower() == user_input.lower()):
                    count += 1
                    print(random.choice(answer_correct))
                    amount += Jeopardy["Float Value List"].iloc[index]
                    print("Your current earnings are "+str(amount)+"$\n")
                else:
                    print(random.choice(answer_incorrect))
                    sleep(1)
                    print("Thank you for participating to Jeopardy!!!\n")
                    sleep(1)
                    print("We are waiting you back!!!")
                    return
                if(count < 3):
                    sleep(1)
                    choice = input("Do you want to continue or you keep the money?\n")
                    while(choice):
                        if(choice == 'Continue'):
                            print("Okay then, let's go for the round number "+str(count)+"\n")
                            break
                        elif(choice == "Keep"):
                            print("Congratulations you are the winner of "+str(amount)+"$")
                            return
                        elif(choice != 'Continue' or choice != 'Keep'):
                            choice = input("Please type 'Continue' or 'Keep'!!!\n") 
            round +=1
        elif(round == 2):
            print("")
            Jeopardy_Double = round_type("Double Jeopardy!")
            saved_amount = amount
            print("Congratulations you have "+str(saved_amount)+"$ saved from the Jeopardy Stage\n")
            sleep(1)
            print("Time for Double Jeopardy!\n")
            sleep(1)
            print("I want to remember that you won't lose your saved amount from the first stage of Jeopardy if you answer wrong in this stage\n")
            print("Let's go for the round number "+str(count)+"\n")
            sleep(0.7)
            print("Here is the question")
            while(count < 5):
                index = random.randint(0, Jeopardy_Double["Show Number"].count())
                question = Jeopardy_Double.Question.iloc[index]
                answer = Jeopardy_Double.Answer.iloc[index]
                print(question)
                print(answer)
                print("")
                sleep(1)
                user_input = input(random.choice(answer_ask))
                if(answer.lower() == user_input.lower()):
                    count += 1
                    print(random.choice(answer_correct))
                    amount += Jeopardy["Float Value List"].iloc[index]
                    print("You just added "+str(amount)+"$ to your earnings\n")
                else:
                    print(random.choice(answer_incorrect))
                    sleep(1)
                    print("Thank you for participating to Jeopardy!!!\n")
                    sleep(1)
                    print("But you go home with your saved money from the first stage.\n")
                    sleep(1)
                    print("That means you won: "+str(saved_amount)+"$\n")
                    print("We are waiting you back!!!")
                    return
                if(count < 5):
                    sleep(1)
                    choice = input("Do you want to continue or you keep the money?\n")
                    while(choice):
                        if(choice == 'Continue'):
                            print("Okay then, let's go for the round number "+str(count)+"\n")
                            break
                        elif(choice == "Keep"):
                            print("Congratulations you are the winner of "+str(amount)+"$")
                            return
                        elif(choice != 'Continue' or choice != 'Keep'):
                            choice = input("Please type 'Continue' or 'Keep'!!!\n")    
            round +=1
        elif(round == 3):
            Jeopardy_Final = round_type("Final Jeopardy!")
            print("Time for Final Jeopardy round!\n")
            sleep(1)
            print("Two more rounds! Will you get your x3 prize?\n")
            sleep(1)
            print("Let's go for the round number "+str(count)+"\n")
            sleep(0.7)
            print("Here is the question")
            while(count < 7):
                index = random.randint(0, 3631)
                question = Jeopardy_Final.Question.iloc[index]
                answer = Jeopardy_Final.Answer.iloc[index]
                print(question)
                print(answer)
                print("")
                sleep(1)
                user_input = input(random.choice(answer_ask))
                if(answer.lower() == user_input.lower()):
                    count += 1
                    print(random.choice(answer_correct))
                    amount += Jeopardy["Float Value List"].iloc[index]
                    print("You just added "+str(amount)+"$ to your earnings\n")
                else:
                    print(random.choice(answer_incorrect))
                    sleep(1)
                    print("Thank you for participating to Jeopardy!!!\n")
                    sleep(1)
                    print("But you go home with your saved money from the first stage.\n")
                    sleep(1)
                    print("That means you won: "+str(saved_amount)+"$\n")
                    print("We are waiting you back!!!")
                    return
                if(count == 6):
                    print("This is the last round!!! If you give the corect answer you will get x3 money!!!\n")
                    print("Good Luck!")
                    sleep(1)
                    choice = input("Do you want to continue to the final round?\n")
                    while(choice):
                        if(choice == 'Continue'):
                            print("Okay then, let's go for the round number "+str(count)+"\n")
                            break
                        elif(choice == "Keep"):
                            print("Congratulations you are the winner of "+str(amount)+"$")
                            return
                        elif(choice != 'Continue' or choice != 'Keep'):
                            choice = input("Please type 'Continue' or 'Keep'!!!\n")
            print("Congratulations you are the winner of the biggest prize!!!\n")
            print("You won: "+str(amount*3)+"$")
            sleep(2)
            print()
            break
quiz()
#print(round_type("Final Jeopardy!")["Question"])


