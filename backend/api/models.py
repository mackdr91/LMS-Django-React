from datetime import timedelta
from django.db import models
from userauth.models import CustomUser, Profile
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from moviepy.editor import VideoFileClip
import math

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

    def students(self):
        """
        Return a queryset of enrolled students in the course.

        This method filters and retrieves all enrolled courses associated
        with the course instance, providing access to all students that are
        enrolled in the course.

        :return: A queryset of EnrolledCourse objects
        :rtype: QuerySet
        """
        return EnrolledCourse.objects.filter(course=self)

    def curriculum(self):
        """
        Return a queryset of VariantItem objects related to the course.

        This method filters and retrieves all variant items associated
        with the course instance, providing access to all curriculum items
        that are part of the course.

        :return: Queryset of VariantItem objects for this course
        :rtype: QuerySet
        """
        return VariantItem.objects.filter(varriant__course=self)

    def lectures(self):
        """
        Return a queryset of VariantItem objects related to the course.

        This method filters and retrieves all variant items associated
        with the course instance, providing access to all lectures
        that are part of the course.

        :return: Queryset of VariantItem objects for this course
        :rtype: QuerySet
        """
        return VariantItem.objects.filter(varriant__course=self)

    def average_rating(self):
        """
        Return the average rating for the course.

        This method aggregates the average of all CourseReview objects
        associated with the current course instance, providing an overview
        of the course's overall rating.

        :return: Average rating for this course
        :rtype: float
        """
        average_rating = Review.objects.filter(course=self, active=True).aggregate(avg_rating=models.Avg('rating'))
        return average_rating['avg_rating']

    def rating_count(self):
        """
        Return the count of CourseReview objects associated with this course.

        This method filters and retrieves all reviews where the course
        is the current instance, allowing access to all reviews for
        the course.

        :return: Count of CourseReview objects for this course
        :rtype: int
        """
        return Review.objects.filter(course=self, active=True).count()


    def reviews(self):
        """
        Return a queryset of CourseReview objects associated with this course.

        This method filters and retrieves all reviews where the course
        is the current instance, allowing access to all reviews for
        the course.

        :return: Queryset of CourseReview objects for this course
        :rtype: QuerySet
        """
        return Review.objects.filter(course=self, active=True)


class Variant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    variant_id = ShortUUIDField(unique=True, max_length=20, alphabet="1234567890", length=6)
    slug = models.SlugField(unique=True,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Variants'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def variant_items(self):
        """
        Return a queryset of VariantItem objects associated with this variant.

        This method filters and retrieves all variant items where the variant
        is the current instance, allowing access to all variant items for
        the variant.

        :return: Queryset of VariantItem objects for this variant
        :rtype: QuerySet
        """
        return VariantItem.objects.filter(variant=self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Variant, self).save(*args, **kwargs)


class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_items')
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='course-file')
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(unique=True, max_length=20, alphabet="1234567890", length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Variant Items'
        ordering = ('title',)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"


    def save(self, *args, **kwargs):
        """
        Save the VariantItem and calculate the duration of the file.

        This method overrides the default save method to calculate the duration
        of the uploaded file and save it in the content_duration field.

        :param \*args: Additional positional arguments to be passed to the parent class's
            ``save()`` method.
        :param \*\*kwargs: Additional keyword arguments to be passed to the parent class's
            ``save()`` method.
        :return: None
        :rtype: NoneType
        """
        super().save(*args, **kwargs)

        if self.file:
            clip = VideoFileClip(self.file.path) # Replace with the path to your video file
            duration_seconds = clip.duration # Get the duration in seconds

            minutes, remainder = divmod(duration_seconds, 60) # 60 seconds in a minute example: 100 seconds = 1 minute and 40 seconds
            minutes = math.floor(minutes) # Convert the minutes to an integer
            seconds = math.floor(remainder) # Convert the seconds to an integer

            duration = f"{minutes:02d}m:{seconds:02d}s" # Format the duration as "mm:ss" example: 1m:40s
            self.content_duration = duration # Save the duration in the content_duration field

            super().save(update_fields=['content_duration']) # Update only the content_duration field
