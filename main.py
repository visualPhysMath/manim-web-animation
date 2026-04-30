from manim import *
import numpy as np


class WebAnimation(Scene):
    def construct(self):
        title = Text("Manim Animation", font_size=42)
        title.to_edge(UP)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4,
            tips=False,
        )

        dot = Dot(color=YELLOW)
        path = TracedPath(dot.get_center, stroke_color=BLUE, stroke_width=4)

        def curve(t):
            x = t
            y = np.sin(2 * t)
            return axes.c2p(x, y)

        dot.move_to(curve(-4))

        self.play(FadeIn(title), Create(axes))
        self.add(path, dot)
        self.play(
            MoveAlongPath(dot, ParametricFunction(curve, t_range=[-4, 4])),
            run_time=5,
            rate_func=linear,
        )
        self.play(dot.animate.set_color(RED).scale(1.5), run_time=0.6)
        self.wait(1)
