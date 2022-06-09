from email.mime import image
from django.core.paginator import Paginator
from django.views.generic import ListView
from members.models import Powerteam, userProfile
from .models import Answers, Questions
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from .forms import AnswerForm, QuestionForm
# Create your views here.

class PTlist(ListView):
    template_name = "posts/home.html"
    context_object_name = "posts"
    # Hàm này sẽ trả về dữ liệu của powerteam và question
    def get_queryset(self):
        data = {}
        idols = userProfile.objects.order_by('-likes')[0:5]
        data['powerteams'] = Powerteam.objects.all()
        data['numberOfQuestions'] = Questions.objects.count()
        data['idolsProfile'] = idols
        data['recent_activites'] = Questions.objects.order_by('-create_at')[0:8]

        # phân trang cho question
        qs = Paginator(Questions.objects.all(),5)
        try:
            page_number  = int(self.request.GET['page'])
        except:
            page_number = 1
        page_range = qs.get_elided_page_range(number = page_number,on_each_side=2,on_ends=1)
        data['questions']  = qs.get_page(page_number)
        data['page_range'] = page_range      
        return data


class PTDeatil(ListView):
    template_name = "posts/home.html"
    context_object_name = "posts"
    
    # Hàm này sẽ trả về dữ liệu của powerteam và question
    def get_queryset(self):
        data = GetData()
        pk = self.kwargs.get('pk')
        # phân trang cho question
        try:
            questionOfPowerteam  =  Powerteam.objects.get(pk=pk).questions_set.all()
        except:
            # print(HttpResponseRedirect(reverse("post:home")))
            # return HttpResponseRedirect(reverse("post:home"))
            questionOfPowerteam  =  Powerteam.objects.get(pk=1).questions_set.all()


        qs = Paginator(questionOfPowerteam,5)

        try:
            page_number  = int(self.request.GET['page'])
        except:
            page_number = 1

        # Lấy ra dữ liệu trang hiện tại
        data['questions']  = qs.get_page(page_number) 
        # Lấy ra các số trang để hiện thị
        page_range = qs.get_elided_page_range(number = page_number,on_each_side=2,on_ends=1)
        data['page_range'] = page_range

        return data


def question_detail(request,pk):
        data = GetData()
        try:
           question = Questions.objects.get(pk=pk)
        except:
            question = Questions.objects.get(pk=1)
        data['question'] = question 
        
        answers = question.answers_set.all()
        qs = Paginator(answers,5)

        try:
            page_number  = int(request.GET['page'])
        except:
            page_number = 1

        # Lấy ra dữ liệu trang hiện tại
        data['answers']  = qs.get_page(page_number)
        # Lấy ra các số trang để hiện thị
        page_range = qs.get_elided_page_range(number = page_number,on_each_side=2,on_ends=1)
        data['page_range'] = page_range
        form = AnswerForm(None)
        return render(request,'posts/question_detail.html',{'posts':data,'form':form})


def save_answer(request,pk):
    # Nếu chưa đăng nhập thì sẽ không cho tạo mà đẩy về home
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("post:home"))
    if request.method == 'POST':
        user = request.user
        qs = Questions.objects.get(pk=pk)
        form = AnswerForm(request.POST,request.FILES)
        if form.is_valid():
            ans = Answers.objects.create(user = user,question = qs,images = request.FILES.get('images') ,answer = request.POST['answer'])
    return HttpResponseRedirect(reverse("post:question-detail",args=(pk,)))


# Get catagory data, rank data, recent_activities data
def GetData():
    data = {}
    # dùng rank
    idols = userProfile.objects.order_by('-likes')[0:5]
    data['idolsProfile'] = idols

    # Dùng cho catagory
    data['powerteams'] = Powerteam.objects.all()
    data['numberOfQuestions'] = Questions.objects.count()

    # Dùng cho hành động gần đây
    data['recent_activites'] = Questions.objects.order_by('-create_at')[0:8]

    return data



def AnswerUpdateView(request,pk):
    # Nếu chưa đăng nhập thì sẽ không cho cập nhật mà đẩy về home
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("post:home"))
    data = GetData()
    answer = Answers.objects.get(pk=pk)
    # dường dẫn quay trở lại trang trước
    path = request.GET.get('next')
    if request.method == 'POST':
        updateForm = AnswerForm(request.POST,request.FILES,instance = answer)
        if updateForm.is_valid():
            updateForm.save()
            if path == None:
                # Nếu người cố tình loại bỏ path thì đưa người dùng về trang chủ
                return HttpResponseRedirect(reverse("post:home"))
            return HttpResponseRedirect(path)

    return render(request,'posts/AnswerUpdateForm.html',{"posts":data,'answer':answer})

