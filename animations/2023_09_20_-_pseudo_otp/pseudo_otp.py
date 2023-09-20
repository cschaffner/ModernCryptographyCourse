# Needs manim, if you have nix just run "nix-shell -p manim"
# Compile with
# - low quality (faster render): manim -pql 2023_09_19_-_pseudo_otp.py Demo
# - high quality: manim -pqh 2023_09_19_-_pseudo_otp.py Demo
# - high quality, less fps: manim -pqh 2023_09_19_-_pseudo_otp.py --fps 24 Demo
from manim import *

from cryptolib import *

def print_text(scene, old_text, text, wait_time=1,scale=1,minipage_width="8cm",buff=.5):
    myBaseTemplate = TexTemplate(
        documentclass="\documentclass[preview]{standalone}"
    )
    myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

    currentText = Tex(r"{" + minipage_width + r"}\justifying{" +text + r"}", tex_template=myBaseTemplate, tex_environment="minipage").scale(scale).align_on_border(UP, buff=.5)
    if old_text:
        scene.play(ReplacementTransform(old_text, currentText))
    else:
        scene.play(Write(currentText))
    scene.wait(wait_time)
    return currentText


## Note: TransformMatchingShapes does work, but is a bit weird to use as it will do weird matches, like
## the parens might move to other lines.
# See also TransformMatchingShapes
class Demo(ThreeDScene):
    def construct(self):
        Mobject.set_default(color=BLACK)
        #MathTex.set_default(tex_template=template)
        #### Initial library
        lastText = print_text(self, None, "We consider this encryption library:")
        
        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{ots-L}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{k \leftarrow}} \mathsf{pOTP.KeyGen}(1^\lambda)",
                     r"{{c :=}} \mathsf{pOTP.Enc}({{k}}, {{m_L}})",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to((0,0,0)).shift(LEFT)
        self.play(currentLib.create())
        self.wait(2)
        oldLib = currentLib

        lastText = print_text(self, lastText, "We can unfold the definition of pOTP:")
        
        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{hybrid-1}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{k \leftarrow}} \{0,1\}^\lambda",
                     r"{{c :=}} G({{k}}) {{\oplus}} {{m_L}}",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        self.play(transform_cryptolib_lists([oldLib], [currentLib],
                                            lines_to_match_contains=[
                                                (r"c :=", r"c :="),
                                                (r"k \leftarrow", r"k \leftarrow"),
                                            ]))
        self.wait(2)
        oldLib = currentLib

        ## Like the previous lib, but be need to group elements differently: {{G(k)}} instead of G({{k}})
        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{hybrid-1}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{k \leftarrow}} \{0,1\}^\lambda",
                     r"{{c :=}} {{G(k)}} {{\oplus}} {{m_L}}",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        self.play(ReplacementTransform(oldLib,currentLib), run_time=1/60)
        oldLib = currentLib

        
        lastText = print_text(self, lastText, "We can factor out the computation of G(s):")
        
        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{hybrid-2}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{z \leftarrow}} \textsc{query}()",
                     r"{{c :=}} z {{\oplus}} {{m_L}}",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        currentLibAux = CryptoLibrary(
            title=r"\mathcal{L}^{G}_{\mathsf{prg-real}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{query}()",
                 [
                     r"{{k \leftarrow}} \{0,1\}^\lambda",
                     r"\mathsf{return}\ {{G(k)}}",
                 ]),
            ],
            scale=.8,
            total_width=6,
        )
        currentLib.place_as_subroutine(currentLibAux)
        self.play(transform_cryptolib_lists([oldLib], [currentLib, currentLibAux],
                                            lines_to_match_contains=[
                                                (r"c :=", r"c :="),
                                                # (r"k \leftarrow", r"k \leftarrow"),
                                            ],
                                            move_variables=[
                                                ("G(k)", "", "", 0, 0)
                                            ]))
        self.wait(2)
        oldLib = currentLib
        oldLibAux = currentLibAux

        ## change the grouping
        currentLibAux = CryptoLibrary(
            title=r"\mathcal{L}^{G}_{\mathsf{prg-real}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{query}()",
                 [
                     r"{{k}} {{\leftarrow}} {{ \{0,1\} }} ^{{{\lambda}}}",
                     r"{{\mathsf{return}}}\ G({{k}})",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLibAux)
        self.play(ReplacementTransform(oldLibAux,currentLibAux), run_time=1/60)
        oldLibAux = currentLibAux

        
        lastText = print_text(self, lastText, "Since G is a PRG, we can replace $\mathcal{L}_{\mathsf{prg-real}}$ with $\mathcal{L}_{\mathsf{prg-rand}}$:")

        currentLibAux = CryptoLibrary(
            title=r"\mathcal{L}^{G}_{\mathsf{prg-rand}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{query}()",
                 [
                     r"{{z}} \leftarrow {{ \{0,1\} }}^{{{\lambda}}+l}",
                     r"{{\mathsf{return}}}\ {{z}}",
                 ]),
            ],
            scale=.8,
            total_width=6,
        )
        currentLib.place_as_subroutine(currentLibAux)
        ## version 1:
        # self.play(transform_cryptolib_lists([oldLibAux], [currentLibAux],
        #                                     lines_to_match_contains=[
        #                                         (r"return", r"return"),
        #                                         (r"\leftarrow", r"\leftarrow"),
        #                                     ],
        #                                     move_variables=[
        #                                         #("G(k)", "", "", 0, 0)
        #                                     ]))
        ## version 2:
        oldLibAux.play_transform_to_cryptolib_rotate(currentLibAux, self)
        self.wait(2)
        oldLib = currentLib
        oldLibAux = currentLibAux

        lastText = print_text(self, lastText, "We can now merge back the library:")

        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{hybrid-3}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{z}} \leftarrow {{ \{0,1\} }}^{{{\lambda}}+l}",
                     r"{{c :=}} z {{\oplus}} {{m_L}}",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        self.play(transform_cryptolib_lists([oldLib, oldLibAux], [currentLib],
                                            lines_to_match_contains=[
                                            ],
                                            move_variables=[
                                                ("z", r"return", r"\oplus", 0, 0)
                                            ]))
        self.wait(2)
        oldLib = currentLib

        lastText = print_text(self, lastText, "This is now exactly the one-time-pad, so we can change the encrypted message:")
        
        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{hybrid-4}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{z}} \leftarrow {{ \{0,1\} }}^{{{\lambda}}+l}",
                     r"{{c :=}} z {{\oplus}} {{m_R}}",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        self.play(transform_cryptolib_lists([oldLib], [currentLib],
                                            lines_to_match_contains=[
                                                ("\oplus", "\oplus")
                                            ],
                                            move_variables=[
                                            ]))
        self.wait(2)
        oldLib = currentLib

        lastText = print_text(self, lastText, "Now, we play everything backward to reintroduce G!")
        
        lastText = print_text(self, lastText, "So we start with factoring out the sampling of $k$:")

        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{hybrid-5}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"z \leftarrow \textsc{query}()",
                     r"{{c :=}} z {{\oplus}} {{m_R}}",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        currentLibAux = CryptoLibrary(
            title=r"\mathcal{L}^{G}_{\mathsf{prg-rand}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{query}()",
                 [
                     r"{{z}} \leftarrow {{ \{0,1\} }}^{{{\lambda}}+l}",
                     r"{{ \mathsf{return} }} \ z",
                 ]),
            ],
            scale=.8,
            total_width=6,
        )
        currentLib.place_as_subroutine(currentLibAux)
        self.play(transform_cryptolib_lists([oldLib], [currentLib, currentLibAux],
                                            lines_to_match_contains=[
                                            ],
                                            move_variables=[
                                                ("z", r"\oplus", "return", 0, 0)
                                            ]))
        self.wait(2)
        oldLib = currentLib
        oldLibAux = currentLibAux

        lastText = print_text(self, lastText, "Then we use the fact that $G$ is a PRG (reverse direction):")
        
        currentLibAux = CryptoLibrary(
            title=r"\mathcal{L}^{G}_{\mathsf{prg-rand}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{query}()",
                 [
                     r"{{k}} \leftarrow {{ \{0,1\} }} ^{ {{\lambda}} }",
                     r"\mathsf{return}\ {{G(k)}}",
                 ]),
            ],
            scale=.8,
            total_width=6,
        )
        currentLib.place_as_subroutine(currentLibAux)
        # version 1
        # self.play(transform_cryptolib_lists([oldLibAux], [currentLibAux],
        #                                     lines_to_match_contains=[
        #                                         (r"return", r"return"),
        #                                         (r"\leftarrow", r"\leftarrow"),
        #                                     ],
        #                                     move_variables=[
        #                                         #("G(k)", "", "", 0, 0)
        #                                     ]))
        # version 2
        oldLibAux.play_transform_to_cryptolib_rotate(currentLibAux, self)
        self.wait(2)
        oldLibAux = currentLibAux
        
        lastText = print_text(self, lastText, "We inline the definition of $G$:")

        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{hybrid-5}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{k}} \leftarrow {{ \{0,1\} }} ^{ {{\lambda}} }",
                     r"c := {{G(k)}} \oplus {{m_R}}",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        self.play(transform_cryptolib_lists([oldLib, oldLibAux], [currentLib],
                                            lines_to_match_contains=[
                                                ("c :=", "c :=")
                                            ],
                                            move_variables=[
                                                ("G(k)", r"", r"", 0, 0)
                                            ]))
        self.wait(2)
        oldLib = currentLib
        oldLibAux = currentLibAux
        
        
        # currentLib = CryptoLibrary(
        #     title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{ots-R}}",
        #     # global_vars=[r"k \leftarrow \{0,1\}^n"],
        #     functions=[
        #         (r"\textsc{eavesdrop}(m_L, m_R)",
        #          [
        #              r"{{k}} \leftarrow {{ \{0,1\} }} ^{ {{\lambda}} }",
        #              r"c := {{G(k)}} \oplus m_R",
        #              r"\mathsf{return}\ c",
        #          ]),
        #     ],
        #     scale=.8,
        #     total_width=6,
        # ).move_to(oldLib)
        # self.play(transform_cryptolib_lists([oldLib, oldLibAux], [currentLib],
        #                                     lines_to_match_contains=[
        #                                     ],
        #                                     move_variables=[
        #                                         ("G(k)", "", "", 0, 0)
        #                                     ]))
        # self.wait(2)
        # oldLib = currentLib
        # oldLibAux = currentLibAux

        lastText = print_text(self, lastText, "We inline back the pOTP definition:")
        
        currentLib = CryptoLibrary(
            title=r"\mathcal{L}^{\mathsf{pOTP[G]}}_{\mathsf{ots-R}}",
            # global_vars=[r"k \leftarrow \{0,1\}^n"],
            functions=[
                (r"\textsc{eavesdrop}(m_L, m_R)",
                 [
                     r"{{k}} \leftarrow {{\mathsf{pOTP.KeyGen}(1^\lambda)}}",
                     r"{{c :=}} \mathsf{pOTP.Enc}({{k}}, {{m_R}})",
                     r"\mathsf{return}\ c",
                 ]),
            ],
            scale=.8,
            total_width=6,
        ).move_to(oldLib)
        self.play(transform_cryptolib_lists([oldLib], [currentLib],
                                            lines_to_match_contains=[
                                                (r"\leftarrow", r"\leftarrow"),
                                                (r"c :=", r"c :="),
                                            ],
                                            move_variables=[
                                                ## Not sure why it is not automatically detected, while both should be subparts (so the effect is
                                                ## slightly different, but let's not spend too much time on this)
                                                ("m_R", r"\oplus", "pOTP", 0, 0)
                                            ]))
        self.wait(2)
        oldLib = currentLib
        oldLibAux = currentLibAux
        
        lastText = print_text(self, lastText, "Done!", scale=3)
        


class Debug(ThreeDScene):
    def construct(self):
        Mobject.set_default(color=BLACK)
        a = MathTex(r"\mathsf{return}\ G(k)")
        b = MathTex(r"c := G(k) \oplus m_R")
        VGroup(a,b).arrange(DOWN)
        self.play(
            Write(a)
        )
        self.wait(1)
        part1 = a.get_parts_by_tex("G(k)")
        part2 = b.get_parts_by_tex("G(k)")
        self.play(
            Write(b, run_time=3),
            ReplacementTransform(part1, part2, run_time=3)
        )
        self.wait(2)
