from django.db import models
from userauth.models import CustomUser, Profile
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone

LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('fr', 'French'),
        ('es', 'Spanish'),
    )

LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
)

TEACHER_STATUS = (
    ("Draft", "Draft"),
    ("Published", "Published"),
    ("Disabled", "Disabled"),
)

PLATFORM_STATUS = (
    ("Draft", "Draft"),
    ("Published", "Published"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("Pending", "Pending"),
)

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.FileField(default='default.jpg', upload_to='course-file', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.full_name

    def students(self):
        """
        Return a queryset of CartOrderItem objects associated with this teacher.

        This method filters and retrieves all order items where the teacher
        is the current instance, allowing access to all students enrolled
        through the teacher's courses.

        :return: Queryset of CartOrderItem objects for this teacher
        :rtype: QuerySet
        """
        return CartOrderItem.objects.filter(teacher=self)

    def courses(self):

        """
        Return a queryset of Course objects associated with this teacher.

        This method filters and retrieves all courses where the teacher
        is the current instance, allowing access to all courses taught
        by the teacher.

        :return: Queryset of Course objects for this teacher
        :rtype: QuerySet
        """
        return Course.objects.filter(teacher=self)


    def reviews(self):
        """
        Return the count of Course objects for this teacher.

        This method calculates and returns the number of courses
        associated with the current teacher instance, providing
        an overview of the teacher's course load.

        :return: Count of Course objects for this teacher
        :rtype: int
        """
        return Course.objects.filter(teacher=self).count()

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(default='category.jpg', upload_to='course-file', null=True, blank=True)
    slug = models.SlugField(unique=True,null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def course_count(self):
        return Course.objects.filter(category=self).count()


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    image = models.FileField(default='course.jpg', upload_to='course-file', null=True, blank=True)
    slug = models.SlugField(unique=True,null=True, blank=True)
    file = models.FileField(upload_to='course-file', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, default='en')
    level = models.CharField(choices=LEVEL_CHOICES, max_length=12, default='beginner')
    platform_status = models.CharField(choices=PLATFORM_STATUS, max_length=10, default='Published')
    teacher_course_status = models.CharField(choices=TEACHER_STATUS, max_length=10, default='Published')
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True, max_length=20, alphabet="1234567890", length=6)
    date = models.DateTimeField(default=timezone.now)



    class Meta:
        verbose_name_plural = 'Courses'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

