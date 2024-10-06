from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User
from ...models import Post

import random

class Command(BaseCommand):
    help = """
    insert fake data for posts models 
    """
    pass