echo $1, $2, $3
len=$3
codepath="/home/xiaowen/research/202108_nanopore/nanospectra/python/"
echo $codepath
weight=30
neighbor_weight=0
python3 ${codepath}process/generate_theory_trace.py $1 theory_trace.csv $neighbor_weight 10000  none
python3 ${codepath}plot/event_avg_plot.py theory_trace.csv theory_trace.png

python3 ${codepath}/direct/direction_pcc.py theory_trace.csv $2 flip_event.csv direction.data > direction.out 

python3 ${codepath}/direct/direction_plot.py direction.data direction.eps 

python3 ${codepath}process/remove_end.py flip_event.csv flip_event_remove_end.csv
python3 ${codepath}plot/event_avg_plot.py flip_event_remove_end.csv flip_event_remove_end.png
python3 ${codepath}process/trace_sampling.py flip_event_remove_end.csv $len flip_event_${len}.csv

python3 ${codepath}plot/event_avg_plot.py flip_event_${len}.csv flip_event_${len}.png
python3 ${codepath}process/trace_sampling.py theory_trace.csv ${len} theory_trace_${len}.csv
python3 ${codepath}plot/event_avg_plot.py theory_trace_${len}.csv theory_trace_${len}.png

python3 ${codepath}align/align_ref.py theory_trace_${len}.csv flip_event_${len}.csv flip_event_${len}_align.eps > flip_event_${len}_align.out
python3 ${codepath}align_consensus/sort_events.py flip_event_${len}.csv sort_flip_event_${len}.csv > sort_event.out
python3 ${codepath}align_consensus/self_align_consensus.py theory_trace_${len}.csv sort_flip_event_${len}.csv $weight align_optimize_${weight}_${len}.csv > align_optimize_${weight}.out
python3 ${codepath}align/align_ref.py theory_trace_${len}.csv align_optimize_${weight}_${len}.csv align_optimize_${weight}_${len}_align.eps > align_optimize_${weight}_${len}_align.out

python3 ${codepath}align/obtain_current.py theory_trace_${len}.csv align_optimize_${weight}_${len}.csv current_align.png current_${len}.csv
python3 ${codepath}plot/event_avg_plot.py current_${len}.csv current_${len}.png
'
