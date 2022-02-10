#!/bin/bash
 
'''
Released by Winifred A. Atiah and Edmund I. Yamba.
 
When using this code, please acknowledge the Meteorology and Climate Science Unit (KNUST).

This script computes the rainfall indices (onsets, cessations and durations) from rainfall data using the percentage mean cumulative rainfall amount (PMCR) method. 

This code is open-licensed, hence modifications are allowed to suit the users preference and work. Any major 
modifications should however be communicated to the author via email at winifred.a.atiah@aims-senegal.org. We appreciate 
your compliance, and thanks for choosing this package.
'''

path1=~/Documents/Consul_Work_AFRISING/Chirps_daily/New_data/Ghana_data


for dt in {1..6000}  ###loop through grids containing rainfall values
   do
  
     
     input=${path1}/All_grids_data/RR_GH_${dt}
     output=${path1}/onsetcess/RR_GH_${dt}_ocl.txt
 
     
    if [ -s $output ] ; then
       rm $output
    fi
    
    yy=1981
    while [ $yy -le 2020 ] ; do

	awk -v yy=$yy '{if($1==yy) {print $0}}' $input > tta
	
	
      awk '{sum+=$4} 
           END{printf("%6.4f\n",sum);
           }' tta > total.txt
              
     awk '{sum+=$4} 
           (NR%5)==0{printf("%d %6.4f\n",NR,sum); sum=0;
          }' tta > dat4.txt 
         rm tta

	 
     read a < total.txt
    
    awk -v a=$a '{
                 printf("%d %6.4f\n",$1,($2/a)*100);
                 }' dat4.txt > dat5.txt
                rm dat4.txt
                rm total.txt
      Cumulative###c         
     awk 'BEGIN {sum=0}
                {sum=sum+$2;
                printf("%d %6.2f\n",$1,sum);
                }' dat5.txt > dat6.txt
                 rm dat5.txt
		
	
    # print out the onset/cessation day
      awk '{if($2>=7){print $0}}' dat6.txt | head -1 > out1
      awk '{if($2>=90){print $0}}' dat6.txt | head -1 > out2

      paste out1 out2 > dta
      rm dat6.txt; rm out1; rm out2

      awk -v yy=$yy '{printf("%4.2d %5d %5d %5d\n",yy,$1,$3,$3-$1)
       }' dta >> $output
      rm dta
      
      
      yy=`expr $yy + 1`
      
    done
    echo 'done with' $dt
done 
     


exit


