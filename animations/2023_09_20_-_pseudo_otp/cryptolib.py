# %%manim -qm CircleToSquare
# This code is GPLv3 licensed, copyright Léo Colisson
from manim import *

config.background_color = WHITE

template = TexTemplate()
template.add_to_preamble(r"\usepackage{graphicx}") # provide \scalebox

config.tex_template = template

class CryptoLibrary(VMobject):
    """Call like CryptoLibrary("\mathcal{L}_{\mathsf{right}}", [("function1(arg)", ["code 1", "code 2"])])"""
    def __init__(self, title, global_vars=[], functions=[], scale=1, total_width=5, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)
        self.title_orig = title
        self.functions_orig = functions
        self.global_vars_orig = global_vars
        self.scale_orig = scale
        self.kwargs_orig = kwargs
        self.total_width = total_width
        self.title_tex = MathTex(title)
        self.functions_str = functions
        self.functions = [
            {
                "function_name": MathTex(r"\underline{" + name + r"}"),
                "lines": [
                    {"line": MathTex(l)}
                    for l in lines
                ]
            }
            for (name, lines) in functions
        ]
        self.global_vars = [
            { "line": MathTex(line) }
            for line in global_vars
        ]

        for f in self.functions:
            f["group_lines"] = VGroup(*[l["line"] for l in f["lines"]])
            f["group_function"] = VGroup(f["function_name"], f["group_lines"])
        self.group_global_vars = VGroup(*[line["line"] for line in self.global_vars])
        self.group_functions = VGroup(*[f["group_function"] for f in self.functions])
        self.group_functions_and_global_vars = VGroup(self.group_global_vars, self.group_functions)
        self.group_library_no_background = VGroup(self.title_tex, self.group_functions_and_global_vars)
        self.background_title = Rectangle(color=GREY, stroke_width=0, fill_color=LIGHTER_GRAY, fill_opacity=1)
        self.group_library_no_rect = VGroup(self.group_library_no_background, self.background_title)
        self.surrounding_rect = Rectangle(color=BLACK)
        self.group_library = VGroup(self.group_library_no_rect, self.surrounding_rect)
        self.reset_position()
        self.add(self.group_library)

    def reset_position(self):
        for f in self.functions:
            f["group_lines"].arrange(direction=DOWN, aligned_edge=LEFT)
            f["group_function"].arrange(direction=DOWN, aligned_edge=LEFT)
            f["group_lines"].shift(0.2*RIGHT)
        self.group_functions.arrange(direction=DOWN, aligned_edge=LEFT)
        self.group_functions_and_global_vars.arrange(direction=DOWN, aligned_edge=LEFT)
        self.group_library_no_background.arrange(direction=DOWN, aligned_edge=LEFT)
        console.log("title_tex", self.title_tex)
        if self.title_orig == "":
            self.background_title.stretch_to_fit_height(0).stretch_to_fit_width(self.total_width)
        else:
            self.background_title.surround(
                self.title_tex,
                stretch=True,
                buff=0.5).stretch_to_fit_width(self.total_width,
                                               about_point=self.background_title.get_left()+0.1*RIGHT)
        self.background_title.z_index = -1
        self.surrounding_rect.surround(self.group_library_no_rect,stretch=True,buff=0)
        self.surrounding_rect.stretch_to_fit_height(
            self.surrounding_rect.height+0.25,
            about_point=self.surrounding_rect.get_top()
        )
        self.surrounding_rect.z_index = 1
        self.group_library.scale(self.scale_orig)

    def get_all_function_names_mobj(self):
        return [f["function_name"] for f in self.functions]

    def get_all_lines_mobj(self):
        return [line["line"] for line in self.global_vars] + [line["line"] for f in self.functions for line in f["lines"]]

    def create(self):
        ## TODO: not sure why, the fade in does not appear gradually
        ## Todo: try with Write instead of Create
        return AnimationGroup(*[Write(obj) for obj in self.get_all_function_names_mobj() + self.get_all_lines_mobj() + [self.title_tex]], FadeIn(self.background_title), Create(self.surrounding_rect))

    def place_as_subroutine(self, subroutine_lib):
        """This places subroutine_lib right to the current lib."""
        subroutine_lib.next_to(self, RIGHT, buff=.5)
    
    def new_lib_apply(self, f):
        return CryptoLibrary(f(self.title_orig), [f(l) for l in self.global_vars_orig], [(f(f_name), [f(l) for l in f_lines]) for (f_name, f_lines) in self.functions_orig], self.scale_orig, **self.kwargs_orig)

    def new_lib_replace(self, old_name, new_name):
        return self.new_lib_apply(lambda x: x.replace(old_name, new_name))

    def new_lib_remove(self, match):
        """Create a new lib while removing all lines containing match"""
        return CryptoLibrary(self.title_orig, [l for l in self.global_vars_orig if l.contains(match)], [(f_name, [f(l) for l in f_lines if l.contains(match)]) for (f_name, f_lines) in self.functions_orig], self.scale_orig, **self.kwargs_orig)

    def get_line_or_fct_name_from_content(self, content):
        return [ l for l in self.get_all_lines_mobj() if l.tex_string == content ] + [ l for l in self.get_all_function_names_mobj() if l.tex_string == content ]

    def get_line_or_fct_name_from_content_contains(self, content):
        return [ l for l in self.get_all_lines_mobj() if content in l.tex_string ] + [ l for l in self.get_all_function_names_mobj() if content in l.tex_string ]

    
    def transform_to_cryptolib(self, new_lib, lines_to_match_contains=[], replace_before_match=[]):
        """
        lines_to_match_contains is a list of pairs (line1, line2), where line containing line1 should be turned into the
        lines containing line2. If you are afraid that some other lines might contain your string, add a tex
        comment with a unique string to the string.
        Replace before match is a list of pairs (from_text, to_text), where from_text elements in the original
        string are replaced with to_text, before trying to merge them.
        """
        # list of animations to run
        list_anims = [
            AnimationGroup(Transform(self.surrounding_rect, new_lib.surrounding_rect)),
            AnimationGroup(Transform(self.background_title, new_lib.background_title)),
            AnimationGroup(TransformMatchingTex(self.title_tex, new_lib.title_tex)),
        ]
        # These lines are basically new, so we will just add them manually
        lines_to_manually_add_later = new_lib.get_all_lines_mobj() + new_lib.get_all_function_names_mobj()
        lines_to_manually_remove_later = []
        for l in self.get_all_lines_mobj() + self.get_all_function_names_mobj():
            print("Starting to deal with l", l)
            text_to_match = l.tex_string
            for (from_text, to_text) in replace_before_match:
                text_to_match = text_to_match.replace(from_text, to_text)
            not_found = True
            ## Check if it is
            for (from_line, to_line) in lines_to_match_contains:
                if from_line in text_to_match:
                    to = new_lib.get_line_or_fct_name_from_content_contains(to_line)
                    if len(to) == 1:
                        list_anims += [ AnimationGroup(TransformMatchingTex(l, to[0])) ]
                        print("Before", len(lines_to_manually_add_later))
                        # Not sure why, but list.remove does not work, seems like objects are different.
                        lines_to_manually_add_later = [ x for x in lines_to_manually_add_later if x.tex_string != to[0].tex_string ]
                        print("After", len(lines_to_manually_add_later))
                        not_found = False
                        break # We stop once we found one match.
                    else:
                        raise NameError(f"Error: we expect 1 matching string for string {from_line} but we got {len(to)}.")
            if not_found:
                ## Lines_To_Match_Contains does not contain what we want… let's find them ourselve
                print("Text_to_match is ", text_to_match)
                to = new_lib.get_line_or_fct_name_from_content(text_to_match)
                if len(to) == 1:
                    print("We found it ourself", l, text_to_match, to[0])
                    list_anims += [ AnimationGroup(TransformMatchingTex(l, to[0])) ]
                    # Not sure why, but list.remove does not work, seems like objects are different.
                    lines_to_manually_add_later = [ x for x in lines_to_manually_add_later if x.tex_string != to[0].tex_string ]
                    not_found = False
                elif len(to) > 1:
                    raise NameError(f"Error: we expect 1 matching string for string {l.tex_string} (translated to {text_to_match}) but we got {len(to)}.")
            if not_found:
                print("Not found", l)
                list_anims += [ AnimationGroup(Uncreate(l)) ]
        list_anims += [ AnimationGroup(Create(l)) for l in lines_to_manually_add_later ]
        return AnimationGroup(*list_anims)

    def play_transform_to_cryptolib_rotate(self, new_lib, scene):
        """
        Rotate the library to turn it into new_lib. Due to a bug in Succession, I need to take the scene as input.
        """
        # list of animations to run
        new_lib.rotate(-PI/2, axis=(0,1,0))
        scene.play(Rotate(self, angle=PI/2, axis=(0,1,0),rate_func=rate_functions.ease_in_cubic,run_time=.5))
        scene.play(ReplacementTransform(self, new_lib, run_time=1/60))
        scene.play(Rotate(new_lib, angle=PI/2, axis=(0,1,0), run_time=.5, rate_func=rate_functions.ease_out_cubic))

