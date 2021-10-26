from django.shortcuts import render
from .models import Blog , Author


def blog(request):
    blogs = Blog.objects.all()
    trending_blogs = Blog.objects.all().order_by('-click_counter')
    if request.method == "POST":
        filtered_blogs = []
        keyword = request.POST.get("keyword")
        for blog in blogs:
            keywords= str(blog.keywords).split(';')
            for k in keywords:
                if k.lower()==keyword.lower():
                    filtered_blogs.append(blog)
                    break
        blogs=filtered_blogs
    return render(request, "blog/blogs.html",{'blogs':blogs,'trending_blogs':trending_blogs})

def blog_detail(request, blog_name):
    blog = Blog.objects.get(title=blog_name)
    blog.click_counter=blog.click_counter+1
    blog.save()
    trending_blogs = Blog.objects.all().order_by('-click_counter')
    return render(request, "blog/blog_detail.html",{'blog':blog,'trending_blogs':trending_blogs})
