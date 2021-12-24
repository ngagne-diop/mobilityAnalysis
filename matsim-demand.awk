# script pour générer la demande
# Authors: Moez Kilani and Ngagne Diop
# Date: April 2020
# Last edited: May 2021
#######Quelques modifs par rapport à la version 4 du code :
############ 1/ line 10 : .0 en tant que texte car obligatoire 
############ 2/ line 90 : le mode dans la balise leg
############ 3/ input code : travel diaries NPdC lancé à la place de HdF
############ 4/ lines 30, 31, 35 et 36 remplacées par lines 33 et 38



BEGIN {
  FS=";"; 
# Mandatory heading for MATSim
  print "<?xml version=\""1".0\" encoding=\"utf-8\"?>";
  print "<!DOCTYPE population SYSTEM \"http://www.matsim.org/files/dtd/population_v6.dtd\">";
  print "";
  print "<population>";
  print "";
  print "  <attributes>";
  print "    <attribute name=\"coordinateReferenceSystem\" class=\"java.lang.String\" >EPSG:2154</attribute>";
  print "  </attributes>";
  print "";
# initialisation
  for(i=0; i<=10; ++i) {y[i]=i/10;}
  id=""; 
  debut=0;
  ctr=0;
  rev_max = 0;
  rev_min =100000;
  gr1=0;
  gr2=0;
  gr3=0;
  rev_th1 = 11324.39; # threshold between rev1 and rev2
  rev_th2 = 22995.59; # threshold between rev2 and rev3 
}


NR > 1 {
## Coordonnées activité à l'origine
   D3X=$8;
   D3Y=$9;
## Coordonnées activité à l'arrivée
   D7X = $14;
   D7Y = $15;
## Temps de debut du déplacement (temps de fin de l'activité amont)
#   if($5<=9){HH="0"$5;}else{HH=$5};
#   if($6<=9){MM="0"$6;}else{MM=$6};
#   D4=HH":"MM":00";
   D4=$5":"$6":00";
## Temps de fin du déplacement (temps de début de l'activité aval)
#   if($11<=9){HH="0"$11;}else{HH=$11};
#   if($12<=9){MM="0"$12;}else{MM=$12};
#   D8=HH":"MM":00";
   D8=$11":"$12":00";


# Check consistency (departure times should precede arrival time)
#  if($5>30) {print "haha5->> " $5, $2;}
#  if($5>$11) {print "haha6->> " $5, $11, $2, $34}
#  if($5==$11 && $6>$12) {print "haha7->> " $5,":"$6,"   ", $11":"$12, $2, $34}
   if($6>60 || $12>60) {print "haha8 --> ", $2;}


## Coefficient de ponderation
   COEQ=$3;

# Deciles of the revenu
   if($48 > 10 && $2 != id) {
     x[0]  = $48 - ($49-$48);
     x[1]  = $48;
     x[2]  = $49;
     x[3]  = $50;
     x[4]  = $51;
     x[5]  = $45;
     x[6]  = $52;
     x[7]  = $53;
     x[8]  = $54;
     x[9]  = $55;
     x[10] = $55 + ($55-$54);
     YY = rand();
     II = int(YY*10);
     XX = x[II] + (YY - y[II]) * (x[II+1] - x[II]) / (y[II+1] - y[II]);
     if (XX < rev_th1) {
         rev="rev1";
         ++gr1;
       } else if (XX > rev_th2) {
         rev="rev3"; 
         ++gr3;
       } else {
         rev="rev2";
         ++gr2;
     }
#    if (rev_min > XX) {rev_min = XX;}
#    if (rev_max < XX) {rev_max = XX;}
   }
#  print "REVENUE ==> ", II, XX, YY, "x[",II"]=",x[II], "x[",II+1,"]=",x[II+1];

   D2AA = MotifOrigine($10);
   D5AA = MotifDestination($16);
   MODP = ModeTransport($17);

   if (debut==0) {
   # valeurs de la nouvelle ligne
     ctr = 1;
     AjouterLignes(pers,ctr,D2AA,D3X,D3Y,"00:00:00",D4,MODP);
     ctr = 3; 
     debut = 1;
   } else if ($2 != id"") {
#    print $2, "id", id;
   # valeurs de l'ancienne ligne
     AjouterLigne(pers,ctr,D5AA0,D7X0,D7Y0,D80);
#    ctr += 1;
#    print x[0], x[10], XX, YY
     ImprimerPersonne(id,1,ctr,COEQ_old,rev);
   # On passe à une nouvelle personne
   # valeurs de la nouvelle ligne
     ctr = 1;
     AjouterLignes(pers,ctr,D2AA,D3X,D3Y,"00:00:00",D4,MODP);
     ctr = 3;
   } else {
   # valeurs de la nouvelle ligne
#    print $2, "id", id;
     AjouterLignes(pers,ctr,D2AA,D3X,D3Y,D80,D4,MODP);
     ctr += 2;
   }
   id=$2;
   D80 = D8;
   D5AA0 = D5AA;
#  print D5AA0;
   D3X0 = D3X ;
   D3Y0 = D3Y ;
   D7X0 = D7X ;
   D7Y0 = D7Y ;
   D40  = D4 ;
   MODP = MODP0;
   COEQ_old=COEQ;


 }

