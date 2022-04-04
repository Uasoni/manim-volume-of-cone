from math import gamma
from manim import *

class S1(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-6, 6, 1], y_range=[-6, 6, 1], z_range=[-6, 6, 1])
        axes.get_z_axis().set_opacity(0)
        self.play(Create(axes), run_time=3)
        
        r = ValueTracker(2)
        h = ValueTracker(3)

        lineFunc = lambda x: (r.get_value()/h.get_value())*x
        
        lineGraphed = always_redraw(lambda: axes.plot(lineFunc, color=BLUE_B))

        self.play(Create(lineGraphed))
        dashedLine = always_redraw(lambda: DashedLine(start=axes.c2p(h.get_value(), 0), end=axes.c2p(h.get_value(), lineFunc(h.get_value())), color=YELLOW ))
        self.play(Create(dashedLine))
        self.wait()

        functionLabelAnim = MathTex(r'f(x) =', r'{r', r'x', r'\over', r'h}').set_color_by_tex("r", RED_B).set_color_by_tex("h", GREEN_B).to_corner(UR, buff=1).add_background_rectangle(BLACK, opacity=0.5)
        functionLabel = MathTex(r'f(x) =', r'{r', r'x',  r'\over', r'h}').set_color_by_tex("r", RED_B).set_color_by_tex("h", GREEN_B).to_corner(UR, buff=1).add_background_rectangle(BLACK, opacity=0.5)

        self.play(Create(functionLabelAnim))
        self.add_fixed_in_frame_mobjects(functionLabel)
        self.remove(functionLabelAnim)

        self.wait()

        hScreenTex = MathTex("h", "=").set_color_by_tex("h", GREEN_B).next_to(functionLabel, DOWN).align_to(functionLabel, LEFT).shift(DOWN*4).add_background_rectangle(BLACK, opacity=0.5)
        hScreenNum = always_redraw(lambda: DecimalNumber(h.get_value()).next_to(hScreenTex, RIGHT).add_background_rectangle(BLACK, opacity=0.5))

        rScreenTex = MathTex("r", "=").set_color_by_tex("r", RED_B).next_to(hScreenTex, DOWN, buff=0.4).add_background_rectangle(BLACK, opacity=0.5)
        rScreenNum = always_redraw(lambda: DecimalNumber(r.get_value()).next_to(rScreenTex, RIGHT).add_background_rectangle(BLACK, opacity=0.5))

        hBraces = always_redraw(lambda: Brace(always_redraw(lambda: Line(start=axes.c2p(0, 0), end=axes.c2p(h.get_value(), 0)))).set_color(GREEN_B))
        rBraces = always_redraw(lambda: Brace(always_redraw(lambda: Line(start=axes.c2p(h.get_value(), 0), end=axes.c2p(h.get_value(), r.get_value()))), direction=RIGHT).set_color(RED_B))

        self.play(Create(VGroup(hScreenTex, hScreenNum, rScreenTex, rScreenNum)))
        self.play(Create(VGroup(hBraces, rBraces)))

        self.wait()

        self.play(h.animate.set_value(4))
        self.play(r.animate.set_value(1))

        self.wait()
        self.play(r.animate.set_value(2), h.animate.set_value(3))
        self.wait()

        integralArea = always_redraw(lambda: axes.get_area(lineGraphed, x_range=[0, h.get_value()], color=YELLOW_B, opacity=0.5))

        self.play(FadeIn(integralArea), run_time=1)

        self.play(r.animate.set_value(3), h.animate.set_value(2))
        self.wait()
        self.play(r.animate.set_value(2), h.animate.set_value(3))
        self.wait()

        lineGraphed.shade_in_3d = True
        axes.shade_in_3d = True

        self.play(axes.get_z_axis().animate.set_opacity(1), FadeOut(VGroup(hScreenNum, hScreenTex, rScreenNum, rScreenTex)))

        self.move_camera(phi=PI/4, theta=-PI/4)
        self.begin_ambient_camera_rotation()

        self.wait(1)

        twoDGraphSet = VGroup(lineGraphed, dashedLine, rBraces, hBraces, integralArea)
        t = ValueTracker(0)

        coneSurface = always_redraw(lambda: 
            Surface(lambda u, v: axes.c2p(v, r.get_value()*v*np.cos(u)/h.get_value(), r.get_value()*v*np.sin(u)/h.get_value()),
            u_range=[0, t.get_value()],
            v_range=[0, h.get_value()],
            checkerboard_colors=[YELLOW_B, YELLOW_B],
            stroke_color=YELLOW
            )
        )

        cone = always_redraw(lambda: 
            Cone(
                base_radius=axes.c2p(0, r.get_value())[1],
                height = axes.c2p(h.get_value(), 0)[0],
                direction=LEFT,
                checkerboard_colors=False,
                show_base=True
            ).set_color(YELLOW_B)
        )

        self.add(coneSurface)
        self.play(Rotating(twoDGraphSet, X_AXIS, 2*PI, run_time=3, rate_func=smooth), t.animate(run_time=3, rate_func=smooth).set_value(2*PI))
        self.play(LaggedStart(ReplacementTransform(coneSurface, cone), FadeOut(twoDGraphSet), lag_ratio=0.1))
        self.wait()

        self.play(h.animate.set_value(4), r.animate.set_value(1))
        self.play(h.animate.set_value(1), r.animate.set_value(3))
        self.play(h.animate.set_value(3), r.animate.set_value(2))
        self.wait()
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=PI/4, theta=-PI/4)
        self.wait()

        blackRectangle = Rectangle(color=BLACK, height=2, width=4).set_opacity(1).to_corner(UL, buff=0.7)
        volumeExpression=MathTex(r'V= \pi \int_0^h \left(\frac{rx}{h}\right)^2 dx').add_background_rectangle(BLACK, 0.5).move_to(blackRectangle.get_center())
        self.add_fixed_in_frame_mobjects(blackRectangle)
        self.add_fixed_in_frame_mobjects(volumeExpression)
        self.bring_to_front(blackRectangle)
        self.play(blackRectangle.animate.set_opacity(0))

        self.wait()

