from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    otp = models.CharField(max_length=100, blank=True, null=True)
    refresh_token = models.CharField(max_length=1000, blank=True, null=True)

    USERNAME_FIELD = 'email' # The field that will be used as the unique identifier for a user
    REQUIRED_FIELDS = ['username', 'full_name'] # The fields that are required to create a user

    def __str__(self):
        """
        Return a string representation of the user.

        This string is used to represent the user in the Django admin interface,
        and anywhere else that Django needs a string representation of a user.

        :return: A string representation of the user
        :rtype: str
        """
        return self.email





class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.FileField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the user.

        If the user has a full name set, this will be returned.
        Otherwise, the username of the associated user will be returned.

        :return: A string representation of the user
        :rtype: str
        """
        if self.full_name:
            return self.full_name
        else:
            return str(self.user.full_name)



    def save(self, *args, **kwargs):
        """
        Save the profile to the database.

        If the profile's full_name is not set, it will be set to the username
        of the associated user.

        :param \*args: Additional positional arguments to be passed to the
            parent class's ``save()`` method.
        :param \*\*kwargs: Additional keyword arguments to be passed to the
            parent class's ``save()`` method.
        :return: None
        :rtype: NoneType
        """

        if self.full_name is None or self.full_name == "":
            self.full_name = self.user.full_name
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a Profile instance when a new CustomUser is created.

    This function listens to the `post_save` signal of the `CustomUser` model.
    If a new `CustomUser` instance is created, it creates a corresponding
    `Profile` instance associated with that user.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance of the model being saved.
    :param created: Boolean; True if a new record was created.
    :param \*\*kwargs: Additional keyword arguments.
    :return: None
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    """
    Signal receiver that saves the Profile associated with a CustomUser
    when it is updated.

    This function listens to the `post_save` signal of the `CustomUser` model.
    When a `CustomUser` instance is updated, it saves the associated
    `Profile` instance.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance of the model being saved.
    :param **kwargs: Additional keyword arguments.
    :return: None
    """
    instance.profile.save()



