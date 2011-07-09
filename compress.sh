#!/bin/bash

D="fa/jquery/resources";
CMD="python compressor.py  -c $HOME/jar/yuicompressor-2.4.2.jar "

for f in $(find $D -mindepth 1 -maxdepth 1 -name "*.css"); do
    $CMD -o $D/min/$(basename $f) -t css $f
done;

for f in $(find $D -mindepth 1 -maxdepth 1 -name "*.js"); do
    $CMD -o $D/min/$(basename $f) -t js $f
done;
