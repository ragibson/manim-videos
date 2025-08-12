# Rendering a batch in 480p15, 1080p60, and 2160p60 quality in parallel. The final high-quality render needs
# to be in webm format to circumvent some codec restrictions in DaVinci Resolve's Linux release.
(ls *.py | xargs -n 1 nice -n 19 manim -a -ql) &
(sleep 1 && ls *.py | xargs -n 1 nice -n 19 manim -a) &
(sleep 2 && ls *.py | xargs -n 1 nice -n 19 manim -a -qk --format webm) &
wait