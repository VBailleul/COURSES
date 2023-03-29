#!/bin/bash
IFS=$'\n'
cut -f1 donnees_pays.txt | awk ' {if(NR>1) print}' | head -n -1 | awk '{print toupper($0)}'> countries_code.txt
grep -wf countries_code.txt continent_pays.txt | cut -d: -f8 | sort -u > zones.txt

zones=$(cat zones.txt) 

zone=$(yad --form --fixed --width=450 --title "Choisissez une zone continentale" --separator=":" --item-separator="\n" --field="Pays ":CB "$zones" )
zone=$(echo $zone | cut -d: -f1)
echo $zone
grep -w "$zone" continent_pays.txt | cut -d: -f3 > countries_code.txt
countries=$(grep -wif countries_code.txt donnees_pays.txt | awk -F'\t' '{print $2}')

printf '' > countries_list.txt
for country in $countries
do
    echo "FALSE" >> countries_list.txt
    echo "$country" >> countries_list.txt
done

(yad --list --fixed --width=450 --height=450 --title "Choisissez un ou plusieurs pays" --checklist --multiple --separator="" --print-column=2 --column "Select" --column "Countries" $(cat countries_list.txt)) > selected_countries_list.txt
years=$(head -n 1 donnees_pays.txt | cut -f1,2 --complement)
head -n 1 donnees_pays.txt | tr '\t' ',' > res.csv
grep -wf selected_countries_list.txt donnees_pays.txt | tr '\t' ',' >> res.csv

start=$(yad --entry --entry-label="Début de la période d'étude" --numeric 1800 2050)
end=$(yad --entry --entry-label="Fin de la période d'étude" --numeric $start 2050)

start_col=$(expr $start - 1797)
end_col=$(expr $end - 1797)


cut -d"," -f2,$start_col-$end_col res.csv > data_chart.csv

echo "series: [" > data_chart.html

lines=$(tail -n +2 data_chart.csv | wc -l)
x=2

while [ $x -le $(expr $lines + 1) ]
do
    name=$(sed "${x}q;d" data_chart.csv | cut -d"," -f1)
    serie=$(sed "${x}q;d" data_chart.csv | cut -d"," -f1 --complement)

    echo "{
            name: '$name',
            data: [$serie]
        }, " >> data_chart.html
    x=$(( $x + 1 ))
done

echo "],
" >> data_chart.html



cat model_start.html > final_chart.html
cat data_chart.html >> final_chart.html
cat model_end.html >> final_chart.html

sed -i -e "s/VARstart/$start/g" final_chart.html
sed -i -e "s/VARend/$end/g" final_chart.html

rm countries_code.txt
rm zones.txt
rm res.csv
rm data_chart.csv
rm countries_list.txt
rm selected_countries_list.txt