---
layout: single
title: Angebot
permalink: /de/oferta/
sidebar:
  nav: services
lang: de
---

## Unsere Dienstleistungen

Wir bieten umfassende Dienstleistungen im Bereich Landschaftsarchitektur und Dendrologie. Im Folgenden finden Sie eine detaillierte Beschreibung unseres Angebots.

<div class="services-grid">
{% assign de_services = site.pages | where_exp: "item", "item.url contains '/de/services/'" %}
{% for service in de_services %}
  <div class="service-item">
    <a href="{{ service.url | relative_url }}">
      <h3>{{ service.title }}</h3>
      {% if service.description %}
        <p class="excerpt">{{ service.description | truncate: 150 }}</p>
      {% endif %}
      {% if service.service_type %}
        <span class="service-type">{{ service.service_type }}</span>
      {% endif %}
      <span class="read-more">Weiterlesen →</span>
    </a>
  </div>
{% endfor %}
</div>

<style>
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.service-item {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  background: white;
}

.service-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
  border-color: #52adc8;
}

.service-item h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #333;
}

.service-item .excerpt {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.service-item .service-type {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f0f0f0;
  border-radius: 3px;
  font-size: 0.85rem;
  color: #666;
  margin-right: 0.5rem;
}

.service-item .read-more {
  display: inline-block;
  color: #52adc8;
  font-weight: 600;
  margin-top: 0.5rem;
}

.service-item a {
  text-decoration: none;
  color: inherit;
}

.service-item a:hover .read-more {
  text-decoration: underline;
}
</style>

---

<a name="dendrology"></a>
### Dendrologische Dienstleistungen

Wir spezialisieren uns auf die umfassende Betreuung von Bäumen:

{% assign dendro_services = de_services | where: "service_type", "dendrology" %}
<ul>
{% for service in dendro_services %}
  <li><a href="{{ service.url | relative_url }}">{{ service.title }}</a></li>
{% endfor %}
</ul>

<a name="design"></a>
### Planungsdienstleistungen

Wir erstellen Grünflächengestaltungen, die an Ihre Bedürfnisse angepasst sind:

{% assign design_services = de_services | where: "service_type", "design" %}
<ul>
{% for service in design_services %}
  <li><a href="{{ service.url | relative_url }}">{{ service.title }}</a></li>
{% endfor %}
</ul>

<a name="supervision"></a>
### Bauüberwachung und andere Dienstleistungen

{% assign other_services = de_services | where_exp: "item", "item.service_type != 'dendrology'" | where_exp: "item", "item.service_type != 'design'" %}
{% if other_services.size > 0 %}
<ul>
{% for service in other_services %}
  <li><a href="{{ service.url | relative_url }}">{{ service.title }}</a></li>
{% endfor %}
</ul>
{% endif %}