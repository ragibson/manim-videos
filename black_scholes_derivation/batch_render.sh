# Rendering a batch in 480p15, 1080p60, and 2160p60 quality in parallel. The final high-quality render needs
# Due to codec restrictions in DaVinci Resolve's Linux release, these will eventually need to be converted like so
#   for i in *.mp4; do ffmpeg -i "$i" -vcodec dnxhd -profile:v dnxhr_lb -acodec pcm_s16le -f mov "${i%.*}.mov"; done
(ls *.py | xargs -n 1 nice -n 19 manim -a -ql) &
(sleep 1 && ls *.py | xargs -n 1 nice -n 19 manim -a) &
(sleep 2 && ls *.py | xargs -n 1 nice -n 19 manim -a -qk) &
wait