class Team:
    teams = []
    def __init__(self, id=None, name=None, code=None, flag=None, image=None, country=None, players=[], matches=[]):
        self.id = id
        self.name = name
        self.code = code
        self.flag = flag
        self.image = image
        self.country = country
        self.players = players
        self.matches = matches
        Team.teams.append(self)
        
    @classmethod
    def get_teams(cls):
        return cls.teams

    def to_dict(self):
        """
        Converts the team data to a dictionary.

        Returns: 
            dict: A dictionary containing the team's data.
        """
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "flag": self.flag,
            "image": self.image,
            "country": self.country,
            "players": [player.to_dict() for player in self.players],
            "matches": [match.to_dict() for match in self.matches]
        }

    def __repr__(self):
        """Return a string representation of the Passenger instance."""
        return f"Team({self.code})"


class Player:
    players = []
    def __init__(self, id=None, name=None, age=None, height=None, weight=None, hometown=None, photo=None, stats=None):
        self.id = id
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.hometown = hometown
        self.photo = photo
        self.stats = stats or {}
        Player.players.append(self)

    def to_dict(self):
        """
        Converts the player data to a dictionary.

        Returns:
            dict: A dictionary containing the player's data and statistics.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "hometown": self.hometown,
            "photo": self.photo,
            "stats": self.stats
        }
        
    @classmethod
    def get_players(cls):
        return cls.players
    
    def __repr__(self):
        """Return a string representation of the Passenger instance."""
        return f"Player({self.name})"


class Match:
    matches = []
    
    def __init__(self, id=None, stage=None, date=None, location=None, home={'team': None, 'image': None, 'score': None}, away={'team': None, 'image': None, 'score': None}):
        self.id = id
        self.stage = stage
        self.date = date
        self.location = location
        self.home = home
        self.away = away
        Match.matches.append(self)
    
    @classmethod
    def get_matches(cls):
        return cls.matches

    @classmethod
    def get_matches_by_stage(cls):
        """
        Organizes matches by their stage and returns them in a specific order.
        Returns:
            dict: Matches grouped by stage in the predefined order.
        """
        matches_per_stage = {}
        for match in cls.matches:
            if match.stage not in matches_per_stage:
                matches_per_stage[match.stage] = []
            matches_per_stage[match.stage].append(match)
        ordered_stages = ["Pool A", "Pool B", "Pool C", "Pool D", "Quarter-Final", "Semi-Final", "Bronze Final", "Final"]
        return {stage: matches_per_stage.get(stage, []) for stage in ordered_stages}
    
    @classmethod
    def get_matches_by_team(cls):
        """
        Organizes matches by the teams that played them.
        Returns:
            dict: Matches grouped by team.
        """
        matches_per_team = {}
        for match in cls.matches:
            if match.home['team'] not in matches_per_team:
                matches_per_team[match.home['team']] = []
            matches_per_team[match.home['team']].append(match)
            
            if match.away['team'] not in matches_per_team:
                matches_per_team[match.away['team']] = []
            matches_per_team[match.away['team']].append(match)
        return dict(sorted(matches_per_team.items()))

    def to_dict(self):
        """
        Converts the match data to a dictionary.
        Returns:
            dict: A dictionary containing the match's data.
        """
        return {
            "id": self.id,
            "stage": self.stage,
            "date": self.date,
            "location": self.location,
            "home": self.home,
            "away": self.away,
        }
    
    def __repr__(self):
        """Return a string representation of the Passenger instance."""
        return f"Match({self.date} - {self.location})"