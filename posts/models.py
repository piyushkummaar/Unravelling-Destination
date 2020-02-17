from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid

User = get_user_model()


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'PostView'
        verbose_name_plural = 'Postviews'
        db_table = 'tbl_postview'
        managed = True

    def __str__(self):
        return self.user.username


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        db_table = 'tbl_author'
        managed = True

    def __str__(self):
        return self.user.username
    


class Category(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'tbl_category'
        managed = True

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        db_table = 'tbl_comment'
        managed = True

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    # comment_count = models.IntegerField(default = 0)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Add Blog'
        db_table = 'tbl_post'
        managed = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'pk': self.pk
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

class ContactUs(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        db_table = 'tbl_contactus'
        managed = True

    def __str__(self):
        return self.fname + '-  ' +self.email
    
    
class Signup(models.Model):
    email = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
        db_table = 'tbl_newsletter'
        managed = True

    def __str__(self):
        return self.email
    
    
class AllaboutSikkim(models.Model):
    bg_image = models.ImageField() 
    bg_heading = models.CharField(max_length=10)
    heading1 =  models.TextField()
    heading2 = models.TextField()
    image1 = models.ImageField()
    sub_heading1 = models.TextField()
    image2 = models.ImageField()
    sub_heading2 = models.TextField()
    heading3 = models.TextField()
    
    class Meta:
        verbose_name = 'All About Sikkim'
        verbose_name_plural = 'Add About Sikkim'
        db_table = 'tbl_aboutsikkim'
        managed = True

    def __str__(self):
        return self.bg_heading
    
    def get_absolute_url(self):
        return reverse('sikkim', kwargs={
            'pk': self.pk
        })
