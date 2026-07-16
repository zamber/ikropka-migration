---
layout: single
title: "Oferta"
permalink: /oferta/
sidebar:
  nav: "services"
---

## Nasze usługi

Oferujemy kompleksowe usługi z zakresu architektury krajobrazu i dendrologii. Poniżej znajdziesz szczegółowy opis naszej oferty.

<div class="services-grid">
{% for service in site.services %}
  <div class="service-item">
    <a href="{{ service.url | relative_url }}">
      <h3>{{ service.title }}</h3>
      {% if service.description %}
        <p class="excerpt">{{ service.description | truncate: 150 }}</p>
      {% endif %}
      {% if service.service_type %}
        <span class="service-type">{{ service.service_type }}</span>
      {% endif %}
      <span class="read-more">Czytaj więcej →</span>
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
### Usługi Dendrologiczne

Specjalizujemy się w kompleksowej opiece nad drzewami:

{% assign dendro_services = site.services | where: "service_type", "dendrology" %}
<ul>
{% for service in dendro_services %}
  <li><a href="{{ service.url | relative_url }}">{{ service.title }}</a></li>
{% endfor %}
</ul>

<a name="design"></a>
### Usługi Projektowe

Tworzymy projekty zieleni dopasowane do Twoich potrzeb:

{% assign design_services = site.services | where: "service_type", "design" %}
<ul>
{% for service in design_services %}
  <li><a href="{{ service.url | relative_url }}">{{ service.title }}</a></li>
{% endfor %}
</ul>

<a name="other"></a>
### Inne Usługi

{% assign other_services = site.services | where_exp: "service", "service.service_type != 'dendrology' and service.service_type != 'design'" %}
{% if other_services.size > 0 %}
<ul>
{% for service in other_services %}
  <li><a href="{{ service.url | relative_url }}">{{ service.title }}</a></li>
{% endfor %}
</ul>
{% endif %}
