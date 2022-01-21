BEGIN {
  FS="\"";
  ok=0;
  print "pers;cat;act;link1;x;y;max_dur;mode;time1;link2;time2;dist";
}

/person id/ {pers=$2;}
/yes/{ok=1;}

/activity type/ && ok==1{
	act=$2;link1=$4;x=$6;y=$8;max_dur=$10;

	print pers";"cat";"act";"link1";"x";"y";"max_dur";"mode";"time1";"link2";"time2";"dist
}
/leg mode/ && ok==1{mode=$2;time1=$6;}
/route type/ {link2=$6;time2=$8;dist=$10}
/selected/ && /no/ {ok=0;}
/rev/ {cat=substr($5,2,4);}


