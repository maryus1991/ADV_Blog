{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello Freand Please enter this lin to rest your password account
{% endblock %}

{% block body %}
<a href="https://{{ url }}" > </a>
<a href="http://{{ url }}" > </a>
{% endblock %}