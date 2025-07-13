#!/bin/bash
ls *.py | xargs -I {} -P 8 nice -n 19 manim -a "{}"
