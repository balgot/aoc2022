# for sed labels: 

# cat input.txt |
sed ':a;N;$!ba;s/\([^\n]\)\n\([^\n]\)/\1+\2/g;s/\n\n/\n/g' | bc | sort -n | tail -n 3 | paste -sd+ | bc