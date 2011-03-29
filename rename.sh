if [ $# -ne 1 ]; then
 echo "Usage: `basename $0` {NewExtensionName}"
 exit 65
fi

NEWNAME=$1
NEWNAME_LOWER="`echo $NEWNAME | awk '{print tolower($0)}'`"
echo $NEWNAME_LOWER
mv ckanext/exampletheme ckanext/$NEWNAME_LOWER
grep -rl ExampleTheme * | grep -v `basename $0` | xargs perl -pi -e "s/ExampleTheme/$NEWNAME/g"
grep -rl exampletheme * | grep -v `basename $0` | xargs perl -pi -e "s/exampletheme/$NEWNAME_LOWER/g"
cd ..
mv ckanext-exampletheme ckanext-$NEWNAME_LOWER