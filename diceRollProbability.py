import random

def rollDice(diceAmount=1, diceType=20, bonus=0, playerAdvantage=False, playerDisadvantage=False):
    if playerAdvantage == playerDisadvantage:
        return bonus + sum(random.randint(1, diceType) for _ in range(diceAmount))
    else:
        rolls = [sum(random.randint(1, diceType) for _ in range(diceAmount)) for _ in range(2)]
        return bonus + (max(rolls) if playerAdvantage else min(rolls))

def parseNotation(notation):
    diceAmount, rest = notation.split('d')
    diceType, bonus = rest.split('+') if '+' in rest else (rest.split('-')[0], '-' + rest.split('-')[1])
    return int(diceAmount), int(diceType), int(bonus)

def measure(bonus, DC, reps=100_000):
    if isinstance(DC, tuple):
        diceAmount, diceType, dc_bonus = DC
        beat = sum(1 for _ in range(reps) if rollDice(1, 20, bonus) >= rollDice(diceAmount, diceType, dc_bonus))
    else:
        beat = sum(1 for _ in range(reps) if rollDice(1, 20, bonus) >= DC)
    return beat / reps

def calculate_winnings(success_rates, winnings):
    expected_winnings = 0
    for i in range(4):
        prob = 1
        for j in range(3):
            if j < i:
                prob *= success_rates[j]
            else:
                prob *= 1 - success_rates[j]
        expected_winnings += prob * winnings[i]

    return expected_winnings

def measure_three_checks(bet, bonuses, activity, DC):
    if activity == 3:
        bet_mapping = {10: 50, 15: 100, 20: 200, 25: 1000}
        bet = bet_mapping.get(DC, 50)
    winnings_mapping = {
        1: [-bet, .5*bet, 1.5*bet, 2*bet],
        2: [0, 50, 100, 200],
        3: [-bet, 0, .5*bet, bet]
    }
    winnings = winnings_mapping.get(activity, [0, 0, 0, 0])
    success_rates = [measure(bonus, DC) for bonus in bonuses]
    return calculate_winnings(success_rates, winnings)

prof = 3
ex = 2 * prof
activity = 1 # 1 = gambling, 2 = drinking, 3 = crime
bonuses = [4+ex, 4+ex, 2+prof]
DC = parseNotation("2d10+5")

# Activity specific values
crimeDC = 20
bet = 100

if activity != 0:
    avg_winnings = measure_three_checks(bet, bonuses, activity, DC if activity != 3 else crimeDC)
else:
    avg_winnings = sum(measure_three_checks(bet, bonuses, act, DC if act != 3 else crimeDC) for act in range(1, 4)) / 3

print(f"The average expected winnings are {avg_winnings}")
