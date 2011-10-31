set terminal png
set output "output.png"
plot "workloadsmaller.txt" using 1, "steadysmaller.txt" using 1
