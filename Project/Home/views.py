from django.contrib import messages
from django.shortcuts import redirect, render
from Categories.models import Categories
from Posts.models import post , comment
from . import logic
from Customer.models import Customer, message
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    most_pupolar = post.objects.filter(post_status=1).order_by("-post_view").first()
    recent_posts = post.objects.raw("SELECT * FROM Posts_post WHERE Posts_post.post_status = 1 ORDER BY id DESC")

    page_num = request.GET.get('page',1)
    paginator = Paginator(recent_posts,6)
    recent_posts = paginator.page(page_num)

    most_views = post.objects.raw("SELECT * FROM Posts_post WHERE Posts_post.post_status = 1 ORDER BY post_view DESC LIMIT 3")

    all_cat = Categories.objects.raw("SELECT count(*) as count_post,Categories_categories.*  FROM Posts_post JOIN Categories_categories on Categories_categories.id = Posts_post.cat_id_id GROUP by Categories_categories.id LIMIT 6")

    data = {
        'most_pupolar' : most_pupolar,
        'recent_posts' : recent_posts,
        'most_views' : most_views,
        'all_cat' : all_cat,
    }

    return render(request,"index.html",data)

def contact(request):
    if request.session.get('email') == None:
        messages.warning(request,"You Must Login In")
        return render(request,'signin.html')
    elif request.method == 'POST':
        Cust_send = request.POST['id']
        message_send = request.POST['message']
        flag_error = False

        if(len(message_send) < 8):
            flag_error = True
            messages.info(request,"Message Less Than 8 Char")

        if(flag_error):
            return redirect("/contact")
        else:
            customer_send = Customer.objects.get(id=Cust_send)
            message.objects.create(meg_details=message_send,cust_id=customer_send)
            message_success = {
                    'success' : 'Message Send Successfully'
                }
            return render(request,'contact.html',message_success)

    else:
        customer_contact =  Customer.objects.get(user_email=request.session.get('email'))
        messages_send = message.objects.raw(f"SELECT * FROM Customer_message JOIN Customer_reply on Customer_reply.meg_id_id == Customer_message.id WHERE Customer_message.cust_id_id = {customer_contact.id}")

        data = {
            'customer_contact' : customer_contact,
            'messages_send' : messages_send,
        }
        return render(request,"contact.html",data)

def about(request):
    return render(request,"about.html")

def singup(request):
    if(request.method == "POST"):
        flag_erros = False
        fname = request.POST["firstName"]
        lname = request.POST["lastName"]
        email = request.POST["email"]
        password = request.POST["password"]
        conpassword = request.POST["confirmPassword"]

        if(len(fname) < 3):
            messages.info(request,"Frist Name Must Greater Than 3 Char")
            flag_erros = True
        if(len(lname) < 3):
            messages.info(request,"Last Name Must Greater Than 3 Char")
            flag_erros = True
        if(password != conpassword):
            messages.info(request,"Password Not Match")
            flag_erros = True

        cust =Customer.objects.filter(user_email=email).exists()
        if cust:
            messages.info(request,'Email Already Exist')
            flag_erros = True


        if(flag_erros):
            return redirect("/singup")
        else:
            newcust = Customer.objects.create(user_first=fname,user_last=lname,user_email=email,user_pass=password)
            if(newcust):
                message_success = {
                    'success' : 'Customer Register Successfully'
                }
                return render(request,'signup.html',message_success)
    else:
        return render(request,"signup.html")

def singin(request):

    if(request.method=='POST'):
        email = request.POST["email"]
        password = request.POST["password"]

        flag = Customer.objects.filter(user_email=email,user_pass=password).exists()
        if(flag):
            info_customer = Customer.objects.get(user_email=email)
            name = info_customer.user_first + '.' + info_customer.user_last[0].upper()
            request.session["email"] = email
            request.session["password"] = password
            request.session['name'] = name
            request.session['id'] = info_customer.id
            return redirect('/home')
        else:
            messages.info(request,"Error in Email Or Password")
            return render(request,'signin.html')
    else:
        return render(request,"signin.html")

def logout(request):
    request.session.clear()
    return redirect('/home')

def search(request):
    keyword = request.GET['search']
    all_post = post.objects.raw(f"SELECT * FROM Posts_post WHERE Posts_post.post_status = 1 AND Posts_post.post_title like '%{keyword}%'")

    page_num = request.GET.get('page',1)
    paginator = Paginator(all_post,6)
    all_post = paginator.page(page_num)

    data = {
        'keyword': keyword,
        'all_post': all_post,
    }
    return render(request,'search.html',data)

def post_single(request,post_id):

    if request.method == 'POST':

        my_post = post.objects.get(id=post_id)

        post_comment = post.objects.get(id=request.POST['post_id'])

        customer_comment = Customer.objects.get(user_email=request.session.get('email'))

        com_details = request.POST['com_details']

        comment.objects.create(com_details=com_details,post_id=post_comment,
        cust_id=customer_comment,com_status=0)


        return redirect(f'/post/{my_post.id}')

    else:
        my_post = post.objects.get(id=post_id)
        post.objects.filter(id=post_id).update(post_view=my_post.post_view+1)
        post_comment = comment.objects.filter(post_id=my_post).filter(com_status=1)
        data = {
            'my_post' : my_post,
            'post_comment' : post_comment
        }
        if request.session.get('email'):
            customer_comment = Customer.objects.get(user_email=request.session.get('email'))
            post.objects.filter(id=post_id).update(post_view=my_post.post_view+1)
            post_comment = comment.objects.filter(post_id=my_post).filter(com_status=1)
            post_comment_non_active = comment.objects.filter(post_id=my_post).filter(com_status=0).filter(cust_id=customer_comment)
            data = {
                'my_post' : my_post,
                'post_comment' :post_comment,
                'post_comment_non_active' : post_comment_non_active
            }
        return render(request,'post.html',data)

def cat_post(request,cat_id):
    category = Categories.objects.get(id=cat_id)
    posts = post.objects.filter(cat_id=category).filter(post_status=1)

    page_num = request.GET.get('page',1)
    paginator = Paginator(posts,6)
    posts = paginator.page(page_num)

    data = {
        'category' : category,
        'posts' : posts,
    }
    return render(request,"categories_post.html",data)

def change_pass(request):
    if request.session.get('email') == None:
        return redirect("/home")
    else:
        if request.method == 'POST':
            flag = False
            password = request.POST['password']
            new_password = request.POST['new_password']
            new_password_again = request.POST['new_password_again']

            print(password)
            print(new_password)
            print(new_password_again)
            print(request.session.get('password'))
            print(request.session.get('email'))
            print(request.session.get('id'))

            if password != request.session.get('password'):
                flag = True
                messages.info(request,"Old Password is not Correct")

            if new_password != new_password_again:
                flag = True
                messages.info(request,"Password Don't Matching")

            if(flag):
                return redirect('/change_password')
            else:
                new_password = request.POST['new_password']
                Customer.objects.filter(id=request.session.get('id')).update(user_pass=new_password)
                # Customer.objects.raw(f"Update Customer_Customer set user_pass = {password} Where id = 2")
                request.session["password"] = password
                context = {
                    'success' : "password Change Successfully"
                }
                return render(request,'change_password.html',context)
        else:
            return render(request,'change_password.html')