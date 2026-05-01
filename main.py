from manim import *
import numpy as np
import random

# 実行例:
# manim -pqh ising_cool.py IsingCoolAnimation
# 軽く確認:
# manim -pql ising_cool.py IsingCoolAnimation


class IsingCoolAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#050505"

        # =====================
        # Parameters
        # =====================
        N = 27
        cell_size = 0.18
        J = 1.0
        frames = 80
        sweeps_per_frame = 3

        # 温度スケジュール
        T_start = 4.0
        T_end = 0.35

        rng = np.random.default_rng(3)
        spins = rng.choice([-1, 1], size=(N, N))

        # =====================
        # Layout
        # =====================
        grid_group = VGroup()
        cells = []

        for i in range(N):
            row = []
            for j in range(N):
                sq = Square(side_length=cell_size)
                x = (j - N / 2) * cell_size
                y = (N / 2 - i) * cell_size
                sq.move_to([x, y, 0])
                sq.set_stroke(width=0)
                sq.set_fill(self.spin_color(spins[i, j]), opacity=0.95)
                row.append(sq)
                grid_group.add(sq)
            cells.append(row)

        grid_group.scale(1.15)
        grid_group.shift(LEFT * 1.9)

        # 外枠
        frame_box = SurroundingRectangle(
            grid_group,
            color=WHITE,
            buff=0.08,
            stroke_width=2
        ).set_opacity(0.7)

        # 数式
        hamiltonian = MathTex(
            r"H = -J \sum_{\langle i,j\rangle} s_i s_j",
            font_size=42
        )
        hamiltonian.to_corner(UR)
        hamiltonian.shift(DOWN * 0.25)
        hamiltonian.set_color(WHITE)

        prob = MathTex(
            r"P = \min \left(1, e^{-\Delta E/T}\right)",
            font_size=36
        )
        prob.next_to(hamiltonian, DOWN, buff=0.35)
        prob.set_color(WHITE)

        # 温度表示
        temp_label = Text("Temperature", font_size=26)
        temp_label.next_to(prob, DOWN, buff=0.55)
        temp_label.align_to(prob, LEFT)

        temp_bar_bg = RoundedRectangle(
            width=3.0,
            height=0.18,
            corner_radius=0.08,
            stroke_color=WHITE,
            stroke_width=1,
        )
        temp_bar_bg.next_to(temp_label, DOWN, buff=0.2)
        temp_bar_bg.align_to(temp_label, LEFT)

        temp_bar = Rectangle(
            width=3.0,
            height=0.18,
            stroke_width=0,
            fill_opacity=1.0,
            fill_color=YELLOW
        )
        temp_bar.move_to(temp_bar_bg.get_center())
        temp_bar.align_to(temp_bar_bg, LEFT)

        temp_value = DecimalNumber(T_start, num_decimal_places=2, font_size=28)
        temp_value.next_to(temp_bar_bg, RIGHT, buff=0.25)
        temp_value.set_color(YELLOW)

        # 磁化率表示
        mag_label = Text("Magnetization", font_size=26)
        mag_label.next_to(temp_bar_bg, DOWN, buff=0.45)
        mag_label.align_to(temp_bar_bg, LEFT)

        mag_value = DecimalNumber(0, num_decimal_places=2, font_size=34)
        mag_value.next_to(mag_label, DOWN, buff=0.15)
        mag_value.align_to(mag_label, LEFT)

        # タイトル
        title = Text("2D Ising Model", font_size=42, weight=BOLD)
        title.to_corner(UL)
        title.shift(RIGHT * 0.3 + DOWN * 0.2)

        subtitle = Text("random spins  →  ordered domains", font_size=24)
        subtitle.next_to(title, DOWN, buff=0.18)
        subtitle.align_to(title, LEFT)
        subtitle.set_opacity(0.75)

        # =====================
        # Opening
        # =====================
        self.play(
            FadeIn(grid_group, scale=0.92),
            Create(frame_box),
            FadeIn(title, shift=DOWN * 0.2),
            FadeIn(subtitle, shift=DOWN * 0.2),
            run_time=1.4
        )

        self.play(
            Write(hamiltonian),
            FadeIn(prob, shift=DOWN * 0.2),
            FadeIn(temp_label),
            Create(temp_bar_bg),
            FadeIn(temp_bar),
            FadeIn(temp_value),
            FadeIn(mag_label),
            FadeIn(mag_value),
            run_time=1.6
        )

        # 粒子っぽい背景エフェクト
        particles = self.make_particles()
        self.add(particles)

        # =====================
        # Main animation
        # =====================
        for frame in range(frames):
            alpha = frame / (frames - 1)
            T = T_start * (1 - alpha) + T_end * alpha

            changed = []

            for _ in range(sweeps_per_frame):
                for _ in range(N * N):
                    i = rng.integers(0, N)
                    j = rng.integers(0, N)

                    dE = self.delta_E(spins, i, j, J)

                    if dE <= 0 or rng.random() < np.exp(-dE / T):
                        spins[i, j] *= -1
                        changed.append((i, j))

            # 色更新
            anims = []

            # 毎フレーム全セルを更新すると重いので、変更セル中心
            unique_changed = list(set(changed))

            for i, j in unique_changed[:250]:
                sq = cells[i][j]
                anims.append(
                    sq.animate.set_fill(self.spin_color(spins[i, j]), opacity=0.95)
                )

            # たまに全体を同期
            if frame % 10 == 0:
                for i in range(N):
                    for j in range(N):
                        cells[i][j].set_fill(self.spin_color(spins[i, j]), opacity=0.95)

            # 温度バー
            bar_width = 3.0 * (T - T_end) / (T_start - T_end)
            bar_width = max(bar_width, 0.04)

            temp_bar.generate_target()
            temp_bar.target.stretch_to_fit_width(bar_width)
            temp_bar.target.align_to(temp_bar_bg, LEFT)
            temp_bar.target.move_to([
                temp_bar_bg.get_left()[0] + bar_width / 2,
                temp_bar_bg.get_center()[1],
                0
            ])

            M = abs(np.mean(spins))

            temp_value.set_value(T)
            mag_value.set_value(M)

            if M < 0.3:
                mag_value.set_color(BLUE)
            elif M < 0.7:
                mag_value.set_color(YELLOW)
            else:
                mag_value.set_color(RED)

            # 臨界温度っぽいところで演出
            extra_anims = []
            if 0.42 < alpha < 0.48 and frame % 2 == 0:
                pulse = SurroundingRectangle(
                    grid_group,
                    color=YELLOW,
                    buff=0.12,
                    stroke_width=4
                )
                pulse.set_opacity(0.8)
                self.add(pulse)
                extra_anims.append(FadeOut(pulse, scale=1.15))

            self.play(
                *anims,
                MoveToTarget(temp_bar),
                *extra_anims,
                run_time=0.055,
                rate_func=linear
            )

        # =====================
        # Final emphasis
        # =====================
        final_text = Text("Symmetry breaks.", font_size=40, weight=BOLD)
        final_text.next_to(mag_value, DOWN, buff=0.55)
        final_text.align_to(mag_label, LEFT)

        glow_box = SurroundingRectangle(
            grid_group,
            color=RED,
            buff=0.10,
            stroke_width=4
        )

        self.play(
            Create(glow_box),
            FadeIn(final_text, shift=UP * 0.2),
            run_time=1.0
        )

        self.play(
            grid_group.animate.scale(1.035),
            glow_box.animate.scale(1.035),
            run_time=0.6,
            rate_func=there_and_back
        )

        self.wait(1.5)

    # =====================
    # Helper functions
    # =====================
    def spin_color(self, s):
        if s == 1:
            return "#ff3b30"  # red
        else:
            return "#2f80ff"  # blue

    def delta_E(self, spins, i, j, J):
        N = spins.shape[0]
        s = spins[i, j]

        nn = (
            spins[(i + 1) % N, j]
            + spins[(i - 1) % N, j]
            + spins[i, (j + 1) % N]
            + spins[i, (j - 1) % N]
        )

        return 2 * J * s * nn

    def make_particles(self):
        particles = VGroup()
        rng = np.random.default_rng(10)

        for _ in range(90):
            dot = Dot(radius=rng.uniform(0.006, 0.018))
            dot.move_to([
                rng.uniform(-7, 7),
                rng.uniform(-4, 4),
                0
            ])
            dot.set_color(WHITE)
            dot.set_opacity(rng.uniform(0.08, 0.22))
            particles.add(dot)

        return particles
