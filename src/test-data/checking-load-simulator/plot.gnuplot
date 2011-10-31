set terminal pdf
set output output.pdf
plot "smaller.txt" using 1, "steadysmaller.txt" using 1
