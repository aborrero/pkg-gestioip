#
# Regular cron jobs for the gestioip package
#
0 4	* * *	root	[ -x /usr/bin/gestioip_maintenance ] && /usr/bin/gestioip_maintenance
