
CONFIG_DEFAULTS = """\
[tcc3]
log-format = $(levelname)s: $(message)s
database-type = csv
collector-type = vmstat
main-database-name = main
trained-database-name = trained
databases-dir = ./databases
learning-method = knn

knn-number-neighbours = 5

[conf]
path-environment = TCC3_CONF
user-file = .tcc3.conf
system-file = /etc/tcc3/tcc3.conf
"""
