from django.db import models
from django.utils import timezone

# Create your models here.
class ArticleCategory(models.Model):
    """
    文章分类
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table='tb_category'
        verbose_name = '类别管理'
        verbose_name_plural = verbose_name