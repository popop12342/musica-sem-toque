pid=`cat /home/pi/felipe.pid`
lista=`ps -ef|grep $pid|awk {'print\$2'}`
for n in $lista
	do
	kill -9 $n
done
