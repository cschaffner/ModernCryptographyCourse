# Animation pseudo OTP

Leo Colisson (leo.colisson@cwi.nl) made a (very young and not yet stable nor properly documented) manim library to generate animations. To generate the animation, install manim (if you have nix, just run `nix-shell -p manim`) and run:

```bash
manim -pqh pseudo_otp.py --fps 24 Demo
```

If you want to debug or improve it, you might prefer the faster low quality version `manim -pql +pseudo_otp.py Demo`. The final video is named [./Demo_24fps.mp4](./Demo_24fps.mp4), but you can directly play the result in a slide-like fashion by opening [this link](https://leo-colisson.github.io/blenderpoint-web/index.html?video=https://raw.githubusercontent.com/cschaffner/ModernCryptographyCourse/master/animations/2023_09_20_-_pseudo_otp/Demo_24fps.mp4).



