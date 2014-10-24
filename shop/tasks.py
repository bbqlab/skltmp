from __future__ import absolute_import
from celery import Celery

import os
import sys
import requests
import MySQLdb as mdb

path = '/home/bbq/Git'
if path not in sys.path:
    sys.path.append(path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillup.settings')

from django.conf import settings

import os

app = Celery('skillup', backend='amqp', broker=settings.BROKER_URL, include=['skillup.shop.tasks'])
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


LHC_PATH = '/opt/livehelperchat/lhc_web'
LHC_DASHBOARD_PATH = '/var/www/dashboard.skillup.it'
LHC_DASHBOARD_URL = 'http://dashboard.skillup.it'
LHC_SETTINGS_PATH = "%s/settings/settings.ini.php" % LHC_PATH 

@app.task
def add(x,y):
    return x + y

@app.task
def sleeptask(i):
    from time import sleep
    sleep(i)
    return i

@app.task(name='shop.tasks.deploy_lhc')
def deploy_lhc(user_id, domain, password, plan='Trial'):
    print "INSIDE CREATING INSTANCE"
    print "user %s domain %s plan %s" % (user_id, domain, plan)
    manager = DeploymentManager(domain, user_id, password, plan)
    try:
        manager.deploy()
    except Exception, e:
        print "ERROR: %s" % e



class DeploymentManager:
    def __init__(self, domain, user_id, password, plan):
        self.user_id = user_id
        self.domain = domain
        self.plan = plan
        self.password = password

    def deploy(self):
        self.copy_codebase()
        self.create_db()
        self.install_lhc()
    
    def copy_codebase(self):
        try:
            dst = "%s/%s" % (LHC_DASHBOARD_PATH, self.domain)
            copytree(LHC_PATH, dst)
            os.system("chgrp -R www-data %s" % dst)
        except Exception, e:
            raise e

    

    def create_db(self):
        connection = mdb.connect(settings.LHC_DASHBOARD_DBHOST, 
                                 settings.LHC_META_DBUSER,
                                 settings.LHC_META_DBPASS)
        
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE %s" % self.domain)
        print "CREATE DATABASE %s" % self.domain
        cursor.execute("GRANT ALL PRIVILEGES ON `%s`.* to '%s'@'localhost' IDENTIFIED BY '%s'" %
                        (self.domain,
                        settings.LHC_DASHBOARD_DBUSER,
                        settings.LHC_DASHBOARD_DBPASS))

    def install_lhc(self):
        url = "%s/%s/index.php/site_admin/install/install" % (LHC_DASHBOARD_URL, self.domain)
        print settings.BROKER_URL        
        # first step: db values
        data = { "DatabaseUsername": settings.LHC_DASHBOARD_DBUSER,
                 "DatabasePassword": settings.LHC_DASHBOARD_DBPASS,
                 "DatabaseHost": settings.LHC_DASHBOARD_DBHOST,
                 "DatabasePort": "3306",
                 "DatabaseDatabaseName": self.domain}

        print "make call to %s/2" %url
        print data
        requests.post("%s/2" % url, data=data)

        data = {"AdminUsername":"support",
                "AdminPassword":"antani",
                "AdminPassword1":"antani",
                "AdminEmail":"test@test.it",
                "AdminName":"Mario",
                "AdminSurname":"Rossi",
                "DefaultDepartament": "Support"
                }
        print "make call to %s/3" %url
        print data
        requests.post("%s/3" % url, data=data)

        post_install_url = "%s/%s/index.php/site_admin/postinstall/postinstall" % (LHC_DASHBOARD_URL, self.domain)
        print "posting to %s" % post_install_url
        data = {'title': self.domain.capitalize(), 
                'secret': settings.LHC_SECRET,
                'password': '',
                'user_id': ''}
        requests.post(post_install_url, data=data)



def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue

        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)

        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                os.symlink(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    if errors:
        raise Error(errors)





