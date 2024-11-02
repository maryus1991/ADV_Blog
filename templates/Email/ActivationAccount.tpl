{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello Freand Please Activate your account
{% endblock %}

{% block body %}
<a href="https://{{ url }}" > </a>
<a href="http://{{ url }}" > </a>
{% endblock %}