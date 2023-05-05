#!/bin/bash

while getopts "trh" arg;do
    case $arg in
        t)
            translate="1";;
        r)
            resources="1";;
        q)
            create_qm_files="1";;
        *)
            echo "-t updates ui.ts file."
            echo "-r updates resources.py file."
            echo "-f create qm files from ts files."
    esac
done

# finding the parent directory
dir=`pwd`
parent_dir=`dirname $dir`


if [ "$translate" == "1" ];then

    # generate ui.ts file 
    pylupdate5 -translate-function ui_tr "$dir/translation_files.pro"
    echo "$dir/locales/ui.ts is generated!"
fi

if [ "$resources" == "1" ];then

    # generate resource.py file
    pyrcc5 resources.qrc -o "$parent_dir/mounzil/gui/resources.py"
    #pyside-rcc -py3 -o "$parent_dir/mounzil/gui/resources.py" resources.qrc

    echo  "$parent_dir/mounzil/gui/resources.py is generated!"
fi

if [ "$create_qm_files" == "1" ];then

    # generate qm files from ts files
    lrelease "$dir/locales/*.ts"
fi
