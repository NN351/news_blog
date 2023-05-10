from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


from apps.blog.models import Post
from apps.accounts.models import User





@receiver(post_save, sender=Post)
def email_notification(sender, instance, created, **kwargs):
    if created: # Если был создан абсолютно новый пост.
        DOMAIN = "localhost:8000"
        email_subject = "Новые посты на News_Blog: Будьте в курсе последних событий!"
        posts = Post.objects.filter(is_active=True).order_by("-created_at")[:3]
        message = render_to_string("new_posts_email.html", {"posts":posts, "domain":DOMAIN})
        to_emails = User.objects.all().values_list("email", flat=True)
        email = EmailMessage(email_subject, message, to=to_emails)
        email.content_subtype = "html"
        email.send()