while :
do
    data=$(date +%H)
    if [[ $data -ge "06"  && $data -le "18" ]]
    then
        export INSTANCIAS=2
    else
        export INSTANCIAS=10
    fi

    echo Iniciando $INSTANCIAS instancias paralelas
    newrelic-admin run-python main.py  
done;