class S2(ThreeDScene):
    def construct(self):
        volumeExpressionA=MathTex(r'V= \pi \int_0^h \left(\frac{rx}{h}\right)^2 dx').add_background_rectangle(BLACK, 0.5).shift(UP*3)
        volumeExpression=MathTex(r'V= \pi \int_0^h \left(\frac{rx}{h}\right)^2 dx').add_background_rectangle(BLACK, 0.5).shift(UP*3)

        axes = ThreeDAxes(x_range=[-6, 6, 1], y_range=[-6, 6, 1], z_range=[-6, 6, 1])
        self.play(Create(axes), run_time=3)

        self.play(Create(volumeExpressionA))
        self.add_fixed_orientation_mobjects(volumeExpression)
        self.remove(volumeExpressionA)

        self.wait()
        r = ValueTracker(2)
        dx = ValueTracker(0.5)
        h = ValueTracker(3)
        slice = always_redraw(lambda: Cylinder(radius=axes.c2p(r.get_value())[0], height=axes.c2p(dx.get_value())[0], direction=RIGHT, resolution=(32, 32), checkerboard_colors=False).set_color(BLUE_B))

        self.play(Create(slice), FadeOut(volumeExpression))
        self.wait()
        self.move_camera(phi=PI/2, theta=-PI/4)
        self.wait()

        dxBrace=always_redraw(lambda: Brace(always_redraw(lambda: Line(start=axes.c2p(0-(dx.get_value()/2), r.get_value(), 0), end=axes.c2p(0+(dx.get_value()/2), r.get_value(), 0)  )), direction=Y_AXIS ).set_color(GREEN_B))
        rBrace=always_redraw(lambda: Brace(always_redraw(lambda: Line(start=axes.c2p(0+(dx.get_value()/2), r.get_value(), 0), end=axes.c2p(0+(dx.get_value()/2), -r.get_value(), 0)  )), direction=X_AXIS ).set_color(RED_B))

        self.move_camera(phi=0, theta=-PI/2)

        self.play(Create(VGroup(dxBrace, rBrace)))
        self.wait()


        cylinderVol=MathTex(r'V_c = \pi', r'r^2', r'h').set_color_by_tex('r', RED_B).set_color_by_tex('h', GREEN_B).shift(UP*3).add_background_rectangle(BLACK, 0.5)
        cylinderVolwDX=MathTex(r'V_c = \pi', r'r^2', r'\Delta x').set_color_by_tex('r', RED_B).set_color_by_tex('dx', GREEN_B).shift(UP*3).add_background_rectangle(BLACK, 0.5)
        cylinderVolLabel=Text('"Volume of Cylinder"').set_color_by_gradient(GREEN_B, RED_B).scale(0.7).shift(DOWN*3)
        self.play(Create(cylinderVol))
        self.wait()
        self.play(ReplacementTransform(cylinderVol, cylinderVolwDX))
        self.play(Write(cylinderVolLabel))
        self.wait()
        self.play(r.animate.set_value(3))
        self.play(r.animate.set_value(2))
        self.play(dx.animate.set_value(0.2))
        self.play(dx.animate.set_value(0.5))

        self.play(FadeOut(VGroup(dxBrace, rBrace, slice)))
        self.wait()
        
        lineFunc = lambda x: (r.get_value()/h.get_value())*x
        
        lineGraphed = always_redraw(lambda: axes.plot(lineFunc, color=BLUE_B))
        dashedLine = always_redraw(lambda: DashedLine(start=axes.c2p(h.get_value(), 0), end=axes.c2p(h.get_value(), lineFunc(h.get_value())), color=YELLOW ))

        self.play(LaggedStart(FadeOut(VGroup(cylinderVol, cylinderVolwDX, cylinderVolLabel)), Create(VGroup(lineGraphed, dashedLine)), lag_ratio=0.3))

        self.wait()

        dxRectanglesLst = [0.5, 0.2, 0.1, 0.05, 0.025]

        sliceUnderLine = VGroup(*[
            axes.get_riemann_rectangles(
                graph=lineGraphed,
                x_range=[0, h.get_value()],
                stroke_width=0,
                stroke_color=WHITE,
                dx=dxRectangles
            ) for dxRectangles in dxRectanglesLst
            ])

        definiteSum = MathTex(r'V \approx \sum_{k=0}^{h} \pi \left(\frac{rx}{h}\right)^2 \Delta x').shift(UP*3).add_background_rectangle(BLACK, 0.5)
        definiteSumSubbed = MathTex(r'V \approx \sum_{k=0}^{h} \pi \frac{r^2x^2}{h^2} \Delta x').shift(UP*3).add_background_rectangle(BLACK, 0.5)

        firstRec = sliceUnderLine[0]
        self.play(Create(VGroup(firstRec, definiteSum)))
        self.wait()
        self.play(ReplacementTransform(definiteSum, definiteSumSubbed))
        self.wait()

        for i in range(1, len(dxRectanglesLst)):
            newRec = sliceUnderLine[i]
            self.play(Transform(firstRec, newRec))
            self.wait()

        indefiniteSum = MathTex(r'V = \lim_{n \to \infty} \sum_{k=0}^{h} \pi\frac{r^2x^2}{h^2} \Delta x').shift(UP*3).add_background_rectangle(BLACK, 0.5)
        integral = MathTex(r'V= \pi \int_0^h \left(\frac{rx}{h}\right)^2 dx').shift(UP*3).add_background_rectangle(BLACK, 0.5)

        self.play(ReplacementTransform(definiteSumSubbed, indefiniteSum))
        self.wait()
        self.play(ReplacementTransform(indefiniteSum, integral))

        self.play(FadeOut(VGroup(axes, lineGraphed, sliceUnderLine, dashedLine)), integral.animate.scale(2).move_to([0, 0, 0]))
        self.wait()
        self.play(Circumscribe(integral, color=BLUE_B))
        self.wait()

        #TODO: Show dimentions on the rectangles and add extra steps to make the derivation easier to understand.

