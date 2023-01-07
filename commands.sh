source ./venv/bin/activate

pip install Django~=4.1.0

python -m django --version

django-admin startproject mysite

cd mysite
python manage.py migrate
#Operations to perform:
#  Apply all migrations: admin, auth, contenttypes, sessions
#Running migrations:
#  Applying contenttypes.0001_initial... OK
#  Applying auth.0001_initial... OK
#  Applying admin.0001_initial... OK
#  Applying admin.0002_logentry_remove_auto_add... OK
#  Applying admin.0003_logentry_add_action_flag_choices... OK
#  Applying contenttypes.0002_remove_content_type_name... OK
#  Applying auth.0002_alter_permission_name_max_length... OK
#  Applying auth.0003_alter_user_email_max_length... OK
#  Applying auth.0004_alter_user_username_opts... OK
#  Applying auth.0005_alter_user_last_login_null... OK
#  Applying auth.0006_require_contenttypes_0002... OK
#  Applying auth.0007_alter_validators_add_error_messages... OK
#  Applying auth.0008_alter_user_username_max_length... OK
#  Applying auth.0009_alter_user_last_name_max_length... OK
#  Applying auth.0010_alter_group_name_max_length... OK
#  Applying auth.0011_update_proxy_permissions... OK
#  Applying auth.0012_alter_user_first_name_max_length... OK
#  Applying sessions.0001_initial... OK

python manage.py runserver
#Watching for file changes with StatReloader
#Performing system checks...
#
#System check identified no issues (0 silenced).
#December 30, 2022 - 11:02:41
#Django version 4.1.4, using settings 'mysite.settings'
#Starting development server at http://127.0.0.1:8000/
#Quit the server with CONTROL-C.

python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings

python manage.py startapp blog

python manage.py shell

python manage.py makemigrations blog
#Migrations for 'blog':
#  blog/migrations/0001_initial.py
#    - Create model Post
#    - Create index blog_post_publish_bb7600_idx on field(s) -publish of model post

python manage.py sqlmigrate blog 0001
#BEGIN;
#--
#-- Create model Post
#--
#CREATE TABLE "blog_post" (
#  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#  "title" varchar(250) NOT NULL,
#  "slug" varchar(250) NOT NULL,
#  "body" text NOT NULL,
#  "publish" datetime NOT NULL,
#  "created" datetime NOT NULL,
#  "updated" datetime NOT NULL,
#  "status" varchar(2) NOT NULL,
#  "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
#);
#--
#-- Create index blog_post_publish_bb7600_idx on field(s) -publish of model post
#--
#CREATE INDEX "blog_post_publish_bb7600_idx" ON "blog_post" ("publish" DESC);
#CREATE INDEX "blog_post_slug_b95473f2" ON "blog_post" ("slug");
#CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
#COMMIT;
## The exact output depends on the database you are using. The preceding output is generated for SQLite.

python manage.py migrate
#Operations to perform:
#  Apply all migrations: admin, auth, blog, contenttypes, sessions
#Running migrations:
#  Applying blog.0001_initial... OK

python manage.py createsuperuser
#Username (leave blank to use 'xiaoqinglee'):
#Email address:
#Password:
#Password (again):
#Error: Blank passwords aren't allowed.
#Password:
#Password (again):
#Error: Your passwords didn't match.
#Password:
#Password (again):
#The password is too similar to the username.
#Bypass password validation and create user anyway? [y/N]: y
#Superuser created successfully.

python manage.py runserver

python manage.py shell
#>>> from django.contrib.auth.models import User
#>>> from blog.models import Post
#>>> user = User.objects.get(username='xiaoqinglee')
#>>> post = Post(title='Another post',
#... slug='another-post',
#... body='Post body.',
#... author=user)
#>>> post.save()

#Post.objects.create(title='One more post',
#slug='one-more-post',
#body='Post body.',
#author=user)

#>>> post.title = 'New title'
#>>> post.save()

#>>> all_posts = Post.objects.all()
#>>> all_posts
#<QuerySet [<Post: One more post>, <Post: Another post new title>, <Post: Who is John Wick?>]>

#>>> Post.objects.filter(publish__year=2023, author__username='xiaoqinglee')

#>>> Post.objects.filter(publish__year=2023) \
#>>> .filter(author__username='xiaoqinglee')

#Queries with field lookup methods are built using two underscores, for example, publish__
#year, but the same notation is also used for accessing fields of related models, such as
#author__username.

#>>> Post.objects.filter(publish__year=2023).exclude(title__startswith='Who')
#<QuerySet [<Post: One more post>, <Post: Another post new title>]>

#>>> Post.objects.order_by('title')

#>>> Post.objects.order_by('-title')

#>>> post = Post.objects.get(id=1)
#>>> post.delete()

#>>> all_posts = Post.objects.all()
#>>> all_posts
#<QuerySet [<Post: One more post>, <Post: Another post new title>, <Post: Who is John Wick?>]>
#>>> all_posts[0].id
#3
#>>> all_posts[0].delete()
#(1, {'blog.Post': 1})
#>>> Post.objects.all()
#<QuerySet [<Post: Another post new title>, <Post: Who is John Wick?>]>
#>>>

#Creating a QuerySet doesn’t involve any database activity until it is evaluated.
#
#QuerySets are only evaluated in the following cases:
#• The first time you iterate over them
#• When you slice them, for instance, Post.objects.all()[:3]
#• When you pickle or cache them
#• When you call repr() or len() on them
#• When you explicitly call list() on them
#• When you test them in a statement, such as bool(), or, and, or if

python manage.py shell
#>>> from django.contrib.auth.models import User
#>>> from blog.models import Post
#>>> Post.published.filter(title__startswith='Who')

python manage.py runserver

python manage.py shell
#>>> from blog.models import Post
#>>> post = Post.objects.get(id=1)
#>>> post
#<Post: Who is John Wick?>
#>>> post.tags.all()
#<QuerySet []>
#>>> post.tags.add('movie', 'gun', 'man')
#>>> post.tags.all()
#<QuerySet [<Tag: gun>, <Tag: movie>, <Tag: man>]>
#>>> post.tags.remove('gun')
#>>> post.tags.all()
#<QuerySet [<Tag: movie>, <Tag: man>]>
#>>>
