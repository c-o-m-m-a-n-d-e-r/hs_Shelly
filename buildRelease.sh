#!/bin/bash
(cd ../../; python2 ./generator.pyc Shelly utf-8)
markdown2 --extras tables,fenced-code-blocks,strike,target-blank-links doc/log14169.md > release/log14169.html
(cd release; zip -r 14169_Shelly.hslz *)