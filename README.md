## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

You will need to have the following software/technologies:

```
Visual Studio Code/PyCharm Community Edition
Python 3.7.4
Flask
Pandas
```

### Installing

Clone from the group's repository;

```
https://github.com/csc301-fall-2019/paired-assignment-1-otot.git
```

Enter the correct directory;

```
cd paired-assignment-1-otot
```

Open the python file named *api.py* with VS Code/PyCharm.

To run the API code, issue the following command at a command prompt:

```
python api.py
```
The API server should be running on 127.0.0.1:5000 (a.k.a. localhost on port 5000)

URLs are provided down below under the header *Testing URLs* to test the API. Curl or Postman can be used.

# User Stories
##### Resource1
As a casual fan of the NHL, I want data about game results on a given day so I can still keep up to date with how the tournament is going even if I do not watch a lot of the games.
##### Resource2
As a prospective gambler betting on competitions in the NHL, I want data about game statistics of completed games so I can analyze and make predictions to better my odds when betting on which team is going to win the league.
##### Resource3
As a stats junkie of the NHL, I want data about individuals' performance in games so I can analyze and make predictions on the upcoming NHL Draft.

# Acceptance Criterias
##### Resource1
* Ability to specify a given date to provide summaries of game results
* Ability to list every game played on a given date
* For each game played, provide:
    * Names of home/away team
    * Scores for home/away team
    * Outcome of the game
    * Game Type(Regular season/PlayOffs)
    *  Links to retrieve information for both teams
##### Resource2
* Ability to specify a game_id to provide team statistics of completed games
* Ability to list both teams' statistics of a completed game
* For each game played, provide:
    * Number of shots taken by each team
    * Number of goals by each team
    * Number of power play goals
    * Penalty in minutes by home/away team
    * faceOffWinPercentage for each team
    * Coaches for each team
    * Links to retrieve information for both teams and game plays
##### Resource3
* Ability to specify a game_id to provide players' statistics of a game
* Ability to list statistics of players for both teams
* For each game played, provide:
    * Time spent on ice for each player
    * Number of goals shot by an individual
    * Number of assists, blocks achieved for each player
    * Number of power play goals
    * Primary position held for each player
    * Links to retrieve information for both teams and game details

# Resources Descriptions
##### Resource1
An API to query the summaries of game results on a given tournament day. The URL structure is designed in a way such that *results* is a path parameter since the interest here are the game results. Should a client be particularly interested in the game results on a specific day, the URL adds a *date* query parameter which allows them to enter a date. Thus the endpoint is */api/results?date={YYYY-MM-DD}*. The JSON structure implemented is a list of dictionaries with each dictionary representing the summary of each of the game results on a given day. The dictionary each contains properties and their corresponding values that a client might want to know(Team Name, Goals, Team ID, Outcome). Each dictionary also contains a link property which in itself is also a list of three dictionaries which contain a link to other resources with more information about both teams and the team's statistics in the games.
##### Resource2/3
APIs to query the teams' or players' statistics of a completed game. The URL structure is designed in a way such that *results* is a path parameter since the interest here are the game results. To view the teams'(players) statistics of a completed game, we would require a particular game ID, followed by a *teams*/*players* path parameter because we are only interested in the teams(players) that played in this particular game.
* The JSON structure for resource2 is a list of two dictionaries and each dictionary is a representation of a team's statistics in a given game. Each dictionary contains properties and their corresponding values that a client might want to know for a team(Total Shots, Hits, Penalties in Minutes, PowerPlayGoals, etc). Each dictionary also contains a link property which in itself is also a list of three dictionaries each containing a link to other relevant resources containing more information about the team, the team's coach(hypothetical URL),players' statistics and the details about plays of each goal made in this particular game.
* The JSON structure for resource3 is a list of dictionaries and each dictionary is a representation of a player's statistics in a given game. Each dictionary contains properties and their corresponding values that a client might want to know for a player(time on ice, goals, assists, position, etc). Each dictionary also contains a link property that holds a list of dictionaries each containing links to other relevant resources containing more information about the player, player's team and the team's statistics in that game.
##### Resource4
An API to query the summary of each of the goals in a given game. The URL structure is designed in a way such that *results* is a path parameter since the interest here are the game results. Should a client be particularly interested in the specifics of each of the goals of a specific game, the URL adds a *scoringsummary* path parameter because we are only interested in the summary of the goals.  The JSON structure implemented is a list of dictionaries with each dictionary representing the summary of each of the goals in a given game. The dictionary each contains properties and their corresponding values that a client might want to know(Names of Scorers/Assists, period goal was scored in, time during the period it was scored in). Each dictionary also contains a link property which in itself is also a list of dictionaries which each contain a link to other resources with more information about the individuals(Scorers/Assists) involved in that specific goal made that game.

### Design Rationale
1. For the resources, they are mostly implemented in such a way where mostly raw data from the csv file are being provided to them rather than formatting them in such a way that it can be directly presented. This particular implementation was chosen so that clients have the flexibility to format the data to present it however they like. This means that changes in design or the way the data is presented is decoupled with the API. In addition, providing mostly raw data means that there are potentially little to no information loss due to reformatting the information.
2. The links provided in each of the resources can be thought of as a mostly connected and directed graph where each resource is a node and there is always a path from a resource to another. This is to facilitate ease of navigation of the resources, rather than having to type the path again, with regards to related resources. For instance, if a user is looking at the summary of the game results of a particular day (Resource1), they might also be interested in more information about a particular game itself (Resouce2).
3. We chose to merge some of the data frames as it would allow easier access to the information that we required when implementing the resources.

### Trade-Offs
1. For all the resources, we had to join different tables to get the properties we wanted in our JSON structure design. In resource1(games summaries) for example, we had to join games and team info table in order to provide the team names, which would require additional processing. (loading and merging large .csv files)
2. For all the resources, we did not choose to rename most of the columns after reading data from the respective csv files. This means that the properties in our JSON structure uses mostly the same column names as you find in the csv files. Additional columns added such as links are also mostly raw data. This might suggest a reduced reusability for clients when accessing the resources. In addition, the extra work of formatting the data for presentation will be duplicated throughout all the clients.

# Testing URLs
##### Resource1
* Happy Paths:
    * http://127.0.0.1:5000/api/results?date=2011-05-01
    * http://127.0.0.1:5000/api/results?date=2012-06-03
* Fake Paths with Error Handling:
    * http://127.0.0.1:5000/api/results?date=2020-09-06
##### Resource2
* Happy Paths:
    * http://127.0.0.1:5000/api/results/2011030221/teams
    * http://127.0.0.1:5000/api/results/2011030411/teams
* Fake Paths with Error Handling:
    * http://127.0.0.1:5000/api/results/2020090611/teams
##### Resource3
* Happy Paths:
    * http://127.0.0.1:5000/api/results/2011030221/players
    * http://127.0.0.1:5000/api/results/2011030222/players
* Fake Paths with Error Handling:
    * http://127.0.0.1:5000/api/results/2020090221/players
##### Resource4 (Enhancement)
* Happy Paths:
    * http://127.0.0.1:5000/api/results/2011030221/scoringsummary
    * http://127.0.0.1:5000/api/results/2011030222/scoringsummary
* Fake Paths with Error Handling:
    * http://127.0.0.1:5000/api/results/2020090221/scoringsummary
