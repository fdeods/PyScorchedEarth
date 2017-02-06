import unittest
import pygame
from menu.option import Option


def empty_function():
    pass


def return_text(text):
    return text


isCalled = False
def called():
    global isCalled
    isCalled = True


class OptionTestCase(unittest.TestCase):

    def test_option_text(self):
        pygame.init()
        title_font = pygame.font.Font('../assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        self.assertEqual(test.text(), "SCORCHED  EARTH")

    def test_option_text_position(self):
        pygame.init()
        title_font = pygame.font.Font('../assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        self.assertEqual(test.pos, 20)

    def test_option_hovered(self):
        pygame.init()
        title_font = pygame.font.Font('../assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        test.hovered = True
        self.assertEqual(test.hovered, True)

    def test_option_hovered_and_color(self):
        pygame.init()
        title_font = pygame.font.Font('../assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        test.hovered = True
        self.assertEqual(test.get_color(),  (251, 223, 124))
        test.hovered = False
        self.assertEqual(test.get_color(), (0, 0, 0))

    def test_option_select(self):
        global isCalled
        pygame.init()
        title_font = pygame.font.Font('../assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, called, title_font)
        isCalled = False
        test.select()
        self.assertEqual(isCalled, True)


if __name__ == '__main__':
    unittest.main()
