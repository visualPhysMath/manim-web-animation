from manim import *
import random

class MonteCarloGambling(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        random.seed(7)

        # ----------------------------
        # 設定
        # ----------------------------
        initial_bankroll = 100
        bankroll = initial_bankroll

        base_sequence = [1, 2, 3]
        sequence = base_sequence.copy()

        win_prob = 18 / 37
        n_rounds = 80

        history = [bankroll]
        rounds_data = []

        # ----------------------------
        # モンテカルロ法のシミュレーション
        # ----------------------------
        for i in range(n_rounds):
            if len(sequence) == 0:
                sequence = base_sequence.copy()

            if len(sequence) == 1:
                bet = sequence[0]
            else:
                bet = sequence[0] + sequence[-1]

            # 資金以上は賭けられない
            bet = min(bet, bankroll)

            if bet <= 0:
                break

            win = random.random() < win_prob

            old_sequence = sequence.copy()

            if win:
                bankroll += bet

                if len(sequence) >= 2:
                    sequence = sequence[1:-1]
                else:
                    sequence = []

                result = "WIN"
            else:
                bankroll -= bet
                sequence.append(bet)
                result = "LOSE"

            history.append(bankroll)
            rounds_data.append((i + 1, bet, result, bankroll, old_sequence, sequence.copy()))

            if bankroll <= 0:
                break

        # ----------------------------
        # タイトル
        # ----------------------------
        title = Text("モンテカルロ法は本当に必勝法なのか？", font_size=42)
        subtitle = Text("ルーレットの赤黒でシミュレーション", font_size=26, color=GRAY_B)

        title.to_edge(UP)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)

        # ----------------------------
        # ルール説明
        # ----------------------------
        rule1 = Text("数列を用意する", font_size=30)
        seq_text = MathTex("[1,\\ 2,\\ 3]", font_size=44)

        rule2 = Text("賭け金 = 左端 + 右端", font_size=30)
        bet_formula = MathTex("1 + 3 = 4", font_size=44)

        rule3 = Text("勝ち → 左端と右端を消す", font_size=30)
        rule4 = Text("負け → 賭け金を右端に追加", font_size=30)

        rules = VGroup(rule1, seq_text, rule2, bet_formula, rule3, rule4)
        rules.arrange(DOWN, buff=0.35)
        rules.move_to(ORIGIN)

        self.play(FadeOut(subtitle), FadeIn(rules[0]), Write(rules[1]))
        self.wait(0.8)
        self.play(FadeIn(rules[2]), Write(rules[3]))
        self.wait(0.8)
        self.play(FadeIn(rules[4]))
        self.wait(0.6)
        self.play(FadeIn(rules[5]))
        self.wait(1.5)

        self.play(FadeOut(rules))

        # ----------------------------
        # 画面構成
        # ----------------------------
        capital_label = Text("資金", font_size=28)
        capital_value = Integer(initial_bankroll, font_size=42)
        capital_group = VGroup(capital_label, capital_value).arrange(DOWN)
        capital_group.to_corner(UL)

        round_label = Text("Round", font_size=26)
        round_value = Integer(0, font_size=36)
        round_group = VGroup(round_label, round_value).arrange(DOWN)
        round_group.next_to(capital_group, DOWN, buff=0.6)

        seq_label = Text("現在の数列", font_size=28)
        seq_display = Text("[1, 2, 3]", font_size=34)
        seq_group = VGroup(seq_label, seq_display).arrange(DOWN)
        seq_group.to_edge(UP).shift(DOWN * 1.2)

        bet_label = Text("賭け金", font_size=28)
        bet_value = Integer(0, font_size=42)
        bet_group = VGroup(bet_label, bet_value).arrange(DOWN)
        bet_group.to_corner(UR)

        result_text = Text("", font_size=46)

        # グラフ
        axes = Axes(
            x_range=[0, len(history), 20],
            y_range=[0, max(history) + 40, 50],
            x_length=9,
            y_length=4.5,
            tips=False,
            axis_config={"color": GRAY_B},
        )
        axes.to_edge(DOWN)

        x_label = Text("試行回数", font_size=22).next_to(axes.x_axis, DOWN)
        y_label = Text("資金", font_size=22).next_to(axes.y_axis, LEFT)

        graph_title = Text("資金の推移", font_size=28)
        graph_title.next_to(axes, UP)

        zero_line = axes.plot_line_graph(
            x_values=[0, len(history)],
            y_values=[initial_bankroll, initial_bankroll],
            add_vertex_dots=False,
            line_color=GRAY,
        )

        self.play(
            FadeIn(capital_group),
            FadeIn(round_group),
            FadeIn(seq_group),
            FadeIn(bet_group),
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(graph_title),
            Create(zero_line),
        )

        # ----------------------------
        # シミュレーション表示
        # ----------------------------
        points = [axes.c2p(0, history[0])]
        graph_line = VMobject()
        graph_line.set_points_as_corners(points)
        graph_line.set_stroke(WHITE, width=4)

        self.add(graph_line)

        for idx, data in enumerate(rounds_data):
            r, bet, result, current_bankroll, old_seq, new_seq = data

            round_value_new = Integer(r, font_size=36)
            round_value_new.move_to(round_value)

            capital_value_new = Integer(current_bankroll, font_size=42)
            capital_value_new.move_to(capital_value)

            bet_value_new = Integer(bet, font_size=42)
            bet_value_new.move_to(bet_value)

            new_seq_text = Text(str(new_seq), font_size=34)
            new_seq_text.move_to(seq_display)

            if result == "WIN":
                result_text_new = Text("WIN", font_size=46, color=GREEN)
            else:
                result_text_new = Text("LOSE", font_size=46, color=RED)

            result_text_new.move_to(ORIGIN + UP * 0.4)

            new_point = axes.c2p(r, current_bankroll)
            points.append(new_point)

            new_graph_line = VMobject()
            new_graph_line.set_points_as_corners(points)
            new_graph_line.set_stroke(WHITE, width=4)

            dot = Dot(new_point, radius=0.05, color=YELLOW)

            self.play(
                Transform(round_value, round_value_new),
                Transform(capital_value, capital_value_new),
                Transform(bet_value, bet_value_new),
                Transform(seq_display, new_seq_text),
                FadeIn(result_text_new, scale=1.2),
                Transform(graph_line, new_graph_line),
                FadeIn(dot),
                run_time=0.18,
            )

            self.play(FadeOut(result_text_new), run_time=0.08)

            if current_bankroll <= 0:
                break

        self.wait(0.8)

        # ----------------------------
        # 結論
        # ----------------------------
        final_bankroll = history[-1]

        if final_bankroll > initial_bankroll:
            conclusion_main = Text("今回は増えた", font_size=42, color=GREEN)
        elif final_bankroll < initial_bankroll:
            conclusion_main = Text("今回は減った", font_size=42, color=RED)
        else:
            conclusion_main = Text("今回は変わらなかった", font_size=42)

        conclusion_sub = Text(
            "しかし、勝率が 1/2 未満なら長期的には不利",
            font_size=30,
            color=YELLOW,
        )

        conclusion_sub2 = Text(
            "賭け方を変えても、期待値そのものは改善しない",
            font_size=28,
            color=GRAY_B,
        )

        conclusion = VGroup(conclusion_main, conclusion_sub, conclusion_sub2)
        conclusion.arrange(DOWN, buff=0.4)
        conclusion.move_to(ORIGIN)

        background_rect = Rectangle(
            width=13,
            height=3.5,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_opacity=0,
        )
        background_rect.move_to(conclusion)

        self.play(FadeIn(background_rect), FadeIn(conclusion))
        self.wait(3)