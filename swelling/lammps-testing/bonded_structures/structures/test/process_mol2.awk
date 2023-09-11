awk 'BEGIN {process=0} 
     /@<TRIPOS>ATOM/ {process=1} 
     /@<TRIPOS>/ {if ($0 !~ /@<TRIPOS>ATOM/) process=0} 
     process==1 && /^[[:space:]]*[0-9]+/ {$2=substr($2, 1, 1)} 
     {print}' input.mol2 > output.mol2

