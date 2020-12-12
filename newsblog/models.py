from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import datetime
# Create your models here.

class MyuserManager(BaseUserManager):
    def create_user(self, email, name, mobile_number, password=None):
        
        if not email:
            raise ValueError('User must have a valid email address')

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            mobile_number = mobile_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name,  mobile_number, password=None):
        
        user = self.create_user(
            email,
            name = name,
            password=password,
            mobile_number=mobile_number,
        )
        user.is_admin = True
        user.save(using = self._db)
        return user
        
class MyUser(AbstractBaseUser):

    email = models.EmailField(verbose_name='email_address', max_length=255, unique=True)
    name = models.CharField(verbose_name='name', max_length=255,)
    mobile_number = models.CharField(max_length=10, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyuserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin    

class profilepic(models.Model):
    user = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    propic = models.ImageField(upload_to="newsblog/media/")

class article(models.Model):
    user = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    headline = models.CharField(max_length=255)
    article_image = models.ImageField(upload_to="newsblog/media/article_img/")
    content = models.TextField(max_length=1000)
    timedate = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title + " by " + self.user.name

class comments(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(article, null=True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=255)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timedate = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment + " by " + self.user.name
    
    