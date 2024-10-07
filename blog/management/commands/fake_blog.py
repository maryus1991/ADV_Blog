from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User
from ...models import Post, PostsComment

import random

class Command(BaseCommand):
    help = """
    insert fake data for posts models 
    """
    def add_arguments(self, parser):
        """
        for get email objects in terminal and get or create super user   
        """
        parser.add_argument("email", type=str)

    def handle(self,*arg, **kwargs):
        """
        create post and comment for it 
        """
        faker = Faker(['fa_IR'])
        email = kwargs.get('email')
        user = User.objects.get_or_create(
                                        is_active=True, 
                                        is_staff=True, 
                                        is_superuser=True, 
                                        is_verified=True,
                                        email=email
                                        )
        if user[1]:
            user[0].set_password = "123"
            user[0].save()

        for _ in range(10):
            # for create posts
            post = Post.objects.create(
                author = user[0],
                image='assets/images/featured/img-1.jpg',
                title = faker.paragraph(1),
                text = faker.paragraph(10),
            )
            for _ in range(5):
                # create comment for this post 
                comment = PostsComment.objects.create(
                    full_name=faker.name()
                    ,email=faker.email()
                    ,comment=faker.paragraph(2)
                    ,post_id=post.id

                )

                # create sub comment for this  comment  

                PostsComment.objects.create(
                    full_name=faker.name()
                    ,email=faker.email()
                    ,comment=faker.paragraph(2)
                    ,post=post
                    ,parent=comment
                )
        print('done!!!')
        


