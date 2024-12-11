# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.contrib.auth.models import Group
#
# # Signal handler for creating default groups
# @receiver(post_migrate)
# def create_default_groups(sender, **kwargs):
#     # Create default groups if they don't exist
#     Group.objects.get_or_create(name='Admin')
#     Group.objects.get_or_create(name='Manager')
#     Group.objects.get_or_create(name='Staff')