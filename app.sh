while :
do
    data=$(date +%H)
    if [[ $data -ge "06"  && $data -le "18" ]]
    then
        export INSTANCIAS=2
    else
        export INSTANCIAS=30
    fi

    echo $INSTANCIAS
    python main.py  
done;