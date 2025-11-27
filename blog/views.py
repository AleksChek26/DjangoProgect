from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from .models import BlogPost
from .forms import BlogPostForm

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Выводим только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)



class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Увеличиваем счётчик просмотров
        obj.views += 1
        obj.save()

        # Проверка на 100+ просмотров (дополнительное задание)
        if obj.views >= 100:
            self.send_achievement_email(obj)

        return obj

    def send_achievement_email(self, post):
        send_mail(
            subject='Поздравляем! Статья достигла 100 просмотров!',
            message=f'Статья "{post.title}" набрала 100+ просмотров!\n\nURL: {self.request.build_absolute_uri()}',
            from_email='no-reply@yourdomain.com',
            recipient_list=['your-email@example.com'],  # замените на свой email
            fail_silently=False,
        )



class PostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    success_url = '/blog/'  # можно заменить на reverse()




class PostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        # Перенаправление на страницу статьи после редактирования
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})




class PostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/blog/'
