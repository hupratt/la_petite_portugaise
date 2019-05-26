
from posts.models import Post

def create_connection_postgres():
    import psycopg2
    import os
    try:
        if os.environ.get('DJANGO_DEVELOPMENT') is not None:
            connection = psycopg2.connect(user=os.environ.get('dbuser'),
                                          password=os.environ.get(
                                              'dbpassword'),
                                          host=os.environ.get('hostipdev'),
                                          port=os.environ.get('pnumber'),
                                          database='lapetiteportugaise')
        else:
            connection = psycopg2.connect(user=os.environ.get('dbuser'),
                                          password=os.environ.get(
                                              'dbpassword'),
                                          host=os.environ.get('hostip'),
                                          port=os.environ.get('pnumber'),
                                          database='lapetiteportugaise')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return cursor, connection


def translate(posts, lang):
    c, _ = create_connection_postgres()
    def werk(post):
        c.execute("SELECT translation FROM klingon_translation WHERE object_id = %s AND lang = %s AND field = %s",
                    (post.pk, lang, 'title'))
        fetch = c.fetchone()
        if fetch is not None and post.title is not None and type(fetch) is tuple:
            post.title = ''.join(fetch)
        c.execute("SELECT translation FROM klingon_translation WHERE object_id = %s AND lang = %s AND field = %s",
                    (post.pk, lang, 'content'))
        fetch = c.fetchone()
        if fetch is not None and post.content is not None and type(fetch) is tuple:
            post.content = ''.join(fetch)
    if isinstance(posts, Post):
        werk(posts)
    else:
        for post in posts:
            werk(post)     
    return posts

