#!/bin/bash
################################################################################
_info="
#===============================================================================
 FILENAME: bashrx.sh
 AUTHOR:   Daniel Alan Collins (DAC) <dac@dacdynamics.com>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
_svn=( $(printf "%s" "${_info}")
  2026-08-10-1551u
); _rev=$(printf ${_svn[$((${#_svn[*]}-1))]} ) ;
################################################################################
##==============================================================================
## MYBASHRC (~/mybashrc.sh)
## if [ -f "$MYBASHRC" ]; then . "$MYBASHRC"; fi 

##==============================================================================
## LOAD PERSONAL SETTINGS
##------------------------------------------------------------------------------

  SETPATHRC="$HOME/etc/.pathrc"
  MYPATHSRC="$HOME/etc/mypaths.rc"
  MYBASHRC="$HOME/lib/mybashrc.sh"
  alias mybash=". \"$MYBASHRC\" "
  alias abe="   . \"$MYBASHRC\" "

#==========================================================
  ME=${USER} ;
  LIB="${HOME}/lib";
  HUB="${HOME}/lib/sh";
  HUB="${HOME}/lib";

        bashrx="${LIB}/bashrx.sh" ;
        bax="${LIB}/bashrx.sh" ;
  alias bashrx="    . $bashrx" ;
  alias bax="       . $bax " ;
  bashit(){
    . "$bashrx";
    # cp -pvf "$bashrx" ${HOME}/.bashrc 
  }
  basher(){
    . "$bashrx";
  }
###========================================================
  #PYTHONPATH=/Users/dac/mylab
  export PYTHONPATH=/Users/dac/lib/py
##=========================================================
## MYPATHSRC... setting & retrieving favorites 
##---------------------------------------------------------
  # set paths
  #	PATH=$(cat /home/common/pathset/pathset.rc) ;
	# export PATH=${PATH}:${HUB}:${CLIB}:/home/common/lic:/home/common/lib ;

  savepath(){
    echo "saving $PWD as favorite in $MYPATHSRC"
    printf  '%s\n' "$PWD" >> $MYPATHSRC
    # tail -n1 $MYPATHSRC
  }
  alias swd='savepath'
  getpath(){
    local dest="${1}" 
    ## dest:{ "y|d" -->"ydir"; def: "c|*"--> cd selpath }    
    local j listpaths eachpath sel selpath
    local jmax=(`wc -l $MYPATHSRC`)
    br ">"; printf "\t Selection menu\n"
    printf "%s \t %s \n" "Key" "Path"
    for j in `seq 1 $jmax` ; do
      eachpath=$(head -n $j $MYPATHSRC | tail -n 1)
      printf "%d \t %s \n" $j "$eachpath" 
    done
    read -p "> To select desired path, enter associated key: " sel
    if [ -z $sel ]; then selpath="$PWD"; fi
    selpath=$(head -n $sel $MYPATHSRC | tail -n 1) 
    printf "\n You chose selection# ${sel} and directory %s \n" "${selpath}"
    br ">" 
    case $dest in 
    d|y|yd|ydir)
      export ydir="${selpath}"
      printf "saving the selected path as ydir...\n"
      printf "ydir=${ydir} \n"
    ;;
    cd|c|*)
      printf "now navigating to the selected path as ydir...\n"
      cd "$selpath"      
      date; pwd; ls -latr -h | tail -n10 ; printf "\n"
    ;;
    esac
    printf "\n"
  }
  alias ask=' getpath '
  alias awd=' getpath '
  alias gwd=' getpath '
	alias cwd='		 cat -n  ~/.pathrc | more';
	function fav(){
		FAVDIR=(`cat ~/.pathrc `) ;
		export $FAVDIR 
		. $HUB/setfav.sh 
	}
	alias getfav=". $HUB/setfav.sh " 

##=========================================================
## PRINT BREAKS 
##---------------------------------------------------------
  function dash(){
    local str="${1}"
    local rep="${2}"
    if [ -z $rep ]; then rep=80;  fi
    if [ -z $str ]; then str="#"; fi
    local OUT=$(printf "%${rep}s"|sed "s/ /${str}/g")
    printf '%s' $OUT 
  }
 #br(){ local c="$1"; printf "%s\n" $(dash "$c" 80); } ## eg: br '\~
  br(){ local r=78;local s="$1";printf "# %s\n" $(printf "%${r}s"|sed "s/ /${s}/g");} 
  pr(){ local r=78;local s="$1";printf "# %s\n" $(printf "%${r}s"|sed "s/ /${s}/g");} 
  function dasher(){
    #str="${1}"
    local str=$(printf '%s' "${1}")
    local rep="${2}"
    if [ -z $rep ]; then rep=10;  fi
    if [ -z $str ]; then str="#"; fi
    local rep=$((rep-2)) ; if [[ $rep -lt 5 ]]; then rep=3; fi
    local OUT=$(printf "%${rep}s"|sed "s/ /${str}/g")
    printf '# %s\n' $OUT
  }
  function pash(){  
    str=$(printf '%s' "${1}")
    rep="${2}"
    if [ -z $rep ]; then rep=10;  fi
    if [ -z $str ]; then str="#"; fi
    rep=$((rep-2)) ; if [[ $rep -lt 5 ]]; then rep=3; fi
    OUT=$(printf "${str}%.s" $(seq  1 ${rep} ) )
    printf '# %s\n' $OUT
  } ; 
  DIVI=(
      $(dash '##' 40)
      $(dash '==' 40)
      $(dash '..' 40)
      $(dash '__' 40)
      $(dash '~~' 40)
  );
  fdate(){
      local inp="$1"; local F="-" ;
      case $inp in 
      p|.)    F=".";; #%Y.%m.%d.%H.%M.%S
      u|_)    F="_";; #%Y_%m_%d_%H_%M_%S
      t|~)    F="~";; #%Y~%m~%d~%H~%M~%S
      s|\*)   F="*";; #%Y*%m*%d*%H*%M*%S
      d|-|*)  F="-";; #%Y-%m-%d-%H-%M-%S
      esac
      fdate=$(date +%Y$F%m$F%d$F%H$F%M$F%S)
      printf "$fdate"
  }
