from flask import Flask, jsonify, abort, request
import pandas as pd
import string

app = Flask(__name__)


# sample code for loading the team_info.csv file into a Pandas data frame.  Repeat as
# necessary for other files
def load_teams_data():
    td = pd.read_csv("./team_info.csv")
    return td

def load_games_data():
    gd = pd.read_csv("./game.csv")
    return gd

def load_game_teams_stats():
    gts = pd.read_csv("./game_teams_stats.csv")
    return gts

def load_game_skater_stats():
    gss = pd.read_csv("./game_skater_stats.csv")
    return gss

def load_player_info():
    pi = pd.read_csv("./player_info.csv")
    return pi

def load_game_plays():
    gp = pd.read_csv("./game_plays.csv")
    return gp

def load_game_plays_players():
    gpp = pd.read_csv("./game_plays_players.csv")
    return gpp

#global variables
team_data = load_teams_data()
print("successfully loaded teams data")

game_data = load_games_data()
print("successfully loaded games data")

game_teams_stats = load_game_teams_stats()
print("successfully loaded game_teams_stats data")

game_skater_stats = load_game_skater_stats()
print("successfully loaded game_skater_stats data")

player_data = load_player_info()
print("successfully loaded player data")

game_plays = load_game_plays()
print("successfully loaded game_plays data")

game_plays_players = load_game_plays_players()
print("successfully loaded game_plays_players data")

@app.route('/')
def index():
    return "NHL API"


# route mapping for HTTP GET on /api/schedule/TOR
@app.route('/api/teams/<string:team_id>', methods=['GET'])
def get_task(team_id):
    # fetch sub dataframe for all teams (hopefully 1) where abbreviation=team_id
    teams = team_data[team_data["abbreviation"] == team_id]

    # return 404 if there isn't one team
    if teams.shape[0] < 1:
        abort(404, "Error Details: Please enter valid abbrevation of the team /api/teams/{team_id} (team_id for 'TORONTORAPTORS' is 'TOR')")

    # get first team
    team = teams.iloc[0]

    # return customized JSON structure in lieu of Pandas Dataframe to_json method
    teamJSON = {"abbreviation": team["abbreviation"],
                "city": team["shortName"],
                "name": team["teamName"]}

    # creation of possible links for the summary (add as required to links_inner)
    links = []
    for i in range(len(teams)):
        links_inner = []
        # Add links here by appending to links_inner
    teamJSON["links"] = links
    # jsonify easly converts maps to JSON strings
    return jsonify(teamJSON)

@app.route('/api/results', methods=['GET'])
def get_summary():

    # getting argument from query string
    args = request.args.get('date')
    # fetch sub dataframe for all games played on the given date_time if any
    games = game_data[game_data["date_time"] == args]

    # return 404 if there isn't any game from that particular date
    if games.shape[0] < 1:
        abort(404, "Error Details: No games on given date, please input another date in the form of /api/results?date={YYYY-MM-DD} (e.g. 2019-09-20)")
    # sub dataframes with required information
    awaysubgames = games[['game_id', 'type', 'away_team_id', 'outcome', 'away_goals', 'home_goals']]
    homesubgames = games[['game_id', 'home_team_id']]
    subteamdata = team_data[['team_id', 'teamName', 'abbreviation']]

    awayteammerge = awaysubgames.merge(subteamdata, left_on='away_team_id', right_on='team_id')
    awayteammergedict = awayteammerge.to_dict('records')

    hometeammerge = homesubgames.merge(subteamdata, left_on='home_team_id', right_on='team_id')

    # creation of possible links (add as required to links_inner)
    links = []
    for i in range(len(games)):
        links_inner = []
        # Add links here by appending to links_inner
        links_inner.append({"href": "/api/teams/{}".format(awayteammerge.iloc[i]["abbreviation"])})
        links_inner.append({"href": "/api/teams/{}".format(hometeammerge.iloc[i]["abbreviation"])})
        links.append(links_inner)

    awayHomeMerge = awayteammerge.merge(hometeammerge, left_on='game_id', right_on='game_id', suffixes=('_away', '_home'))

    # renaming the outcome to be as required in picture
    for j in range(len(awayHomeMerge)):
        awayHomeMerge.at[j, "outcome"] = awayHomeMerge.iloc[j]["outcome"][9:]

    # attaching possible (some hypothetical) links that could be used
    awayHomeMerge["links"] = links
    awayHomeMergedict = awayHomeMerge.to_dict('records')

    return jsonify(awayHomeMergedict)

@app.route('/api/results/<int:game_id>/teams', methods=['GET'])
def get_game_details(game_id):

    # fetch sub dataframe for team stats for the give game_id if any
    twoTeamsData = game_teams_stats[game_teams_stats["game_id"] == game_id]

    # return 404 if there isn't any game with the given game_id
    if twoTeamsData.shape[0] < 1:
        abort(404, "Error Details: No games with given game_id, please input\
                    another game_id in the form /api/results/{ID}/teams ({ID} is a unique identifier for a game}")

    # sub dataframe of team_data consisting of only the columns team_id and abbreviation.
    subteamdata = team_data[['team_id', 'teamName', 'abbreviation']]

    twoTeamsMerge = twoTeamsData.merge(subteamdata, left_on='team_id', right_on='team_id')

    # creation of possible links (add as required to links_inner)
    links = []
    for i in range(len(twoTeamsData)):
        links_inner = []
        # Add links here by appending to links_inner
        links_inner.append({"href": "/api/teams/{}".format(twoTeamsMerge.iloc[i]["abbreviation"])})
        links_inner.append({"href": "/api/teams/{}/coach".format(twoTeamsMerge.iloc[i]["abbreviation"])})
        links_inner.append({"href": "/api/results/{}/teams".format(game_id)})
        links.append(links_inner)

    # attaching possible (some hypothetical) links that could be used
    twoTeamsMerge["links"] = links
    twoTeamsMergeDict = twoTeamsMerge.to_dict('records')

    return jsonify(twoTeamsMergeDict)

