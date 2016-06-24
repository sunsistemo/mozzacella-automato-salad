#!/usr/bin/env bash
set -e

git checkout gh-pages
git merge master
./node_modules/.bin/webpack --optimize-minimize
git add -A
git add --force automato.js
git commit -m "update mozzacella-automato-salad"
git push -u origin gh-pages
git checkout master