def QuestionUpdateView(request,pk):
    # Nếu chưa đăng nhập thì sẽ không cho cập nhật mà đẩy về home
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("post:home"))
    data = GetData()
    question = Questions.objects.get(pk=pk)
    # dường dẫn quay trở lại trang trước
    question1 = QuestionForm(instance = question) 
    path = request.GET.get('next')
    if request.method == 'POST':
        updateForm = QuestionForm(request.POST,request.FILES,instance = question)
        if updateForm.is_valid():
            updateForm.save()
            if path == None:
                # Nếu người cố tình loại bỏ path thì đưa người dùng về trang chủ
                return HttpResponseRedirect(reverse("post:home"))
            return HttpResponseRedirect(path)
    return render(request,'posts/QuestionUpdateForm.html',{"posts":data,'questionForm':question1,'question':question})


def DeleteAnswer(request,pk):
    # Nếu chưa đăng nhập thì sẽ không cho xoá mà đẩy về home
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("post:home"))
    data = GetData()
    # Lấy đường dẫn nếu không có mặc định chuyển về home
    path = request.GET.get('next')
    if path == None:
        path = reverse("post:home")
    
    if request.method == 'POST':
        answer = get_object_or_404(Answers,pk=pk)
        answer.delete()
        return HttpResponseRedirect(path)
    
    
    return render(request,'posts/deleteAnswer.html',{'posts':data,'path':path})

def DeleteQuestion(request,pk):
    # Nếu chưa đăng nhập thì sẽ không cho xoá mà đẩy về home
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("post:home"))
    data = GetData()
    
    path = reverse("post:home")
    
    if request.method == 'POST':
        question = get_object_or_404(Questions,pk=pk)
        question.delete()
        return HttpResponseRedirect(path)
    
    
    return render(request,'posts/deleteQuestion.html',{'posts':data,'path':path})

def CreateQuestion(request):
    # Nếu chưa đăng nhập thì sẽ không cho tạo mà đẩy về home
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("post:home"))
    data = GetData()

    # nếu người dùng cô tính xoá đường dẫn thì sẽ chuyển về home
    try:
        path = request.GET['next']
    except:
        path = reverse('post:home')
    if request.method == 'POST':
        QuestionCreateForm = QuestionForm(request.POST,request.FILES)

        if QuestionCreateForm.is_valid():
            # Get data 
            powerteamID = request.POST.get('powerteam')
            powerteam = Powerteam.objects.get(pk=powerteamID)
            title = request.POST.get('title')
            description = request.POST.get('description')
            images = request.FILES.get('images')
            # create data in database
            Questions.objects.create(user = request.user,powerteam = powerteam,title = title,description = description,images=images)

            return HttpResponseRedirect(path)
     # tạo form gửi lên
    QuestionCreateForm = QuestionForm(None)
    return render(request,'posts/QuestionCreateForm.html',{'QuestionCreateForm':QuestionCreateForm,'posts':data})

# Tìm kiếm theo câu hỏi

def SearchQuestion(request):
    # Nếu người dùng cố tính sửa lại phương thức
    if request.method =="POST":
        return HttpResponseRedirect(reverse("post:home"))
    # lấy ra catagory,rank,recently_activity
    data = GetData()
    # Get question
    question_name = request.GET.get('q')
    if question_name == None:
        question_name = ''
    # Nêu mà người dùng k nhập
 
    question = Questions.objects.filter(title__icontains = question_name)
    # 1 trang có tối đa 5 câu hỏi
    qs = Paginator(question,5) 
    # Kiểm tra ngoại lệ
    try:
        page_number  = int(request.GET['page'])
    except:
        page_number = 1
     # Lấy ra dữ liệu trang mà người dùng muốn xem
    data['questions']  = qs.get_page(page_number)
    # Lấy ra các số trang để hiện thị
    page_range = qs.get_elided_page_range(number = page_number,on_each_side=2,on_ends=1)
    data['page_range'] = page_range

    return render(request,'posts/QuestionSearchListView.html',{'posts':data,"query_name":question_name})

    


    

