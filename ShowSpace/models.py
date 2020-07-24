from django.db import models


# Create your models here.

class isilon(models.Model):
    # ID：
    id = models.AutoField(primary_key=True)
    # folder_name
    folder_name = models.CharField(max_length=100)
    # folder_dir
    folder_dir = models.TextField()
    # total_size
    # total_space = models.BigIntegerField()
    total_space = models.CharField(max_length=100)
    # used
    used_space = models.CharField(max_length=100)
    # free
    free_space = models.CharField(max_length=100)
    # percentage
    percentage = models.CharField(max_length=100)
    # 扫描日期
    scan_date = models.DateTimeField()

    def __str__(self):
        return self.scan_date


class radar05(models.Model):
    # ID：
    id = models.AutoField(primary_key=True)
    # folder_name
    folder_name = models.CharField(max_length=100)
    # folder_dir
    folder_dir = models.TextField()
    # 文件夹大小
    folder_size = models.BigIntegerField()
    # 扫描日期
    scan_date = models.DateTimeField()
    # 扫描文件夹所需时间
    time_duration = models.FloatField()

    def __str__(self):
        return self.folder_name


class radar05_details(models.Model):
    # ID：
    id = models.AutoField(primary_key=True)
    # folder_name
    folder_name = models.CharField(max_length=100)
    # 绝对路径
    folder_dir = models.TextField()
    # 文件类型
    type = models.CharField(max_length=100)
    # 文件数量
    number = models.BigIntegerField()
    # 文件夹大小
    size = models.BigIntegerField()
    # 扫描日期
    scan_date = models.DateTimeField()

    def __str__(self):
        return self.folder_name


