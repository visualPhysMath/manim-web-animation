from manim import *
import random

class MartingaleSimulation(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # =========================
        # パラメータ設定
        # =========================
        INITIAL_BANKROLL = 63     # 初期資金
        BASE_BET = 1              # 基本賭け金
        TABLE_LIMIT = 32          # テーブル上限
        WIN_PROB = 18 / 37        # ヨーロピアンルーレットの赤黒
        MAX_ROUNDS = 40
        RNG_SEED = 7

        random.seed(RNG_SEED)

        # =========================
        # 事前シミュレーション
        # =========================
        bankroll = INITIAL_BANKROLL
        next_bet = BASE_BET
        lose_streak = 0

        history = [bankroll]
        records = []
        stop_reason = None

        for round_no in range(1, MAX_ROUNDS + 1):
            # 次の賭けができないなら終了
            if next_bet > bankroll:
                stop_reason = "Not enough bankroll"
                break
            if next_bet > TABLE_LIMIT:
                stop_reason = "Table limit reached"
                break

            bet = next_bet
            win = random.random() < WIN_PROB

            if win:
                bankroll += bet
                result = "WIN"
                lose_streak = 0
                next_bet = BASE_BET
            else:
                bankroll -= bet
                result = "LOSE"
                lose_streak += 1
                next_bet = bet * 2

            records.append(
                {
                    "round": round_no,
                    "bet": bet,
                    "result": result,
                    "bankroll": bankroll,
                    "next_bet": next_bet,
                    "lose_streak": lose_streak,
                }
            )
            history.append(bankroll)

            if bankroll <= 0:
                stop_reason = "Bankrupt"
                break

        if stop_reason is None:
            stop_reason = "Max rounds reached"

        # =========================
        # タイトルとルール説明
        # =========================
        title = Text("Martingale Betting System", font_size=40, color=WHITE)
        subtitle = Text(
            "Lose -> double the next bet / Win -> reset to base bet",
            font_size=24,
            color=GRAY_B
        )
        title.to_edge(UP)
        subtitle.next_to(title, DOWN, buff=0.2)

        self.play(Write(title), FadeIn(subtitle))
        self.wait(0.8)

        rule1 = Text("Rule 1: Start with bet = 1", font_size=28)
        rule2 = Text("Rule 2: If you lose, double the next bet", font_size=28)
        rule3 = Text("Rule 3: If you win, go back to 1", font_size=28)
        rule4 = Text("Rule 4: Stop if bankroll or table limit blocks you", font_size=28)

        rules = VGroup(rule1, rule2, rule3, rule4).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rules.move_to(ORIGIN)

        self.play(FadeIn(rules, shift=UP))
        self.wait(2)
        self.play(FadeOut(rules), FadeOut(subtitle))

        # =========================
        # 情報表示欄
        # =========================
        def make_row(label_text, value_mob):
            label = Text(label_text, font_size=24, color=GRAY_A)
            row = VGroup(label, value_mob).arrange(RIGHT, buff=0.35)
            row.align_to(label, LEFT)
            return row

        round_value = Integer(0, font_size=30, color=WHITE)
        bankroll_value = Integer(INITIAL_BANKROLL, font_size=30, color=WHITE)
        last_bet_value = Integer(0, font_size=30, color=WHITE)
        next_bet_value = Integer(BASE_BET, font_size=30, color=YELLOW)
        lose_streak_value = Integer(0, font_size=30, color=WHITE)

        result_value = Text("START", font_size=30, color=BLUE_B)

        row1 = make_row("Round", round_value)
        row2 = make_row("Bankroll", bankroll_value)
        row3 = make_row("Last bet", last_bet_value)
        row4 = make_row("Next bet", next_bet_value)
        row5 = make_row("Lose streak", lose_streak_value)
        row6 = make_row("Result", result_value)

        info_panel = VGroup(row1, row2, row3, row4, row5, row6)
        info_panel.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        info_panel.to_corner(UL).shift(DOWN * 0.5)

        # 固定情報
        params = VGroup(
            Text(f"Base bet = {BASE_BET}", font_size=22, color=GRAY_B),
            Text(f"Table limit = {TABLE_LIMIT}", font_size=22, color=GRAY_B),
            Text(f"Win prob = 18/37 ≈ {WIN_PROB:.3f}", font_size=22, color=GRAY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        params.to_corner(UR).shift(DOWN * 0.5)

        # =========================
        # グラフ
        # =========================
        max_x = max(len(records), 10)
        max_y = max(max(history) + 10, INITIAL_BANKROLL + 10, TABLE_LIMIT + 10)

        axes = Axes(
            x_range=[0, max_x, 5],
            y_range=[0, max_y, 10],
            x_length=10,
            y_length=4.3,
            tips=False,
            axis_config={"color": GRAY_B},
        )
        axes.to_edge(DOWN)

        x_label = Text("Round", font_size=22).next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Bankroll", font_size=22).next_to(axes.y_axis, LEFT, buff=0.2)
        graph_title = Text("Bankroll over time", font_size=26).next_to(axes, UP, buff=0.2)

        start_point = axes.c2p(0, INITIAL_BANKROLL)
        line = VMobject(color=WHITE, stroke_width=4)
        line.set_points_as_corners([start_point])

        initial_dot = Dot(start_point, radius=0.05, color=WHITE)

        self.play(
            FadeIn(info_panel),
            FadeIn(params),
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(graph_title),
            FadeIn(initial_dot),
            Create(line),
        )

        # =========================
        # ラウンドごとのアニメーション
        # =========================
        points = [start_point]

        for rec in records:
            # 新しい表示用オブジェクトを作る
            new_round = Integer(rec["round"], font_size=30, color=WHITE).move_to(round_value)
            new_bankroll = Integer(rec["bankroll"], font_size=30, color=WHITE).move_to(bankroll_value)
            new_last_bet = Integer(rec["bet"], font_size=30, color=WHITE).move_to(last_bet_value)
            new_next_bet = Integer(rec["next_bet"], font_size=30, color=YELLOW).move_to(next_bet_value)
            new_lose_streak = Integer(rec["lose_streak"], font_size=30, color=WHITE).move_to(lose_streak_value)

            res_color = GREEN if rec["result"] == "WIN" else RED
            new_result = Text(rec["result"], font_size=30, color=res_color).move_to(result_value)

            # 中央に大きく結果表示
            center_result = Text(rec["result"], font_size=48, color=res_color)
            center_result.move_to(UP * 0.5)

            # グラフ更新
            new_point = axes.c2p(rec["round"], rec["bankroll"])
            points.append(new_point)

            new_line = VMobject(color=WHITE, stroke_width=4)
            new_line.set_points_as_corners(points)

            new_dot = Dot(new_point, radius=0.055, color=YELLOW)

            self.play(
                Transform(round_value, new_round),
                Transform(bankroll_value, new_bankroll),
                Transform(last_bet_value, new_last_bet),
                Transform(next_bet_value, new_next_bet),
                Transform(lose_streak_value, new_lose_streak),
                Transform(result_value, new_result),
                FadeIn(center_result, scale=1.15),
                Transform(line, new_line),
                FadeIn(new_dot),
                run_time=0.45,
            )
            self.play(FadeOut(center_result), run_time=0.2)

        # =========================
        # 終了メッセージ
        # =========================
        if stop_reason == "Bankrupt":
            end_main = Text("Bankrupt", font_size=40, color=RED)
        elif stop_reason == "Not enough bankroll":
            end_main = Text("Cannot continue: bankroll too small", font_size=34, color=RED)
        elif stop_reason == "Table limit reached":
            end_main = Text("Cannot continue: table limit reached", font_size=34, color=RED)
        else:
            end_main = Text("Simulation finished", font_size=40, color=WHITE)

        end_sub1 = Text("Martingale does not change the game's expectation.", font_size=26, color=YELLOW)
        end_sub2 = Text("A losing streak makes the required bet explode exponentially.", font_size=26, color=YELLOW)

        formula1 = MathTex(r"\text{after } n \text{ losses: next bet } = 2^n", font_size=34)
        formula2 = MathTex(r"\text{total loss after } n \text{ losses } = 2^n - 1", font_size=34)

        conclusion = VGroup(end_main, end_sub1, end_sub2, formula1, formula2)
        conclusion.arrange(DOWN, buff=0.25)

        box = SurroundingRectangle(conclusion, color=GRAY_B, buff=0.4)
        box.set_fill(BLACK, opacity=0.9)

        group = VGroup(box, conclusion)
        group.move_to(ORIGIN)

        self.play(FadeIn(box), FadeIn(conclusion))
        self.wait(3)