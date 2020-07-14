from django.db import models

# Create your models here.
class Radar_05(models.Model):
    #ID：
    dictionay_id = models.AutoField(primary_key=True)
    # 路径
    dir_name = models.TextField()
    # 大小
    space = models.BigIntegerField()
    # # 空间占比 先不加
    # percentage = models.TextField()
    # 扫描日期
    scan_date = models.DateTimeField()

    def __str__(self):
        return self.dir_name


class networkPaths(models.Model):
    path_id = models.AutoField(primary_key=True)
    #需要扫描的文件路径
    path = models.TextField()

    def __str__(self):
        return self.path
