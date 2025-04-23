from manim import *

class AdaBoost(Scene):
    def construct(self):
        # Title
        title = Text("Adaboost Visualization").to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Goal
        goal = Text("Goal: Accurately classify stars and squares", color=GOLD, font_size=40)
        goal.move_to(ORIGIN)
        self.play(Write(goal))
        self.wait(3)

        # Remove Title + Goal
        self.play(FadeOut(title), FadeOut(goal))

        # Creating dots
        shapes = self.create_shapes()
        self.play(FadeIn(shapes))
        self.wait(1)

        # Adding caption
        caption = Text("The shapes represent the training samples", font_size=34).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(5)
        self.play(FadeOut(caption))

        # First weak classifier
        subtitle = Text("Weak Learner #1", color=PURPLE, font_size=34).to_edge(UP)
        self.play(Write(subtitle))
        self.wait(1)
        self.first_weak_learner(shapes)
        self.wait(1)
        self.play(FadeOut(subtitle))
        self.wait(1)

        # Second weak classifier
        subtitle = Text("Weak Learner #2", color=PURPLE, font_size=34).to_edge(UP)
        self.play(Write(subtitle))
        self.wait(1)
        self.second_weak_learner(shapes)
        self.wait(1)
        self.play(FadeOut(subtitle))
        self.wait(1)

        # Third weak classifier
        subtitle = Text("Weak Learner #3", color=PURPLE, font_size=34).to_edge(UP)
        self.play(Write(subtitle))
        self.wait(1)
        self.third_weak_learner(shapes)
        self.wait(1)
        self.play(FadeOut(subtitle))
        self.wait(2)

        # Ensemble classifier
        subtitle = Text("Ensemble Classifier", color=PURPLE, font_size=34).to_edge(UP)
        self.play(Write(subtitle))
        self.wait(1)
        self.ensemble_classifier(shapes)
        self.wait(5)

    def create_shapes(self):
        shapes = VGroup()
        positions = [
            (0, 2), (-2, 1), (0, 0), (-1, -2), (4, 2),
            (-3, -1), (2, 1), (1, -2), (3, -1), (-4, 2)
        ]

        for i, (x, y) in enumerate(positions):
            point = [x, y, 0]

            if i % 2 == 0:
                shape = Star(n=5, outer_radius=0.3).set_fill(GRAY, 1.0).move_to(point).set_stroke(width=0)
                shape.shape_type = "star"
            else:
                shape = Square(side_length=0.5).set_fill(GRAY, 1.0).move_to(point).set_stroke(width=0)
                shape.shape_type = "square"
            shapes.add(shape)
        return shapes

    def first_weak_learner(self, shapes):
        # Creating line
        classifier_line = Line(start=UP * 2.5, end=DOWN * 2.5, color=GOLD).shift(LEFT * 1.5)
        x_pos = -1.5
        
        # Adding line and labels
        square_label = Text("Squares", color=GOLD).scale(0.7).shift(LEFT * 4 + UP * 3)
        star_label = Text("Stars", color=GOLD).scale(0.7).shift(RIGHT * 4 + UP * 3)
        self.play(Create(classifier_line), Write(square_label), Write(star_label))
        self.wait(1)

        # Adding line caption
        caption = Text("Lines represent the current weak learner", font_size=34).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(5)
        self.play(FadeOut(caption))

        # Grouping circles depending on classification
        misclassified_stars = VGroup()
        classified_stars = VGroup()
        misclassified_squares = VGroup()
        classified_squares = VGroup()

        for shape in shapes:
            if shape.get_center()[0] > x_pos:
                if isinstance(shape, Star):
                    classified_stars.add(shape)
                elif isinstance(shape, Square):
                    misclassified_squares.add(shape)
            elif shape.get_center()[0] < x_pos:
                if isinstance(shape, Star):
                    misclassified_stars.add(shape)
                elif isinstance(shape, Square):
                    classified_squares.add(shape)
        
        # Changing color of circles
        self.play(
            FadeToColor(classified_squares, "#24fffb", run_time=1), 
            FadeToColor(classified_stars, "#24fffb", run_time=1)
        )
        self.wait(1)
        self.play(
            FadeToColor(misclassified_squares, "#ff2474", run_time=1), 
            FadeToColor(misclassified_stars, "#ff2474", run_time=1)
        )
        self.wait(1)

        # Adding color captions
        caption_1 = Text("Blue shapes are correctly classified", font_size=30).to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(caption_1))
        self.wait(1)
        caption_2 = Text("Red shapes are incorrectly classified", font_size=30).to_edge(DOWN).shift(DOWN * 0.3)
        self.play(Write(caption_2))
        self.wait(5)
        self.play(FadeOut(caption_1), FadeOut(caption_2))

        # Changing size of circles
        self.play(
            *[star.animate.scale(1.3) for star in misclassified_stars], 
            *[square.animate.scale(1.3) for square in misclassified_squares]
        )
        self.wait(1)
        self.play(
            *[star.animate.scale(0.7) for star in classified_stars], 
            *[square.animate.scale(0.7) for square in classified_squares]
        )
        self.wait(1)

        # Adding size captions
        caption_1 = Text("The size of the shape represents the sample weight", font_size=30).to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(caption_1))
        self.wait(1)
        caption_2 = Text("Misclassified shapes grow, and correctly classified shapes shrink", font_size=30).to_edge(DOWN).shift(DOWN * 0.3)
        self.play(Write(caption_2))
        self.wait(5)
        self.play(FadeOut(caption_1), FadeOut(caption_2))

        # Removing line
        self.play(FadeOut(classifier_line), FadeOut(square_label), FadeOut(star_label))
        self.play(FadeToColor(shapes, GRAY, run_time=1))

    def second_weak_learner(self, shapes): 
        # Classifier caption
        caption = Text("Future weak learners prioritize heavier weights", font_size=34).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(5)
        self.play(FadeOut(caption))

        # Creating line
        classifier_line = Line(start=UP * 2.5, end=DOWN * 2.5, color=GOLD).shift(RIGHT * 2.5)
        x_pos = 2.5
        
        # Adding line and labels
        square_label = Text("Squares", color=GOLD).scale(0.7).shift(LEFT * 4 + UP * 3)
        star_label = Text("Stars", color=GOLD).scale(0.7).shift(RIGHT * 4 + UP * 3)
        self.play(Create(classifier_line), Write(square_label), Write(star_label))
        self.wait(1)

        # Grouping circles depending on classification
        misclassified_stars = VGroup()
        classified_stars = VGroup()
        misclassified_squares = VGroup()
        classified_squares = VGroup()

        for shape in shapes:
            if shape.get_center()[0] > x_pos:
                if isinstance(shape, Star):
                    classified_stars.add(shape)
                elif isinstance(shape, Square):
                    misclassified_squares.add(shape)
            elif shape.get_center()[0] < x_pos:
                if isinstance(shape, Star):
                    misclassified_stars.add(shape)
                elif isinstance(shape, Square):
                    classified_squares.add(shape)
        
        # Changing color of circles
        self.play(
            FadeToColor(classified_squares, "#24fffb", run_time=1), 
            FadeToColor(classified_stars, "#24fffb", run_time=1)
        )
        self.wait(1)
        self.play(
            FadeToColor(misclassified_squares, "#ff2474", run_time=1), 
            FadeToColor(misclassified_stars, "#ff2474", run_time=1)
        )
        self.wait(1)

        # Changing size of circles
        self.play(
            *[star.animate.scale(1.3) for star in misclassified_stars], 
            *[square.animate.scale(1.3) for square in misclassified_squares]
        )
        self.wait(1)
        self.play(
            *[star.animate.scale(0.7) for star in classified_stars], 
            *[square.animate.scale(0.7) for square in classified_squares]
        )
        self.wait(1)

        # Removing line
        self.play(FadeOut(classifier_line), FadeOut(square_label), FadeOut(star_label))
        self.play(FadeToColor(shapes, GRAY, run_time=1))

    def third_weak_learner(self, shapes): 
        # Classifier caption
        caption = Text("Individual weak learners continue to make mistakes...", font_size=34).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(5)
        self.play(FadeOut(caption))

        # Creating line
        classifier_line = Line(start=LEFT * 4, end=RIGHT * 4, color=GOLD).shift(DOWN * 0.5)
        y_pos = -0.5
        
        # Adding line and labels
        star_label = Text("Stars", color=GOLD).scale(0.7).shift(LEFT * 6 + UP)
        square_label = Text("Squares", color=GOLD).scale(0.7).shift(LEFT * 6 + DOWN * 2)
        self.play(Create(classifier_line), Write(square_label), Write(star_label))
        self.wait(1)

        # Grouping circles depending on classification
        misclassified_stars = VGroup()
        classified_stars = VGroup()
        misclassified_squares = VGroup()
        classified_squares = VGroup()

        for shape in shapes:
            if shape.get_center()[1] > y_pos:
                if isinstance(shape, Star):
                    classified_stars.add(shape)
                elif isinstance(shape, Square):
                    misclassified_squares.add(shape)
            elif shape.get_center()[1] < y_pos:
                if isinstance(shape, Star):
                    misclassified_stars.add(shape)
                elif isinstance(shape, Square):
                    classified_squares.add(shape)
        
        # Changing color of circles
        self.play(
            FadeToColor(classified_squares, "#24fffb", run_time=1), 
            FadeToColor(classified_stars, "#24fffb", run_time=1)
        )
        self.wait(1)
        self.play(
            FadeToColor(misclassified_squares, "#ff2474", run_time=1), 
            FadeToColor(misclassified_stars, "#ff2474", run_time=1)
        )
        self.wait(1)

        # Changing size of circles
        self.play(
            *[star.animate.scale(1.3) for star in misclassified_stars], 
            *[square.animate.scale(1.3) for square in misclassified_squares]
        )
        self.wait(1)
        self.play(
            *[star.animate.scale(0.7) for star in classified_stars], 
            *[square.animate.scale(0.7) for square in classified_squares]
        )
        self.wait(1)

        # Removing line
        self.play(FadeOut(classifier_line), FadeOut(square_label), FadeOut(star_label))
        self.play(FadeToColor(shapes, GRAY, run_time=1))

    def ensemble_classifier(self, shapes): 
        # Resetting sizes of shapes
        self.play(*[
            shape.animate.scale_to_fit_height(0.5)
            for shape in shapes
        ], run_time=2)

        # Classifier caption
        caption = Text("Now, we put the weak learners together", font_size=34).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(5)
        self.play(FadeOut(caption))

        # Creating individual classifier lines
        first_line = Line(start=UP * 2.5, end=DOWN * 2.5, color=GOLD, stroke_width=10).shift(LEFT * 1.5)
        second_line = Line(start=UP * 2.5, end=DOWN * 2.5, color=GOLD, stroke_width=4).shift(RIGHT * 2.5)
        third_line = Line(start=LEFT * 4, end=RIGHT * 4, color=GOLD, stroke_width=10).shift(DOWN * 0.5)

        # Drawing the individual classifier lines
        self.play(Create(first_line))
        self.play(Create(second_line))
        self.play(Create(third_line))

        # Individual classifier explanation
        caption_1 = Text("The width of the line represents how accurate it was", font_size=30).to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(caption_1))
        self.wait(1)
        caption_2 = Text("The thicker the line, the higher the accuracy", font_size=30).to_edge(DOWN).shift(DOWN * 0.3)
        self.play(Write(caption_2))
        self.wait(5)
        self.play(FadeOut(caption_1), FadeOut(caption_2))

        # Fading out the individual lines
        self.play(FadeOut(first_line), FadeOut(second_line), FadeOut(third_line))

        # Creating final line
        classifier_line = VMobject(color=GOLD, stroke_width=6)
        classifier_line.set_points_as_corners([
            LEFT * 1.5 + UP * 2.5,
            LEFT * 1.5 + DOWN * 0.5,
            RIGHT * 1.5 + DOWN * 0.5,
            RIGHT * 1.5 + DOWN * 2.5
        ])

        # Adding line and labels
        square_label = Text("Squares", color=GOLD).scale(0.7).shift(LEFT * 4 + UP * 3)
        star_label = Text("Stars", color=GOLD).scale(0.7).shift(RIGHT * 4 + UP * 3)
        self.play(Create(classifier_line), Write(square_label), Write(star_label))
        self.wait(1)

        # Changing color shapes
        self.play(FadeToColor(shapes, "#24fffb", run_time=1))
        self.wait(1)

        # Final explanation
        caption = Text("The ensemble classifier is incredibly accurate!", font_size=34).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(5)
        self.play(FadeOut(caption))