import random

def rollDice(bonus=0, diceType=20, diceAmount=1, playerAdvantage=False, playerDisadvantage=False):
  if playerAdvantage == playerDisadvantage:
    return bonus + sum(random.randint(1, diceType) for _ in range(diceAmount))
  else:
    rolls = [sum(random.randint(1, diceType) for _ in range(diceAmount)) for _ in range(2)]
    return bonus + (max(rolls) if playerAdvantage else min(rolls))

def inquire():
    questions = ["What will the opposing bonus be?", 
                 "What will the opposing dice type be?", 
                 "How many dice will the opponent roll?"]
    """
    questions = ["Does the player have advantage? (y/n)", 
                 "Does the player have disadvantage? (y/n)", 
                 "What will the opposing bonus be?", 
                 "What will the opposing dice type be?", 
                 "How many dice will the opponent roll?"]
    """
    answers = {}

    for question in questions:
        print(question)
        if question.endswith("(y/n)"):
          answers[question] = input().lower() == 'y'
        else:
          answers[question] = int(input())

    return answers

def measure(bonus, answers, reps=100_000):
  beat = sum(1 for _ in range(reps) if rollDice(bonus, 20, 1) # Player roll is assumed to be 1d20+bonus 
                                                >= rollDice(answers["What will the opposing bonus be?"], 
                                                            answers["What will the opposing dice type be?"], 
                                                            answers["How many dice will the opponent roll?"]))
  """
  beat = sum(1 for _ in range(reps) if rollDice(bonus, 
                                                20,  # Dice type is assumed to be 20
                                                1,  # Dice amount is assumed to be 1
                                                answers["Does the player have advantage? (y/n)"], 
                                                answers["Does the player have disadvantage? (y/n)"]) 
                                                >= rollDice(answers["What will the opposing bonus be?"], 
                                                            answers["What will the opposing dice type be?"], 
                                                            answers["How many dice will the opponent roll?"]))
  """
  return beat / reps

def measure_three_checks(bet, bonuses, gambling):
  answers = inquire()
  if gambling: # If true, gambling, if false, pit fighting
    winnings = [-bet, .5*bet, 1.5*bet, 2*bet]
  else:
    winnings = [0, 50, 100, 200]
  success_rates = [measure(bonus, answers) for bonus in bonuses]

  # Calculate expected winnings
  expected_winnings = 0
  for i in range(4):  # for each possible number of successful checks
    prob = 1
    for j in range(3):  # calculate the probability of that number of successful checks
      if j < i:  # success
        prob *= success_rates[j]
      else:  # failure
        prob *= 1 - success_rates[j]
    expected_winnings += prob * winnings[i]

  return expected_winnings

prof = 3 # Proficiency bonus
ex = 2 * prof # Expertise bonus
activity = True # True for gambling, False for pit fighting
bet = 100
bonuses = [4+ex, 4+ex, 4+ex]  # For gambling, it's insight, intimidation, and deception
avg_winnings = measure_three_checks(bet, bonuses, activity)
print(f"The average expected winnings are {avg_winnings}")
