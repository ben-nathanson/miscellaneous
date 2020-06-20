from time import sleep


def format(d) -> str:
    return str(int(d)).zfill(2)


time_in_minutes = int(input("How many minutes long is your exam?\n"))
number_of_questions = int(input("How many questions are on the exam?"))
if number_of_questions <= 0:
    exit()
if time_in_minutes <= 0:
    exit()
pace = time_in_minutes / number_of_questions
time_remaining = time_in_minutes
question = 1
while time_remaining > 0:
    seconds = time_remaining % 1 * 60
    minutes = time_remaining - (time_remaining % 1)
    print(f"{format(minutes)}:{format(seconds)} remaining.")
    print(f"You should be at question #{question}.")
    question = question + 1
    time_remaining = time_remaining - pace
    sleep(
        pace * 60
    )

print("Congrats.")
