---
layout: single
title: "Projekty Obiektów Zabytkowych"
permalink: /portfolio/zabytkowe/
description: "Projekty renowacji i konserwacji zabytkowych parków, dworów i cmentarzy. Portfolio 11 projektów dla obiektów zabytkowych IKROPKA."
sidebar:
  nav: "portfolio"
---

<nav class="breadcrumb">
  <a href="{{ '/portfolio/' | relative_url }}">Portfolio</a> / <strong>Obiekty zabytkowe</strong>
</nav>

## Projekty Obiektów Zabytkowych

Prezentujemy **11 projektów** renowacji i konserwacji zabytkowych parków, dworów, cmentarzy i ogrodów historycznych.

<div class="portfolio-grid">
{% assign category_projects = site.portfolio | where: "category", "zabytkowe" | sort: 'date' | reverse %}
{% for project in category_projects %}
  <div class="portfolio-item">
    <a href="{{ project.url | relative_url }}">
      {% if project.featured_image %}
        <img src="{{ site.baseurl }}{{ project.featured_image }}" alt="{{ project.title | xml_escape }}" loading="lazy">
      {% endif %}
      <h3>{{ project.title }}</h3>
      {% if project.description %}
        <p class="excerpt">{{ project.description | truncate: 120 }}</p>
      {% endif %}
      {% if project.project.location %}
        <p class="location"><i class="fas fa-map-marker-alt"></i> {{ project.project.location }}</p>
      {% endif %}
    </a>
  </div>
{% endfor %}
</div>

<div class="category-nav">
  <p><strong>Zobacz inne kategorie:</strong></p>
  <a href="{{ '/portfolio/projekty/' | relative_url }}" class="category-link">Projekty (58)</a>
  <a href="{{ '/portfolio/szkolenia/' | relative_url }}" class="category-link">Szkolenia (3)</a>
  <a href="{{ '/portfolio/' | relative_url }}" class="category-link">Wszystkie projekty (72)</a>
</div>

<style>
.breadcrumb {
  margin-bottom: 2rem;
  font-size: 0.9rem;
  color: #666;
}

.breadcrumb a {
  color: #52adc8;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.portfolio-item {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.portfolio-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.portfolio-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.portfolio-item h3 {
  font-size: 1.1rem;
  margin: 1rem;
  color: #333;
}

.portfolio-item .excerpt {
  margin: 0 1rem 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.portfolio-item .location {
  margin: 0 1rem 1rem;
  color: #999;
  font-size: 0.85rem;
}

.portfolio-item .location i {
  color: #52adc8;
}

.category-nav {
  margin: 3rem 0 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.category-nav p {
  margin-bottom: 1rem;
  color: #666;
}

.category-link {
  display: inline-block;
  margin: 0.5rem;
  padding: 0.5rem 1.5rem;
  border: 2px solid #52adc8;
  border-radius: 4px;
  color: #52adc8;
  text-decoration: none;
  transition: all 0.3s ease;
}

.category-link:hover {
  background: #52adc8;
  color: white;
}
</style>