END { 
   AjouterLigne(pers,ctr,D5AA,D7X,D7Y,D8);
#  ctr += 1;
   ImprimerPersonne($2,1,ctr,COEQ,rev);
#  print "    </plan>";
   print "</population>";
#  print gr1, gr2, gr3;
}

function AjouterLignes(pers,ctr,D2AA,D3X,D3Y,D8,D4,MODP) {
     pers[ctr]  ="       <activity type=\""D2AA"\" x=\""D3X"\" y=\""D3Y"\" start_time=\""D8"\" end_time=\""D4"\"/>";
     pers[ctr+1]="       <leg mode=\""MODP"\"></leg>";
   }

function AjouterLigne(pers,ctr,D5AA,D7X,D7Y,D80) {
     pers[ctr]  ="       <activity type=\""D5AA"\" x=\""D7X"\" y=\""D7Y"\" start_time=\""D80"\"/>";
   }

#     print "       <act type=\""D5AA"\" x=\""D7X"\" y=\""D7Y"\" start_time=\""D80"\" />";

function ImprimerPersonne (id,n,ctr,pond,rev) {
  str = id;
  OpenPerson(id,pond,rev);
  for(i=1;i<=ctr;i++) {
    print pers[i]; }
  ClosePerson();
}

function OpenPerson (id,pond,rev) { 
  print "  <person id=\""id"\">"; 
  printf "%-7s %.3f %-4s\n",  "  <!--;",pond,";-->";
  print "    <attributes>"
  print "       <attribute name=\"subpopulation\" class=\"java.lang.String\">"rev"</attribute>"
  print "    </attributes>"
# printf "%-7s %.3f %-4s\n",  "  <!--;",rev,";-->";
  print "    <plan>"; 
}

function ClosePerson () {

  print "    </plan>";
  print "  </person>";

}

# motif à l'origine
function MotifOrigine(X) {
   switch (X) {
     case 1: 
          D2AA = "home";
          break
     case 2:
          D2AA = "work";
          break
     case 3:
          D2AA = "education";
          break
     case 6:
          D2AA = "shop";
          break
     case 7:
          D2AA = "leisure";
          break
     case 8:
          D2AA = "leisure";
          break
     case 9:
          D2AA = "leisure";
          break
     case 10:
          D2AA = "leisure";
          break
     case 11:
          D2AA = "leisure";
          break}; 
      return D2AA;
  }

# motif à l'arrivée
function MotifDestination(X) {
   switch (X) {
     case 1: 
          D5AA = "home";
          break
     case 2:
          D5AA = "work";
          break
     case 3:
          D5AA = "education";
          break
     case 6:
          D5AA = "shop";
          break
     case 7:
          D5AA = "leisure";
          break
     case 8:
          D5AA = "leisure";
          break
     case 9:
          D5AA = "leisure";
          break
     case 10:
          D5AA = "leisure";
          break
     case 11:
          D5AA = "leisure";
          break }; 
     return D5AA;
  }

# mode de transport
function ModeTransport (X) {
   switch(X) {
     case 1:
          MODP = "walk";
          break
     case 11:
          MODP = "bike";
          break
     case 12:
          MODP = "bike";
          break
     case 13:
          MODP = "bike";
          break
     case 14:
          MODP = "bike";
          break
     case 15:
          MODP = "bike";
          break
     case 21:
          MODP = "car";
          break
     case 22:
          MODP = "car";
          break
     case 61:
          MODP = "car";
          break
     case 81:
          MODP = "car";
          break
     case 93:
          MODP = "car";
          break
     case 99:
          MODP = "car";
          break
     case 31:
          MODP = "pt";
          break
     case 32:
          MODP = "pt";
          break
     case 33:
          MODP = "pt";
          break
     case 34:
          MODP = "pt";
          break
     case 39:
          MODP = "pt";
          break
     case 41:
          MODP = "pt";
          break
     case 43:
          MODP = "pt";
          break
     case 51:
          MODP = "pt";
          break
     case 71:
          MODP = "pt";
          break
     case 72:
          MODP = "pt";
          break
     case 91:
          MODP = "pt";
          break
     case 92:
          MODP = "pt";
          break };
     return(MODP);
}

