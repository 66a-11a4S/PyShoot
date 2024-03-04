import pygame


class InputHandler:
    # singleton instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InputHandler, cls).__new__(cls)
            cls.keys = []
            cls.selected_close = False
        return cls._instance

    def update(self):
        self.keys = pygame.key.get_pressed()

        # event のポーリング
        for event in pygame.event.get():
            # X を押してウィンドウを閉じられた
            if event.type == pygame.QUIT:
                self.selected_close = True
