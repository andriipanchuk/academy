import os 
from django.contrib.auth.models import User
import logging

def init_script():
    ## Init script which is responsible to create admin user
    if os.environ.get('ADMIN_USER') and os.environ.get('ADMIN_PASSWORD'):

        ## If table is exist in system 
        if db_table_exists('auth_user'):
            
            ## IF user not created in system init script will go ahead and try to create
            if not User.objects.filter(username=os.environ.get('ADMIN_USER')).exists():
                super_user = User.objects.create_user(os.environ.get('ADMIN_USER'), password=os.environ.get('ADMIN_PASSWORD'))
                super_user.is_superuser=True
                super_user.is_staff=True
                super_user.save()
                logging.warning(f"admin user <{os.environ.get('ADMIN_USER')}> has been created !!")


def db_table_exists(table_name, cursor=None):
    ## Function to check table exist or not
    try:
        
        ## Trying to connect to DB 
        if not cursor:
            from django.db import connection
            cursor = connection.cursor()
        if not cursor:
            raise Exception
        return table_name in connection.introspection.table_names()
    except:
        raise Exception("unable to determine if the table '%s' exists" % table_name)