语音下载方式：  
服务器：xxx.xxx.xxx
路径：/data/workspace/ENAudios/evl/path  
命令：   python3 download.py+ 起止时间  例如：  
 python3 curl_download_f.py 20190401 20190501  
（注意：使用命令行下载的话需要有创建文件夹权限的账号）  
语音处理方式：  
运行linux_read_name_score.py文件  
命令：   python3 analyze_name_score.py 起止时间+任务名  例如：  
 python3 linux_read_name_score.py 20190401 20190501 libu  
（注意：该命令是解压文件到运行py脚本的目录下）  