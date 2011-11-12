if [ $# -ne 1 ]; then
 echo "Usage: `basename $0` {NewExtensionName}"
 exit 65
fi

NEWNAME=$1
NEWNAME_LOWER="`echo $NEWNAME | awk '{print tolower($0)}'`"
echo $NEWNAME_LOWER
mv ckanext/example ckanext/$NEWNAME_LOWER
grep -rl Example * | grep -v `basename $0` | xargs perl -pi -e "s/Example/$NEWNAME/g"
grep -rl example * | grep -v `basename $0` | xargs perl -pi -e "s/example/$NEWNAME_LOWER/g"
cd ..
mv ckanext-example ckanext-$NEWNAME_LOWER
