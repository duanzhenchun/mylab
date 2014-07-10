sed -ie 's#DEBUG = True$#DEBUG = False#g' ./settings.py 
rm static/admin
ln -s $HOME/env/lib/python2.7/site-packages/django/contrib/admin static/

. ~/env/bin/activate
python manage.py collectstatic --noinput
uwsgi --reload uwsgi.pid 
