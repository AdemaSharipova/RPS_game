class SceneManager:
    """
    Scene Manager for easy control scene transitions.
    
    :param: scenes - a list of scenes, that formed in the stack structure.
    Active scene is placed at the end of the stack.
    :param: running - flag indicating if the game is running.
    """
    def __init__(self):
        self.scenes: list = []
        self.running: bool = True

    def push_scene(self, scene) -> None:
        self.scenes.append(scene)

    def pop_scene(self) -> None:
        self.scenes.pop()

    def handle_events(self, events) -> None:
        """
        Handles events by passing them to the active scene (the end of the stack).
        """
        if not self.scenes:
            self.running = False
            return
        self.scenes[-1].handle_events(events)

    def update(self) -> None:
        """
        Updates the active scene
        """
        if not self.scenes:
            self.running = False
            return
        self.scenes[-1].update()

    def render(self, screen) -> None:
        """
        Displays the active scene on the screen
        """
        if not self.scenes:
            self.running = False
            return
        self.scenes[-1].render(screen)


