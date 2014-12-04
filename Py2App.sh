#/bin/bash

cd "$(dirname "$0")"

cd $1

py2applet $2

zip -r9 ../mac/app.zip ${2%.*}.app

rm -r ${2%.*}.app