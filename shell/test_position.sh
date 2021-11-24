echo $1,$2 
len=$2
weight=30
codepath="/Users/xiaowenliu/code/nanospectra/python/"
echo $codepath
#python3 ${codepath}process/generate_theory_trace.py $1 theory_trace_${len}.csv 0 $len
python3 ${codepath}align/align_ref.py theory_trace_${len}.csv align_optimize_${weight}_${len}.csv align_optimize_${weight}_${len}_align.eps > align_optimize_${weight}_${len}_align.out
