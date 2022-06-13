from Posts.models import post
from Categories.models import Categories
from django.core.paginator import Paginator
from django.shortcuts import render

def home_data():
    most_pupolar = post.objects.order_by("-post_view").first()

    recent_posts = post.objects.raw("SELECT * FROM Posts_post ORDER BY id DESC")

    paginator = Paginator(recent_posts,6)
    recent_posts = paginator.page(1)
    
    most_views = post.objects.raw("SELECT * FROM Posts_post ORDER BY post_view DESC LIMIT 3")
    all_cat = Categories.objects.raw("SELECT count(*) as count_post,Categories_categories.*  FROM Posts_post JOIN Categories_categories on Categories_categories.id = Posts_post.cat_id_id GROUP by Categories_categories.id ")

    data = {
        'most_pupolar' : most_pupolar,
        'recent_posts' : recent_posts,
        'most_views' : most_views,
        'all_cat' : all_cat,
    }

    return data