import weakref

class LevelManager:
    _instance = None

    def __init__(self):
        # Only allow initialization once
        if LevelManager._instance is not None:
            return
        self._player_ref = None
        LevelManager._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LevelManager()
        return cls._instance

    def register_player(self, player):
        """Register the player using a weak reference."""
        self._player_ref = weakref.ref(player)

    def deregister_player(self):
        """Remove the player reference."""
        self._player_ref = None

    def get_player(self):
        """Return the player object or None if it no longer exists."""
        return self._player_ref() if self._player_ref else None

    def get_player_position(self):
        """Return the player's local position, or None if player doesn't exist."""
        player = self.get_player()
        if player:
            return player.transform.get_local_position()
        return None

    def get_player_candy(self):
        player_candy = self.get_player().get_component("PlayerCandy")
        if player_candy:
            return weakref.ref(player_candy)
        return None