@app.route('/api/results/<int:game_id>/players', methods=['GET'])
def get_player_details(game_id):

    # fetch sub dataframe for all the skaters stats for the given game_id if any
    playersData = game_skater_stats[game_skater_stats["game_id"] == game_id]

    # return 404 if there isn't any skater stats with the given game_id
    if playersData.shape[0] < 1:
        abort(404, "Error Details: No skaters stats available with given game_id.\
                    Please input another game_id in the form /api/results/{ID}/players\
                      ({ID} is a unique identifier for a game}")
    # sub dataframes with required information
    teamName = team_data[['team_id', 'teamName', 'abbreviation']]
    playerName = player_data[['player_id', 'firstName', 'primaryPosition']]

    playersDataTN = playersData.merge(teamName, left_on='team_id', right_on='team_id')
    PlayersDataTN_PN = playersDataTN.merge(playerName, left_on='player_id', right_on='player_id')

    # creation of possible links (add as required to links_inner)
    links = []
    for i in range(len(playersData)):
        links_inner = []
        # Add links here by appending to links_inner
        links_inner.append({"href": "/api/teams/{}".format(PlayersDataTN_PN.iloc[i]["abbreviation"])})
        links_inner.append({"href": "/api/players/{}".format(PlayersDataTN_PN.iloc[i]["player_id"])})
        links_inner.append({"href": "/api/results/{}/teams".format(game_id)})
        links.append(links_inner)

    # attaching possible (some hypothetical) links that could be used
    PlayersDataTN_PN["links"] = links
    PlayersDataTN_PNDict = PlayersDataTN_PN.to_dict('records')

    return jsonify(PlayersDataTN_PNDict)



@app.route('/api/results/<int:game_id>/scoringsummary', methods=['GET'])
def get_scoring_summary(game_id):

    # fetch sub dataframe for all the plays in a game for the given game_id if any
    gameplaysData = game_plays[game_plays["game_id"] == game_id]

    # sorts the events to find which play_num results in a goal
    gameplaysDataG = gameplaysData[gameplaysData["event"] == "Goal"]
    gameplaysplayersData = game_plays_players[game_plays_players["game_id"] == game_id]

    # return 404 if there are no games with given game_id
    if gameplaysData.shape[0] < 1:
        abort(404, "Error Details: No games with given game_id, please input another game_id in the form\
                    /api/results/{ID}/scoringsummary  ({ID} is a unique identifier for a game}")
    # return 404 if there are no goals that are scored in the games with given game_id
    if gameplaysDataG.shape[0] < 1:
        abort(404, "Error Details: No goals with given game_id, please input another game_id in the form\
                    /api/results/{ID}/scoringsummary  ({ID} is a unique identifier for a game}")
    # return 404 if there are no data on plays of player in the games with given game_id
    if gameplaysplayersData.shape[0] <1:
        abort(404, "Error Details: No data avaliable on plays of players with given game_id, please input another game_id in the form\
                    /api/results/{ID}/scoringsummary  ({ID} is a unique identifier for a game}")

    # sub dataframes with required information
    gameplaysDataG = gameplaysDataG[["play_num", "period", "periodTime", "goals_away", "goals_home", "event", "description"]]
    playerName = player_data[['player_id', 'firstName', 'lastName']]

    # New columns to add to dataframe
    scorers = []
    assists = []
    links = []
    new_periodTime = []
    # Loops through all the game plays that led to a goal
    for i in range(len(gameplaysDataG)):
        # Setting up data required for each iteration (resetting values)
        periodTime = gameplaysDataG.iloc[i]["periodTime"]
        description = gameplaysDataG.iloc[i]["description"]
        play_num = gameplaysDataG.iloc[i]["play_num"]
        playnumData = gameplaysplayersData[gameplaysplayersData["play_num"] == play_num]
        assist_inner = []
        links_inner = []
        i = description.find(')')
        found = -1
        # Loop to parse the description string to obtain player names and scores
        # and proceed to append it to the relevant list
        while (i != -1):
            if (found == -1):
                name_score = description[:i + 1]
                scorers.append(name_score)
                found = 0
            elif (found == 0):
                j = description.find(':')
                name_score = description[j + 2:i + 1]
                assist_inner.append(name_score)
                found = 1
            else:
                j = description.find(',')
                name_score = description[j + 2:i + 1]
                assist_inner.append(name_score)
                found += 1
            # attaching possible (some hypothetical) links that could be used
            links_inner.append({"href_{}".format(name_score[:-4]).replace(" ", "_"): "/api/players/{}".format(playnumData.iloc[found]["player_id"])})
            description = description[i + 1:]
            i = description.find(')')
        # appending to relevant list
        assists.append(assist_inner)
        links.append(links_inner)
        new_periodTime.append("{:02d}:{:02d}".format(int(periodTime)//60, int(periodTime)%60))

    # Adding new columns to dataframe
    gameplaysDataG["Scorers"] = scorers
    gameplaysDataG["Assists"] = assists
    gameplaysDataG["new_periodTime"] = new_periodTime
    gameplaysDataG["links"] = links
    # Dropping irrelevant columns
    gameplaysDataG.drop(["periodTime", "event", "description", "play_num"], axis = 1, inplace = True)
    gameplaysDataGDict = gameplaysDataG.to_dict("records")

    return jsonify(gameplaysDataGDict)



if __name__ == '__main__':
    app.run(debug=True)
