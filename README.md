Tournament Results
==
A python module using PostgreSQL database to track players and matches in a game, and to pair the players with Swiss system.


#Usage
Install VirtualBox and vagrant as described in Udacity course "Intro to Relational Databases."

Start and enter virtual box.
```
$ vagrant up
$ vagrant ssh
```

Enter Postgresql and include sql file.
```
$ cd /vagrant/tournament
$ psql
vagrant=> \i tournament.sql
```

Import the module in your python file!!
```python
from tournament import *

registerPlayer('Amy')
registerPlayer('Bilbo')
registerPlayer('Carol')
registerPlayer('Dalton')
reportMatch('Amy', 'Bilbo')      # Amy is the winner
reportMatch('Carol', 'Dalton')   # Carol is the winner
swissPairings()
```
