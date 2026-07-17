---
layout: single
title: "Portfolio"
permalink: /portfolio/
sidebar:
  nav: "portfolio"
---

## Nasze realizacje

Poniżej znajdziesz **72 zrealizowane projekty** z zakresu architektury krajobrazu.

### Wyszukaj projekt

<div class="portfolio-search">
  <input type="text" id="search-input" placeholder="Szukaj projektu po nazwie, lokalizacji lub opisie..." />
  <button id="clear-search" style="display: none;">Wyczyść</button>
</div>

### Filtruj według kategorii

<div class="portfolio-filters">
  <a href="{{ '/portfolio/' | relative_url }}" class="filter-btn active">Wszystkie (72)</a>
  <a href="{{ '/portfolio/projekty/' | relative_url }}" class="filter-btn">Projekty (58)</a>
  <a href="{{ '/portfolio/zabytkowe/' | relative_url }}" class="filter-btn">Obiekty zabytkowe (11)</a>
  <a href="{{ '/portfolio/szkolenia/' | relative_url }}" class="filter-btn">Szkolenia (3)</a>
</div>

<p class="filter-note"><em>Możesz także filtrować projekty dynamicznie za pomocą wyszukiwarki powyżej.</em></p>

<div class="portfolio-grid">
{% assign sorted_portfolio = site.portfolio | sort: 'date' | reverse %}
{% for project in sorted_portfolio %}
  <div class="portfolio-item" data-category="{{ project.category }}">
    <a href="{{ project.url | relative_url }}">
      {% if project.featured_image %}
        <img src="{{ site.baseurl }}{{ project.featured_image }}" alt="{{ project.title | xml_escape }}" loading="lazy">
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
.portfolio-search {
  margin: 2rem 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  gap: 0.5rem;
}

.portfolio-search input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #52adc8;
  border-radius: 4px;
  font-size: 1rem;
}

.portfolio-search input:focus {
  outline: none;
  border-color: #3a8ba0;
}

.portfolio-search button {
  padding: 0.75rem 1.5rem;
  background: #52adc8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.portfolio-search button:hover {
  background: #3a8ba0;
}

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

<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioItems = document.querySelectorAll('.portfolio-item');
  const searchInput = document.getElementById('search-input');
  const clearBtn = document.getElementById('clear-search');

  // Build search index from portfolio items
  const searchData = Array.from(portfolioItems).map(item => ({
    element: item,
    title: item.querySelector('h3')?.textContent || '',
    description: item.querySelector('.excerpt')?.textContent || '',
    category: item.dataset.category || ''
  }));

  // Initialize Fuse.js
  const fuse = new Fuse(searchData, {
    keys: ['title', 'description', 'category'],
    threshold: 0.3,
    includeScore: true
  });

  let currentFilter = 'all';

  // Note: Category filtering now uses separate pages (SEO-friendly)
  // Filter buttons are now regular links to /portfolio/projekty/, /portfolio/zabytkowe/, etc.
  // This JavaScript now only handles search functionality

  // Search functionality
  searchInput.addEventListener('input', function() {
    const query = this.value.trim();

    if (query.length > 0) {
      clearBtn.style.display = 'block';
    } else {
      clearBtn.style.display = 'none';
    }

    applyFilters();
  });

  // Clear search
  clearBtn.addEventListener('click', function() {
    searchInput.value = '';
    clearBtn.style.display = 'none';
    applyFilters();
  });

  function applyFilters() {
    const query = searchInput.value.trim();

    if (query.length === 0) {
      // No search - show all items
      portfolioItems.forEach(item => {
        item.classList.remove('hidden');
      });
    } else {
      // Search only
      const results = fuse.search(query);
      const matchedElements = new Set(results.map(r => r.item.element));

      portfolioItems.forEach(item => {
        if (matchedElements.has(item)) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    }
  }
});
</script>
