通过jenkins api进入到jenkins的任务，得到包含各个任务的字典的信息，通过比较时间戳的形式，判断是不是当日构建的任务，如果是，则统计下来。
这个脚本遇到的问题在于jenkins api得到的目录是分级的，同一级上可能存同时存在文件夹和任务，我采取的方法是判断特殊键的方式，当有jobs这个键的时候，说明有下级目录的存在，则进入下一级，否则不进入下一级。我深挖的目录最大深度为五级  
本脚本在运行前还会先判断一下是否数据库中有昨天的信息，如果有，则不运行该脚本。