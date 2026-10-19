main(){

date 

echo "list of packages ..." 
cat pip_install_list.txt 

for pkg in `cat pip_install_list.txt`
do

    date
    echo "install $pkg"
    python3 -m pip install $pkg
    conda install -y $pkg

done
echo "done installation"
}

main | tee -a pip_install.log 