echo $1
len=$1
codepath="/Users/xiaowenliu/code/nanospectra/python/"
echo $codepath
for weight in {1..9};
do
  echo "weight $weight"
  python3 ${codepath}align_consensus/self_align_consensus.py theory_trace_${len}.csv sort_flip_event_${len}.csv $weight align_optimize_${weight}_${len}.csv > align_optimize_${weight}.out
done

for i in {1..10};
do
  let weight=$i*10
  echo "weight $weight"
  python3 ${codepath}align_consensus/self_align_consensus.py theory_trace_${len}.csv sort_flip_event_${len}.csv $weight align_optimize_${weight}_${len}.csv > align_optimize_${weight}.out
done
