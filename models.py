class Team:
    teams = []
    def __init__(self, id=None, name=None, code=None, flag=None, image=None, country=None):
        self.id = id
        self.name = name
        self.code = code
        self.flag = flag
        self.image = image
        self.country = country
        self.players = []
        self.matches = []
        Team.teams.append(self)
        
    @classmethod
    def get_teams(cls):
        return cls.teams

    def to_dict(self):
        """
        Converts the team data to a dictionary.

        Returns
        -------
        dict
            A dictionary containing the team's data.
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
    def __init__(self, player_id=None, name=None, age=None, height=None, weight=None, hometown=None, photo=None, stats=None):
        self.id = player_id
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

        Returns
        -------
        dict
            A dictionary containing the player's data and statistics.
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