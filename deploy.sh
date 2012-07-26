#!/bin/bash
cp -u -v -r . /usr/local/django/youtubeinsight | grep -v \.git
rm -r /usr/local/django/youtubeinsight/.git
rm /usr/local/django/youtubeinsight/.gitignore
touch /usr/local/django/youtubeinsight/apache/django.wsgi
