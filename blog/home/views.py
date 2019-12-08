from django.shortcuts import render
from django.views import View
# Create your views here.
from home.models import ArticleCategory,Article
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator,EmptyPage

class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        #?cat_id=xxx&page_num=xxx&page_size=xxx
        cat_id=request.GET.get('cat_id',1)
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 10)
        #判断分类id
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')

        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        #分页数据
        articles = Article.objects.filter(
            category=category
        )

        # 创建分页器：每页N条记录
        paginator = Paginator(articles, page_size)
        # 获取每页商品数据
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            # 如果没有分页数据，默认给用户404
            return HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories':categories,
            'category':category,
            'articles': page_articles,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num,
        }

        return render(request, 'index.html',context=context)

class DetailView(View):

    def get(self,request):
        # detail/?id=xxx&page_num=xxx&page_size=xxx
        #获取文档id
        id=request.GET.get('id')

        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        try:
            article=Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request,'404.html')

        context = {
            'categories':categories,
            'category':article.category,
            'article':article,
        }

        return render(request,'detail.html',context=context)