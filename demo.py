import codecs
import sys
import boto3
import csv

from github import Github
from PostHITask import PostHit

# First create a Github instance:

# using username and password
g = Github("txh357@gmail.com", "s101062139")

#print(g.get_user().name)
# g = Github(base_url="https://github.com/tingyaohsu", login_or_token="23f9a8cc382f4af9c29285ee9fad6f0008de9774")

repo = g.get_repo("tingyaohsu/CrowdSourcing-Project")

# contents = repo.get_contents("Final_Project/README.md")
# print(contents)

# contents = repo.get_contents("test.txt")
# repo.update_file(contents.path, "more tests", "more tests", contents.sha)


filename = codecs.open("Final_Project/index.html", 'r')
html_file = filename.read()
# print (html_file)

# create new html file for worker
create_place = 'Final_Project/index_test.html'
# repo.create_file(create_place, "create html for worker", html_file)

setting_template_xml = codecs.open("Final_Project/setting_template.xml", 'r')
xml_file = setting_template_xml.read()
# print ("ori:",set_xml_link)

url = 'https://tingyaohsu.github.io/CrowdSourcing-Project/{}'.format(create_place)
print (url)

update_xml = xml_file.format(url)

# print("new:",update_xml)
setting_xml = codecs.open("Final_Project/setting.xml", 'w')
setting_xml.write(update_xml)

#update xml
contents = repo.get_contents("Final_Project/setting.xml")
repo.update_file("Final_Project/setting.xml", "update xml for workers", update_xml, contents.sha)

#post my task
# PostHit();




