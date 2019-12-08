from django.shortcuts import render
from django.views import View
# Create your views here.
from home.models import ArticleCategory
from django.http import HttpResponseNotFound

class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        #?cat_id=xxx&page_num=xxx&page_size=xxx
        cat_id=request.GET.get('cat_id',1)

        #判断分类id
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')

        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        context = {
            'categories':categories,
            'category':category
        }

        return render(request, 'index.html',context=context)