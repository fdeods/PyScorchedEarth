import particleEffect, particles, sys, pygame
from game_core import main

class Option:
    hovered = False

    def __init__(self, text, pos, func, font=0):
        self.text = text
        self.pos = pos
        self.func = func
        if (font != 0):
            self.font = font
        else:
            self.font = menu_font
        self.set_rect()
        self.draw()

    def select(self):
        self.func()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (251, 223, 124)
        else:
            return (0, 0, 0)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.center = (int((width / 2)), int(height / 2))
        self.rect.top = self.pos

effectLength = 1200
effectTimeTable = ((3030, 3030+effectLength), (7230, 7230+effectLength), (11150, 11150+effectLength), (15250, 15250+effectLength), (19250, 19250+effectLength-200))
effectTimeMin = effectTimeTable[0][0]
effectTimeMax = effectTimeTable[len(effectTimeTable)-1][1]
def isEffect (musicPos):
    if (musicPos < effectTimeMin):
        return False
    if (musicPos > effectTimeMax):
        return True
    for effect in effectTimeTable:
        if (effect[0] <= musicPos <= effect[1]):
            return True
    return False

def emptyFunc ():
    pass

if __name__ == '__main__':
    size = width, height = 1600 , 800
    screen = pygame.display.set_mode(size)
    bg = pygame.image.load("background.jpg")
    bg = pygame.transform.scale(bg, size)
    light = pygame.image.load('circle.png')

    pygame.init()
    menu_font = pygame.font.Font('font.ttf', 30)
    title_font = pygame.font.Font('font.ttf', 80)
    first, space = 250, 50
    options = [
        Option("SCORCHED EARTCH", 20, emptyFunc, title_font),
        Option("NEW GAME", (first), main.game_loop),
        Option("OPTIONS", (first + space), emptyFunc),
        Option("EXIT", (first + (space * 2)), sys.exit)
    ]

    clock = pygame.time.Clock()
    test = particleEffect.ParticleEffect(screen, (0, 0), (width, height))
    testgrav = test.CreatePointGravity(strength = -5, pos = (width/2, height/2 + 100))

    testsource = test.CreateSource((-10, -10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.5, particlesperframe = 5, particlelife = 75, drawtype = particles.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(50, colour = (3, 74, 236), length = 10.0)
    testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
    testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)

    testsource = test.CreateSource((width + 10, 0), initspeed = 5.0, initdirection = 4.15619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.5, particlesperframe = 5, particlelife = 75, drawtype = particles.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(50, colour = (3, 74, 236), length = 10.0)
    testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
    testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)

    pygame.mixer.music.load('backgroundMenuMusic.mp3')
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if event.type == pygame.MOUSEBUTTONUP:
            # 	pos = pygame.mouse.get_pos()
            #
            # 	# get a list of all sprites that are under the mouse cursor
            # 	clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]
            # do something with the clicked sprites...

        screen.blit(bg, (0, 0))
        test.Update()
        test.Redraw()
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        option.select()
            else:
                option.hovered = False
            option.draw()

        if (not isEffect(pygame.mixer.music.get_pos())):
            filter = pygame.surface.Surface((width, height))
            filter.fill(pygame.color.Color('White'))
            filter.blit(light, tuple(map(lambda x: x - 50, pygame.mouse.get_pos())))
            screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            pygame.display.flip()

        pygame.display.update()
