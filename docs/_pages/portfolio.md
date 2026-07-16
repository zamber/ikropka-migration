---
layout: single
title: "Portfolio"
permalink: /portfolio/
sidebar:
  nav: "portfolio"
---

## Nasze realizacje

Poniżej znajdziesz **72 zrealizowane projekty** z zakresu architektury krajobrazu.

### Filtruj według kategorii

<div class="portfolio-filters">
  <a href="#all" class="filter-btn active" data-filter="all">Wszystkie (72)</a>
  <a href="#projekty" class="filter-btn" data-filter="projekty">Projekty</a>
  <a href="#zabytkowe" class="filter-btn" data-filter="zabytkowe">Obiekty zabytkowe</a>
  <a href="#szkolenia" class="filter-btn" data-filter="szkolenia">Szkolenia</a>
</div>

<div class="portfolio-grid">
{% assign sorted_portfolio = site.portfolio | sort: 'date' | reverse %}
{% for project in sorted_portfolio %}
  <div class="portfolio-item" data-category="{{ project.category }}">
    <a href="{{ project.url | relative_url }}">
      {% if project.featured_image %}
        <img src="{{ project.featured_image | relative_url }}" alt="{{ project.title }}" loading="lazy">
      {% endif %}
      <h3>{{ project.title }}</h3>
      {% if project.description %}
        <p class="excerpt">{{ project.description | truncate: 120 }}</p>
      {% endif %}
      {% if project.category %}
        <span class="category-badge">{{ project.category }}</span>
      {% endif %}
    </a>
  </div>
{% endfor %}
</div>

<style>
.portfolio-filters {
  margin: 2rem 0;
  text-align: center;
}

.filter-btn {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  margin: 0.25rem;
  border: 2px solid #52adc8;
  border-radius: 4px;
  color: #52adc8;
  text-decoration: none;
  transition: all 0.3s ease;
}

.filter-btn:hover,
.filter-btn.active {
  background: #52adc8;
  color: white;
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
  margin: 0 1rem 1rem;
  color: #666;
  font-size: 0.9rem;
}

.portfolio-item .category-badge {
  display: inline-block;
  margin: 0 1rem 1rem;
  padding: 0.25rem 0.75rem;
  background: #f0f0f0;
  border-radius: 3px;
  font-size: 0.85rem;
  color: #666;
}

.portfolio-item.hidden {
  display: none;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioItems = document.querySelectorAll('.portfolio-item');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();

      // Update active button
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      // Filter items
      const filter = this.dataset.filter;

      portfolioItems.forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    });
  });
});
</script>
