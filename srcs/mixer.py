from pygame import mixer


class Mixer:
    """
    Handles sound playback in the game, including background music and sound effects.
    """

    def __init__(self) -> None:
        # Initialize the pygame mixer for sound playback
        mixer.init()

        # List of soundtrack file paths to be played as background music
        self.soundtracks = [
            "assets/sounds/soundtrack/minecraft.wav",
            "assets/sounds/soundtrack/subwoofer_lullaby.wav",
        ]
        self.current_soundtrack = 0  # Index of the currently selected soundtrack

        # Load and configure the sound effect for harvesting an item
        self.harvest_sound = mixer.Sound("assets/sounds/harvest.wav")
        self.harvest_sound.set_volume(1)  # Set volume to maximum

        # Load and configure the sound effect for placing a block
        self.put_sound = mixer.Sound("assets/sounds/put.wav")
        self.put_sound.set_volume(1)  # Set volume to maximum

    def play_soundtrack(self) -> None:
        """
        Plays the next soundtrack in the list if no music is currently playing.
        Automatically loops through the list of soundtracks.
        """
        if not mixer.music.get_busy():  # Check if music is not currently playing
            # Load and play the current soundtrack
            mixer.music.load(self.soundtracks[self.current_soundtrack])
            mixer.music.play()

            # Move to the next soundtrack (loops back to the first one)
            self.current_soundtrack = (self.current_soundtrack + 1) % len(
                self.soundtracks
            )
