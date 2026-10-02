from style import *
from manim import Scene
class P(Scene):
    def construct(self):
        p=FourPanel(); self.add(p)
        for a in p.highlight([("d","a"),("d","g")]): pass
class C(Scene):
    def construct(self):
        self.add(title_card("2.1","Average and Instantaneous Rates of Change","Unit 2: Differentiation"))
