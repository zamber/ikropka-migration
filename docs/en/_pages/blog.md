---
layout: single
title: News
permalink: /en/aktualnosci/
sidebar:
  nav: main
lang: en
---

## News and projects

Discover our latest designs, projects, and news from the world of landscape architecture.

<div class="blog-grid">
{% assign en_posts = site.pages | where_exp: "item", "item.path contains 'en/_posts'" %}
{% assign sorted_posts = en_posts | sort: 'date' | reverse %}
{% for post in sorted_posts %}
  <article class="blog-item">
    <a href="{{ post.url | relative_url }}">
      {% if post.header.image %}
        <img src="{{ site.baseurl }}{{ post.header.image }}" alt="{{ post.title | xml_escape }}" loading="lazy">
      {% endif %}
      <div class="blog-content">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%d.%m.%Y" }}</time>
        <h3>{{ post.title }}</h3>
        {% if post.description %}
          <p class="excerpt">{{ post.description | truncate: 150 }}</p>
        {% elsif post.excerpt %}
          <p class="excerpt">{{ post.excerpt | strip_html | truncate: 150 }}</p>
        {% endif %}
        <span class="read-more">Read more →</span>
      </div>
    </a>
  </article>
{% endfor %}
</div>

<style>
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.blog-item {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
}

.blog-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
  border-color: #52adc8;
}

.blog-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.blog-item .blog-content {
  padding: 1.5rem;
}

.blog-item time {
  display: block;
  color: #999;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.blog-item h3 {
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
  color: #333;
}

.blog-item .excerpt {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.blog-item .read-more {
  display: inline-block;
  color: #52adc8;
  font-weight: 600;
}

.blog-item a {
  text-decoration: none;
  color: inherit;
}

.blog-item a:hover .read-more {
  text-decoration: underline;
}
</style>