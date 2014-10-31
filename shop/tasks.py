from __future__ import absolute_import
from celery import Celery

import os
import sys
import requests
import MySQLdb as mdb

path = '/home/jacko/Projects'
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
def deploy_lhc(user_id, domain, firstname, lastname, email, password, plan='Trial'):
    print "INSIDE CREATING INSTANCE"
    print "user %s domain %s plan %s" % (user_id, domain, plan)
    manager = DeploymentManager(domain, firstname, lastname, email, user_id, password, plan)
    try:
        manager.deploy()
    except Exception, e:
        print "ERROR: %s" % e



class DeploymentManager:
    def __init__(self, domain, firstname, lastname, email, user_id, password, plan):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.domain = domain
        self.plan = plan
        self.password = password

    def deploy(self):
        self.copy_codebase()
        self.create_db()
        self.install_lhc()
        self.install_widget()
    
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
        print "Installing lhc"
        url = "%s/%s/index.php/site_admin/install/install" % (LHC_DASHBOARD_URL, self.domain)
        # first step: db values
        data = { "DatabaseUsername": settings.LHC_DASHBOARD_DBUSER,
                 "DatabasePassword": settings.LHC_DASHBOARD_DBPASS,
                 "DatabaseHost": settings.LHC_DASHBOARD_DBHOST,
                 "DatabasePort": "3306",
                 "DatabaseDatabaseName": self.domain}

        requests.post("%s/2" % url, data=data)

        data = {"AdminUsername":self.domain,
                "AdminPassword":'default',
                "AdminPassword1":'default',
                "AdminEmail":self.email,
                "AdminName":self.firstname,
                "AdminSurname":self.lastname,
                "DefaultDepartament": "Supporto"
                }

        requests.post("%s/3" % url, data=data)

        post_install_url = "%s/%s/index.php/site_admin/postinstall/postinstall" % (LHC_DASHBOARD_URL, self.domain)
        data = {'title': self.domain.capitalize(), 
                'secret': settings.LHC_SECRET,
                'password': self.password.split("$")[2],
                'user_id': ''}
        print "posting post_install"
        print data
        requests.post(post_install_url, data=data)

    def install_widget(self):
        print "installing widget"
        connection = mdb.connect(settings.LHC_DASHBOARD_DBHOST, 
                                 settings.LHC_META_DBUSER,
                                 settings.LHC_META_DBPASS,
                                 db=self.domain)
        print "user %s pass %s host %s db %s" % (settings.LHC_DASHBOARD_DBHOST, settings.LHC_META_DBPASS, 
                                                 settings.LHC_META_DBUSER, self.domain)

        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO `lh_abstract_widget_theme` VALUES (1,'Servizio clienti','f6f6f6','000000','e3e3e3','','','','','87c2ced2d45b776b3cd60d3090f11628.png','var/storagetheme/2014y/10/24/1/','','12836d','ffffff','12836d','12836d','16a085','12836d','2c3e50','','','#lhc_container {\r\n  border-radius:0px !important;\r\nwidth:400px;\r\n}\r\n\r\n#lhc_header {\r\n  height:50px;\r\n}','body {\r\n  background-color:#2c3e50;  \r\n  margin:0px !important;\r\n}\r\n\r\n.widget-chat #messages {\r\n  background-color:#2c3e50;\r\n  margin-top:10px\r\n}\r\n\r\n.widget-chat .msgBlock {\r\n  background-color:#2c3e50 !important; \r\n  color:#adadad;\r\n}\r\n.widget-chat .msgBlock .response {\r\n  color:#fafafa;\r\n}\r\n\r\n.widget-chat #messagesBlock .message-row .msg-date {\r\n    display: block !important;\r\n    float:right;\r\n}\r\n\r\n.widget-chat #messagesBlock .response .msg-date {\r\n    float:left !important;\r\n}\r\n\r\n.widget-chat #widget-layout {\r\n  padding:0px;\r\n}\r\n\r\n.widget-chat #widget-layout  > .columns {\r\n  padding:0px !important;\r\n}\r\n\r\n.widget-chat .large-12 > .row {\r\n  background-color:#293949;\r\n  padding:5px 5px;\r\n}\r\n\r\n.widget-chat .operator-info {\r\n  background-color:#293949;\r\n  border-width:0px;\r\n}','','','','','Hai una domanda? Chiedi pure!','','','2c3e50','90dd1af0e489e0d6f7ffd17bf92351b5.png','var/storagetheme/2014y/10/24/1/','http://www.skillup.it','',1)""")
            cursor.execute("""UPDATE `lh_chat_config` SET value = 1 WHERE identifier = 'default_theme_id'""")
            connection.commit()
        except Exception,e:
            print e 

        connection.close()

        url = "%s/%s/index.php/theme/default" % (LHC_DASHBOARD_URL, self.domain)
        print url
        data = {'ThemeID': 1 }
        requests.post(url, data=data)


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





