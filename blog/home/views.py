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

from home.models import Comment
from django.shortcuts import redirect,reverse
class DetailView(View):

    def get(self,request):
        # detail/?id=xxx&page_num=xxx&page_size=xxx
        #获取文档id
        id=request.GET.get('id')
        page_num=request.GET.get('page_num',1)
        page_size=request.GET.get('page_size',5)
        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        try:
            article=Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request,'404.html')
        else:
            article.total_views+=1
            article.save()

        # 获取热点数据
        hot_articles = Article.objects.order_by('-total_views')[:9]

        # 获取当前文章的评论数据
        comments = Comment.objects.filter(
            article=article
        ).order_by('-created')
        #获取评论总数
        total_count = comments.count()

        # 创建分页器：每页N条记录
        paginator = Paginator(comments, page_size)
        # 获取每页商品数据
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户404
            return HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories':categories,
            'category':article.category,
            'article':article,
            'hot_articles':hot_articles,
            'total_count': total_count,
            'comments': page_comments,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num,
        }

        return render(request,'detail.html',context=context)

    def post(self,request):
        #获取用户信息
        user=request.user

        #判断用户是否登录
        if user and user.is_authenticated:
            #接收数据
            id=request.POST.get('id')
            content=request.POST.get('content')

            #判断商品id
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponseNotFound('没有此文章')

            #保存到数据
            Comment.objects.create(
                content=content,
                article=article,
                user=user
            )
            #修改文章评论数量
            article.comments_count+=1
            article.save()
            #拼接跳转路由
            path=reverse('home:detail')+'?id={}'.format(article.id)
            return redirect(path)
        else:
            #没有登录则跳转到登录页面
            return redirect(reverse('users:login'))

"""
insert into tb_comment(content,created,article_id,user_id)
select content,created,article_id,user_id from tb_comment;
"""