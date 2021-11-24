echo $1 $2 $3
len=$2
num=$3
weight=30
codepath="/Users/xiaowenliu/code/nanospectra/python/"
echo $codepath
python3 ${codepath}process/generate_theory_trace.py $1 theory_trace_${len}.csv 0 $len 'pos'
python3 ${codepath}align/align_ref.py theory_trace_${len}.csv align_optimize_${weight}_${len}.csv align_optimize_${weight}_${len}_align.eps > align_optimize_${weight}_${len}_align.out
python3 ${codepath}process/generate_random.py randam_trace_${num}.csv $len $num

python3 ${codepath}test/test_random.py align_optimize_${weight}_${len}.csv randam_trace_${num}.csv random_scores_${num}.csv random_scores_${num}.png 

python3 ${codepath}test/score_stat.py random_scores_${num}.csv 
