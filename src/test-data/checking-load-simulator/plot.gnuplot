set terminal png
set output "output.png"
plot "workloadsmaller.txt" using 1 title "Carga simulada", "steadysmaller.txt" using 1
