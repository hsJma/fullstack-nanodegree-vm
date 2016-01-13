#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
from contextlib import contextmanager


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


@contextmanager
def connect_db():
    try:
        conn = connect()
        c = conn.cursor()
        yield (conn, c)

    finally:
        conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with connect_db() as (conn, c):
        c.execute('DELETE from matches;')
        conn.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    with connect_db() as (conn, c):
        c.execute('DELETE from players;')
        conn.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    with connect_db() as (conn, c):
        c.execute('SELECT count(*) from players')
        cnt = int(c.fetchone()[0])
    return cnt



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    with connect_db() as (conn, c):
        name = bleach.clean(name)
        c.execute("INSERT into players (name) values(%s)", (name,))
        conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assignssigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    ans = []
    for player in allPlayers():
        p = int(player[0])
        ans.append((player[0], player[1], getWins(p), getMatches(p)))
    return sorted(ans, key=lambda tup: tup[2], reverse=True)


def allPlayers():
    """Returns a list of all current players id and names.

    Returns:
      A list of tuples containing (id, name):
        id: the player's unique id
        name: the player's full name (as registered)
    """
    with connect_db() as (conn, c):
        c.execute('SELECT * from players')
        players = [(row[0], row[1]) for row in c.fetchall()]
    return players


def getWins(id):
    """Returns the number of matches the player has won
    """
    with connect_db() as (conn, c):
        c.execute('SELECT count(*) from matches where winner = (%s)', (str(id),))
        cnt = int(c.fetchone()[0])
    return cnt


def getMatches(id):
    """ Returns the number of matches the player has played.
    """
    with connect_db() as (conn, c):
        c.execute('SELECT count(*) from matches where winner = (%s) or loser = (%s)', (str(id), str(id)))
        cnt = int(c.fetchone()[0])
    return cnt


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with connect_db() as (conn, c):
        c.execute("INSERT into matches(winner, loser) values(%s, %s)", (winner, loser))
        conn.commit()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ans = []
    standings = playerStandings()
    if countPlayers() % 2 != 0:
        weak = standings[-1]
    else:
        while standings:
            p1 = standings.pop(0)
            p2 = standings.pop(0)
            match = (p1[0], p1[1], p2[0], p2[1])
            ans.append(match)
    return ans