def transform_cryptolib_lists(old_libs, new_libs, lines_to_match_contains=[], replace_before_match=[], run_time_block=3, move_variables=[]):
    """
    old_libs is a list of libs to start from, new_libs is the list of libs to end up in. If you are afraid that
    some other lines might contain your string, add a tex
    comment with a unique string to the string.
    Replace before match is a list of pairs (from_text, to_text), where from_text elements in the original
    string are replaced with to_text, before trying to merge them.
    move_variables = [(var, line1, line2, pos1, pos2)] will additionally move the pos1-th subterm var in line1 to the pos2-th subterm in line2
    """
    # list of animations to run
    ## debug:
    print("- Old libs:")
    for lib in old_libs:
        for l in lib.get_all_lines_mobj() + lib.get_all_function_names_mobj():
            print(f"We will look for '{l.tex_string}'")
    print("- New libs:")
    for lib in new_libs:
        for l in lib.get_all_lines_mobj() + lib.get_all_function_names_mobj():
            print(f"We will look for '{l.tex_string}'")
    print("---")
    print("min(len(old_libs), len(new_libs)", min(len(old_libs), len(new_libs)))
    number_common_elts = min(len(old_libs), len(new_libs))
    list_anims = sum([
        [
            AnimationGroup(ReplacementTransform(old_libs[i].surrounding_rect, new_libs[i].surrounding_rect, run_time=run_time_block)),
            AnimationGroup(ReplacementTransform(old_libs[i].background_title, new_libs[i].background_title, run_time=run_time_block)),
            AnimationGroup(TransformMatchingTex(old_libs[i].title_tex, new_libs[i].title_tex, run_time=run_time_block)),
        ]
        for i in range(number_common_elts)
    ], [])
    list_anims_after = []
    list_anims_before = []
    # If the two lists have different sizes:
    libs_to_add = []
    libs_to_remove = []
    if len(old_libs) < len(new_libs):
        libs_to_add = new_libs[number_common_elts:]
    elif len(old_libs) > len(new_libs):
        libs_to_remove = old_libs[number_common_elts:]
    for l in libs_to_add:
        list_anims += [
            AnimationGroup(Create(l.surrounding_rect, run_time=run_time_block)),
            AnimationGroup(Create(l.background_title, run_time=run_time_block)),
            AnimationGroup(Write(l.title_tex, run_time=run_time_block)),
        ]
    for l in libs_to_remove:
        list_anims += [
            AnimationGroup(Uncreate(l.surrounding_rect, run_time=run_time_block)),
            AnimationGroup(Uncreate(l.background_title, run_time=run_time_block)),
        ]
        if l.title_orig != "":
            list_anims += [AnimationGroup(Unwrite(l.title_tex, run_time=run_time_block*0.8))]
    # These lines are basically new, so we will just add them manually
    lines_to_manually_add_later = sum([
        new_lib.get_all_lines_mobj() + new_lib.get_all_function_names_mobj()
        for new_lib in new_libs
    ], [])
    lines_to_manually_remove_later = []

    def get_line_or_fct_name_from_content_contains(list_lib, to_line):
        return sum([ l.get_line_or_fct_name_from_content_contains(to_line) for l in list_lib ], [])

    def get_line_or_fct_name_from_content(list_lib, to_line):
        return sum([ l.get_line_or_fct_name_from_content(to_line) for l in list_lib ], [])

    for l in sum([old_lib.get_all_lines_mobj() + old_lib.get_all_function_names_mobj()
                  for old_lib in old_libs], []):
        print("Starting to deal with l", l)
        text_to_match = l.tex_string
        for (from_text, to_text) in replace_before_match:
            text_to_match = text_to_match.replace(from_text, to_text)
        not_found = True
        ## Check if it is
        for (from_line, to_line) in lines_to_match_contains:
            if from_line in text_to_match:
                to = get_line_or_fct_name_from_content_contains(new_libs, to_line)
                if len(to) == 1:
                    list_anims += [ AnimationGroup(TransformMatchingTex(l, to[0], run_time=run_time_block)) ]
                    print("Before", len(lines_to_manually_add_later))
                    # Not sure why, but list.remove does not work, seems like objects are different.
                    lines_to_manually_add_later = [ x for x in lines_to_manually_add_later if x.tex_string != to[0].tex_string ]
                    print("After", len(lines_to_manually_add_later))
                    not_found = False
                    break # We stop once we found one match
                else:
                    raise NameError(f"Error: we expect 1 matching string for string {from_line} but we got {len(to)}.")
        if not_found:
            ## Lines_To_Match_Contains does not contain what we want… let's find them ourselve
            print("Text_to_match is ", text_to_match)
            to = get_line_or_fct_name_from_content(new_libs, text_to_match)
            if len(to) == 1:
                print("We found it ourself", l, text_to_match, to[0])
                list_anims += [ AnimationGroup(TransformMatchingTex(l, to[0], run_time=run_time_block)) ]
                # Not sure why, but list.remove does not work, seems like objects are different.
                lines_to_manually_add_later = [ x for x in lines_to_manually_add_later if x.tex_string != to[0].tex_string ]
                not_found = False
            elif len(to) > 1:
                raise NameError(f"Error: we expect 1 matching string for string {l.tex_string} (translated to {text_to_match}) but we got {len(to)}.")
        if not_found:
            print("Not found", l)
            list_anims += [ AnimationGroup(Unwrite(l, run_time=run_time_block*0.8)) ]
        ## Here we try to move variables between lines that have not been matched
        for (variable, line1, line2, i, j) in move_variables:
            print(f"Tring to find {variable} in {text_to_match}")
            if line1 in text_to_match and variable in text_to_match:
                print(f"We found the line to match variable: {text_to_match}")
                line_to = [ line
                            for line in sum([
                                    new_lib.get_all_lines_mobj() + new_lib.get_all_function_names_mobj()
                                    for new_lib in new_libs], [])
                            if line2 in line.tex_string and variable in line.tex_string ]
                if len(line_to) != 1:
                    raise NameError(f"We expect only one element in the lines matching {line2}, we found {len(line_to)}")
                partsInLine1 = l.get_parts_by_tex(variable)
                if len(partsInLine1) <= i:
                    raise NameError(f"Cannot find {i}-th part {variable} in line 1 {l} (matches: {partsInLine1})")
                partsInLine2 = line_to[0].get_parts_by_tex(variable)
                if len(partsInLine2) <= j:
                    raise NameError(f"Cannot find {j}-th part {variable} in line 2 {line_to} (matches: {partsInLine2})")
                print(f"The parts are {partsInLine1[i].tex_string} and {partsInLine2[j].tex_string}")
                # I tried everything I could think of, even copy both destination and from: it always moves in a weird way, like if we did
                # a replacement transform, even if we only use only the animate one. Guess manim is buggy??
                partFrom = partsInLine1[i].copy()
                partDest = partsInLine2[j].copy() # weird, in my test a copy was needed, but not always??
                print(partsInLine2)
                # list_anims.append(AnimationGroup(ReplacementTransform(partsInLine1[i], partDest, run_time=run_time_block)))
                #list_anims.append(AnimationGroup(partsInLine1[i].animate(run_time=run_time_block).move_to(partDest)))
                list_anims.append(AnimationGroup(partFrom.animate(run_time=run_time_block).move_to(partDest)))
                list_anims_before += [AnimationGroup(Write(partFrom, run_time=1/60))]
                list_anims_after += [AnimationGroup(Unwrite(partFrom, run_time=1/60))]
    list_anims = [ AnimationGroup(Write(l, run_time=run_time_block)) for l in lines_to_manually_add_later ] + list_anims
    return Succession(AnimationGroup(*list_anims_before), AnimationGroup(*list_anims), AnimationGroup(*list_anims_after))
    
