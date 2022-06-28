from random import shuffle as sh, randint as rd
import copy
import sqlite3

conn = sqlite3.connect('anyone.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM LEADERBOARD')

cursor.execute('DROP TABLE IF EXISTS Qualifiers')

sql = 'CREATE TABLE IF NOT EXISTS Qualifiers( Team Text, GD, PTS, Group_Name TEXT)'
cursor.execute(sql)
cursor.execute('DELETE FROM Qualifiers')


Groups = {'Group A': [], 'Group B': [], 'Group C': [], 'Group D': []}
Qualifiers = []

PremierLeague = ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester City']
LaLiga = ['Atletico Madrid', 'Barcelona', 'Real Madrid', 'Sevilla']
Bundesliga = ['Bayern Leverkusen', 'Bayern Munich', 'Borussia Dortmund', 'RB Liepzig']
SerieA = ['AC Milan', 'Inter Milan', 'Juventus', 'Napoli']

team_list = [PremierLeague, LaLiga, Bundesliga, SerieA]

goalsFor = {}

team_count = 0
for league in team_list:
    for team in league:
        team_count += 1
        goalsFor[team] = 0

goalsAgainst = copy.deepcopy(goalsFor)
goalDifference = copy.deepcopy(goalsFor)
points = copy.deepcopy(goalsFor)
wins = copy.deepcopy(goalsFor)
losses = copy.deepcopy(goalsFor)
draws = copy.deepcopy(goalsFor)

print(f'GF: {goalsFor}')
print(f'GA: {goalsAgainst}')


def team_play_fixtures(group_team):
    while len(group_team) > 0:
        current_team = group_team.pop(0)
        for this_team in group_team:
            print(f'{current_team} vs {this_team}')


def calculate_goals(team1, team2, team1_goals, team2_goals):
    goal_diff = team1_goals - team2_goals

    goalsFor[team1] += team1_goals
    goalsAgainst[team1] += team2_goals
    goalsFor[team2] += team2_goals
    goalsAgainst[team2] += team1_goals
    goalDifference[team1] += goal_diff
    goalDifference[team2] += -goal_diff

    if team1_goals > team2_goals:
        wins[team1] += 1
        losses[team2] += 1
        points[team1] += 3

    elif team2_goals > team1_goals:
        wins[team2] += 1
        losses[team1] += 1
        points[team2] += 3

    else:
        draws[team1] += 1
        draws[team2] += 1
        points[team1] += 1
        points[team2] += 1


def team_play_match_first_leg(group_team):
    while len(group_team) > 0:
        current_team = group_team.pop(0)

        for this_team in group_team:
            home_team = rd(0, 9)
            away_team = rd(0, 9)
            print(f'Match Day 1: {current_team} {home_team} - {away_team} {this_team}')
            calculate_goals(current_team, this_team, home_team, away_team)


def team_play_match_second_leg(group_team):
    while len(group_team) > 0:
        current_team = group_team.pop(0)

        for this_team in group_team:
            home_team = rd(0, 9)
            away_team = rd(0, 9)
            print(f'Match Day 2: {this_team} {home_team} - {away_team} {current_team}')
            calculate_goals(current_team, this_team, home_team, away_team)


def delete_and_create_table(table_name, condition):

    try:
        cursor.execute(f'drop table if exists {table_name}')
        print(f'{table_name} dropped successfully...')

    except:
        print(f'{table_name} not existing')

    sql_query1 = f'''
            CREATE TABLE IF NOT EXISTS {table_name} AS 
            SELECT * FROM LeaderBoard 
            WHERE Group_Name = '{condition}'
            ORDER BY PTS DESC, GD DESC
            LIMIT 2 
            '''
    cursor.execute(sql_query1)
    print(f'{table_name} created successfully...')

    cursor.execute(f'INSERT INTO Qualifiers SELECT Team, GD, PTS, Group_Name FROM {table_name}')


for league in team_list:

    for group in Groups.values():
        sh(league)
        team = league.pop()
        group.append(team)

first_leg_group = copy.deepcopy(Groups)
second_leg_group = copy.deepcopy(Groups)

print('\t----------- First leg ----------- ')
for each_group in first_leg_group.values():
    print(f'\n{each_group}\n')
    team_play_match_first_leg(each_group)

print('\n\t----------- Second leg ----------- ')
for each_group in second_leg_group.values():
    print(f'\n{each_group}\n')
    team_play_match_second_leg(each_group)

print('\n\t\t\t\t\t\t\t\t\t\t\t---------Group Standing----------\n'.upper())

for i, j in Groups.items():

    group_name = i
    beginning = group_name.split(' ')[0]
    where_clause = group_name.replace(' ', f'_{group_name[-1]}_Qualifier')
    where_clause = where_clause[0:len(where_clause) - 1]

    print(f'Group Name is: {group_name}')
    print(
        "\t\t\t\t\t\t\t\t\t\t\t| {:<20} | {:^4} | {:^3} | {:^3} | {:^3} | {:^4} | {:^4} | {:^4} | {:^6} |".format(
            "CLUB", "MP", "W", "D", "L",
            "GF", "GA", "GD", "PTS"))

    for each_team in Groups[i]:
        print("\t\t\t\t\t\t\t\t\t\t\t| {:<20} | {:^4} | {:^3} | {:^3} | {:^3} | {:^4} | {:^4} | {:^4} | {:^6} |".format(
            each_team, 6,
            wins[each_team], draws[each_team], losses[each_team], goalsFor[each_team],
            goalsAgainst[each_team], goalDifference[each_team], points[each_team]))

        sql = f'''insert into LeaderBoard 
        VALUES ('{each_team}', 6,
            {wins[each_team]}, {draws[each_team]}, {losses[each_team]}, {goalsFor[each_team]},
            {goalsAgainst[each_team]}, {goalDifference[each_team]}, {points[each_team]}, '{group_name}')'''
        cursor.execute(sql)
    print("\n")

    delete_and_create_table(where_clause, group_name)

print('Completed successfully...')

# delete_table(table_name, condition)


conn.commit()
conn.close()
