{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello Freand Please enter this lin to rest your password account
{% endblock %}

{% block body %}
{{ first_url }}
{{ second_url }}
{% endblock %}