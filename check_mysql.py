# coding=UTF-8
import psutil
import datetime
import time
import pymysql
import os

#该脚本为MYSQL巡检脚本，传输到服务器上以：python mysql_check.py 格式执行
# 当前时间
now_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
print(now_time)

# 查看cpu物理个数的信息
cpu_count = psutil.cpu_count(logical=False);
print(u"物理CPU个数: %s" % cpu_count)

#CPU的使用率
cpu = (str(psutil.cpu_percent(1))) + '%'
print(u"cup使用率: %s" % cpu)

#查看内存信息,剩余内存.free  总共.total

free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))
total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))
memory = int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total)
print(u"物理内存： %s G" % total)
print(u"剩余物理内存： %s G" % free)
print(u"物理内存使用率： %s %%" % int(memory * 100))
# 系统启动时间
print(u"系统启动时间: %s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))

# 系统用户
users_count = len(psutil.users())

users_list = ",".join([u.name for u in psutil.users()])
print(u"当前有%s个用户，分别是 %s" % (users_count, users_list))

io = psutil.disk_partitions()

print('-----------------------------磁盘信息---------------------------------------')

print("系统磁盘信息：" + str(io))

rw_count = psutil.disk_io_counters()
print( "读总数" + str(int(rw_count.read_count)))
print( "写总数" + str(int(rw_count.write_count)))

for i in io:
    o = psutil.disk_usage("/")
    print("总容量：" + str(int(o.total / (1024.0 * 1024.0 * 1024.0))) + "G")
    print("已用容量：" + str(int(o.used / (1024.0 * 1024.0 * 1024.0))) + "G")
    print("可用容量：" + str(int(o.free / (1024.0 * 1024.0 * 1024.0))) + "G")

db = pymysql.connect(host="47.244.6.232",port=3307,user="root",passwd="6QuoQbcAxiFi" )
cursor = db.cursor()

print("---------------------------------MYSQL巡检信息--------------------------------------")
#open tables
open_tables = "show global status like 'Open_tables';"
cursor.execute(open_tables)
db.commit()
rows = cursor.fetchall()
for i in rows:
        print("当前打开表的数量：" + i[1])

#open tables variables
table_open_cache = "show variables like 'table_open_cache';"
cursor.execute(table_open_cache)
db.commit()
table_open_var = cursor.fetchall()
for i in table_open_var:
	print("打开表数量设置大小:" + str(int(i[1])) )

opened_tables = "show global status like 'Opened_tables';"
cursor.execute(opened_tables)
db.commit()
opened_tables = cursor.fetchall()
for i in opened_tables:
        print("打开过表的总量：" + i[1])

#row current lock
row_lock_current = "show global status like 'Innodb_row_lock_current_waits';"
cursor.execute(row_lock_current)
db.commit()
rows1 = cursor.fetchall()
for a in rows1:
        print("当前锁等待数量：" + a[1])

print("-------------------------缓冲池信息---------------------------------")
#buffer pool size
innodb_buffer_pool_size = "show global status like 'Innodb_buffer_pool_pages_data';"
cursor.execute(innodb_buffer_pool_size)
db.commit()
rows2 = cursor.fetchall()
for r in rows2:
	print("缓冲池使用总量:" + str((int(r[1]) * 16) / (1024 * 1024)) + "G" )

#buffer pool size variables
innodb_buffer_size = "show variables like 'innodb_buffer_pool_size';"
cursor.execute(innodb_buffer_size)
db.commit()
buffer_pool_var = cursor.fetchall()
for i in buffer_pool_var:
	print("缓冲池设定大小:" + str((int(i[1])) / (1024 * 1024 * 1024)) + "G" )

#buffer pool dirty size
Innodb_buffer_pool_pages_dirty = "show global status like 'Innodb_buffer_pool_pages_dirty';"
cursor.execute(Innodb_buffer_pool_pages_dirty)
db.commit()
dirty = cursor.fetchall()
for b in dirty:
        print("缓冲池脏页数量:" + str((int(b[1]) * 16) ) + "K" )

print("--------------------------日志信息---------------------------------")
#redologs
innodb_log_file_size = "show variables like 'innodb_log_file_size';"
cursor.execute(innodb_log_file_size)
db.commit()
redologs = cursor.fetchall()
for i in redologs:
        print("重做日志大小:" + str((int(i[1])) / (1024 * 1024 * 1024) ) + "G" )

#redolog_commit
innodb_flush_log_at_trx_commit = "show variables like 'innodb_flush_log_at_trx_commit';"
cursor.execute(innodb_flush_log_at_trx_commit)
db.commit()
redolog_commit = cursor.fetchall()
for i in redolog_commit:
        print("重做日志刷新方式参数:" + str((int(i[1]))) )

#binlog_sync
sync_binlog = "show variables like 'sync_binlog';"
cursor.execute(sync_binlog)
db.commit()
binlog_sync = cursor.fetchall()
for i in binlog_sync:
        print("二进制日志刷新方式参数:" + str((int(i[1]))) )

print("-----------------------检查是否有挂起的读写------------------------------")
#pending reads
Innodb_data_pending_reads = "show global status like 'Innodb_data_pending_reads';"
cursor.execute(Innodb_data_pending_reads)
db.commit()
pending_reads = cursor.fetchall()
for c in pending_reads:
        print("挂起读数量:" + str(int(c[1])))

#pending write
Innodb_data_pending_writes = "show global status like 'Innodb_data_pending_writes';"
cursor.execute(Innodb_data_pending_writes)
db.commit()
pending_writes = cursor.fetchall()
for d in pending_writes:
        print("挂起写数量:" + str(int(d[1])))

print("-----------------------检查一秒内创建硬盘临时表的数量------------------------------")
#tmp tables
Created_tmp_disk_tables = "show global status like 'Created_tmp_disk_tables';"
cursor.execute(Created_tmp_disk_tables)
db.commit()
disk_tmp_tables = cursor.fetchall()
for e in disk_tmp_tables:
	print("创建的硬盘临时表数量前1秒：" + str(int(e[1])))
time.sleep(1)
Created_tmp_disk_tables1 = "show global status like 'Created_tmp_disk_tables';"
cursor.execute(Created_tmp_disk_tables1)
db.commit()
disk_tmp_tables1 = cursor.fetchall()
for f in disk_tmp_tables1:
        print("创建的硬盘临时表数量后1秒：" + str(int(f[1])))

print("-------------------------当前连接数-----------------------------------")
#current connection
Threads_connected = "show global status like 'Threads_connected';"
cursor.execute(Threads_connected)
db.commit()
connection = cursor.fetchall()
for g in connection:
        print("当前连接数量：" + str(int(g[1])))

print("------------------------复制状态-------------------------------")
#master-slave
show_slave_status = "show slave status"
cursor.execute(show_slave_status)
db.commit()
slave_status = cursor.fetchall()
for h in slave_status:
        print("主从复制状态：")
        print("Slave_IO_Running:" + h[10])
        print("Slave_SQL_Running:" + h[11])

os.system("cd /usr/local/mysql/data && cat mysqld.log | grep 'ERROR'")











