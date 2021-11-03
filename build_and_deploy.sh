#!/bin/bash

jb build .
ghp-import -n -p -f _build/html