class S3(Scene):
    def construct(self):
        integralT = MathTex(r'V= \pi \int_0^h \left(\frac{rx}{h}\right)^2 dx').to_corner(UL, buff=0.5)
        integral = MathTex(r'V= \pi \int_0^h \left(\frac{rx}{h}\right)^2 dx').to_corner(UL, buff=0.5)

        self.play(Write(integralT))
        self.add(integral)
        self.wait()

        step1T = MathTex(r'= \pi \int_0^h \frac{(rx)^2}{h^2} dx').next_to(integral, RIGHT)
        step1 = MathTex(r'= \pi \int_0^h \frac{(rx)^2}{h^2} dx').next_to(integral, RIGHT)
        self.play(ReplacementTransform(integralT, step1T))
        self.add(step1)
        self.wait()

        step2T = MathTex(r'= \pi \frac{r^2}{h^2} \int_0^h x^2 dx').next_to(step1, DOWN).align_to(step1, LEFT)
        step2 = MathTex(r'= \pi \frac{r^2}{h^2} \int_0^h x^2 dx').next_to(step1, DOWN).align_to(step1, LEFT)
        self.play(ReplacementTransform(step1T, step2T))
        self.add(step2)
        self.wait()

        step3T = MathTex(r'= \pi \frac{r^2}{h^2} \Big[ \frac{x^3}{3} \Big]_0^h').next_to(step2, DOWN).align_to(step2, LEFT)
        step3 = MathTex(r'= \pi \frac{r^2}{h^2} \Big[ \frac{x^3}{3} \Big]_0^h').next_to(step2, DOWN).align_to(step2, LEFT)
        self.play(ReplacementTransform(step2T, step3T))
        self.add(step3)
        self.wait()

        step4T = MathTex(r'= \pi \frac{r^2}{h^2} \frac{h^3}{3}').next_to(step3, DOWN).align_to(step3, LEFT)
        step4 = MathTex(r'= \pi \frac{r^2}{h^2} \frac{h^3}{3}').next_to(step3, DOWN).align_to(step3, LEFT)
        self.play(ReplacementTransform(step3T, step4T))
        self.add(step4)
        self.wait()

        step5T = MathTex(r'= \pi \frac{r^2 h}{3}').next_to(step4, DOWN).align_to(step4, LEFT)
        self.play(ReplacementTransform(step4T, step5T))
        self.wait()

        self.play(FadeOut(VGroup(integralT, integral, step1T, step1, step2T, step2, step3T, step3, step4T, step4)), step5T.animate.scale(2).move_to(ORIGIN))
        self.play(Circumscribe(step5T, color=BLUE, fade_out=True, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER))
        self.wait()

#py -3.10-64 -m manim -pqk conevolume.py
#33 Animations in S1
#42 Animations in S2
#15 Animations in S3
