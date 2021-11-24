codepath="/Users/xiaowenliu/code/nanospectra/python/"
echo $codepath

base1=`basename $1`
base2=`basename $2`
base1="${base1%.*}"
base2="${base2%.*}"
echo $base1
echo $base2

python3 ${codepath}/learn/train_model.py ${base1}.data ${base2}.data 