##=========================================================

##---------------------------------------------------------
##	TIMESTAMPING
##---------------------------------------------------------
  NOW=$(date +%Y%m%d%-H%M%S);
  TICK=$(date +%Y%m%d-%H:%M:%S); 
  TIC=$(date +%s );
  function tic() { TIC=$(date +%s ); printf "%s" "${TIC}" ; }
  function heute() {
		JE=(
			$(date +%Y)
			$(date +%m) $(date +%b)
			$(date +%d)
			$(date +%j)
			$(date +%W)
			$(date +%u) $(date +%a)
      $(date +%s )
			$(date +%H) $(date +%M) $(date +%S)
			$(date +%z) $(date +%Z)
			$(date -u +%T) ) ;
    a=$(dash '-' 5)
    a="    "
		printf "\nDate & Local Time:
$a Year:    %s
$a MonthNr: %s
$a Month:   %s
$a dayMon:  %s
$a dayYear: %s
$a Week#:   %s
$a dayNr:   %s
$a dayWeek: %s
$a Epoch:   %s 
$a Hour:    %s
$a Minute:  %s
$a Second:  %s
$a Zone:    %s, %s
$a UTC/Zulu:%s 
" "${JE[@]} " ;
  } ##=========================================================

  function jnow()  { printf "%s" $(date +%Y%m%d_%H%M%S         ); };
  function snow()  { printf "%s" $(date +%s                    ); };
  function jnowe() { NOW=$(date +%Y%m%d_%H%M%S);    printf $NOW;  };
  function snowe() { NOW=$(date +%s   );            printf $NOW;  };
  
  function getz(){ 
    local f="${1}"
    local ts='%s' 
    if [ -n $2 ]; then
      case $2 in 
      3) ts='%Y%m%d-%H%M%S' ;;
      2) ts='%Y%m%d_%H%M%S' ;;
      1|*) ts='%s' ;;
      esac 
    fi 
    printf $(ls -la -D $ts ${f} |awk '{print $6}'); 
  };

  function fsuff(){
    ## returns the suffix of file f 
    local f=$1
    local d=0; if [ -n $2 ]; then
    printf ${f##${f%%.*}} | tr -d "." 
    else 
    printf ${f##${f%%.*}} 
    fi  
  }
  ##---------------------------------------------------------
  ## BANK / ATM / BKUP
  export BANK="${HOME}/BANK" ;
  mkdir -p $BANK ;
 #alias atm=" mv -vi *__????????-???? $BANK " 
  alias atm=" mv -v  *????????-????* $BANK " 
  function ruk(){
	  local T=$(getz ${1} 3);
    local S=$(fsuff $1 1)
    if [ -n $2 ] ;then S="$2"; fi 
    cp -vfp ${1} ${1}_bk${T}.${S} ;
  };

##---------------------------------------------------------
##	...
##---------------------------------------------------------
	function dateline(){
		printf "\n# %s\n $(date)\n $(pwd)\n $(hostname -s)\n# %s \n " \
    $(dash '#' 77)  $(dash '~' 77)
	}

###========================================================
##	BLOCK_A
##---------------------------------------------------------
  alias echoe='echo -e '
	alias ta1='tail -n1'
		    ta1='tail -n1'
	alias he1='head -n1'
		    he1='head -n1'
	alias wee='whoami; hostname; pwd; date;ls -tr1Ah $PWD|tail -n10;df -ah .' 
  alias age=' alias | grep ' 
	alias mv='mv -v'
	alias up="cd .."
	alias vab="vi $HOME/.bashrc"
	alias svf=" .	${HUB}/svf.sh" 
	alias gator='  alias | grep ' 
	alias alamo='  alias | more '
  alias setag='  set   | grep '
  alias gnot=" grep -i -e -v " 
	alias seek='find $PWD | grep -i -e      '
	alias le='less '
	alias ge='gedit  '
	alias mo='more  '
	alias pg='ps -Af | grep '
	alias taff='tail -n 1000  -F -f  '

	alias lt='   ls -1lh   '
	alias lh="   ls -lA1trh "
	alias lt='   ls -lAt   '
	alias lr="   ls -lAtr  "   ##  $ztsm           "
	alias la="   ls -lAtrh "   ##  $ztsm | awk $PQ "
	alias lk='   ls -lASh  '
	alias lg='   ls -laR | grep             '
	alias lsg='  ls -latR . | grep          '
  alias ll='ls -l --color=auto'  ## default

  bank(){
    local file="${1}" 
    local filest=$(basename "$file")
    local filepw="${file%%$filest}"
    if [ -z "$filepw" ]; then filepw="${PWD}"; fi
    local filert="${filest%%\.*}"
    local filext=$( echo ${filest##$filert} | tr -d '.' )
    filext=$( echo ${filest##$filert} )
    if [ -z "$filert" ] ; then filert="$filext"; filext=""; fi
    printf "
    file: $file \n filepw: $filepw \n filest: $filest \n filert: $filert \n filext: $filext \n"
    local F="_"
    local filedate=$(
      ls -latr --full-time --time-style="+%Y$F%m$F%d$F%H$F%M$F%S" "${file}" | \
      awk '{print $6}'
    )
    echo "$filedate"
    local fileback="${filepw}/${filert}_bk${filedate}${filext}"
    cp -pvf "${file}" "${fileback}"
  }
  #latest(){
  #  latest=$(ls -tr $(find . | grep -i -e $1 ) | tail -n1 );
  #  printf "${latest}" ;
  #}
  latest(){
    local ke kw pw lf 
    ke="${1}"
    kw="${2}"
    pw="${3}"
    if [ -z $pw ]; then pw="${PWD}"; fi
    if [ -n $kw ]; then 
      lf=$( ls -tr "${pw}" | grep "${ke}" | grep -E "${kw}" | tail -n1 )
    else 
      lf=$( ls -tr "${pw}" | grep "${ke}" )
    fi
    printf "${lf}"
  }