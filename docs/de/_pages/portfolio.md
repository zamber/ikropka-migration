---
layout: single
title: Portfolio
permalink: /de/portfolio/
sidebar:
  nav: portfolio
lang: de
---

## Unsere Projekte

Im Folgenden finden Sie **72 fertiggestellte Projekte** aus dem Bereich der Landschaftsarchitektur.

### Projekt suchen

<div class="portfolio-search">
  <input type="text" id="search-input" placeholder="Projekt nach Name, Standort oder Beschreibung suchen..." />
  <button id="clear-search" style="display: none;">Zurücksetzen</button>
</div>

### Nach Kategorie filtern

<div class="portfolio-filters">
  <a href="#all" class="filter-btn active" data-filter="all">Alle (72)</a>
  <a href="#projekty" class="filter-btn" data-filter="projekty">Projekte</a>
  <a href="#zabytkowe" class="filter-btn" data-filter="zabytkowe">Baudenkmäler</a>
  <a href="#szkolenia" class="filter-btn" data-filter="szkolenia">Schulungen</a>
</div>

<div class="portfolio-grid">
{% assign de_portfolio = site.pages | where_exp: "item", "item.url contains '/de/_portfolio/'" %}
{% assign sorted_portfolio = de_portfolio | sort: 'title' %}
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

  // Suchindex aus Portfolioposten erstellen
  const searchData = Array.from(portfolioItems).map(item => ({
    element: item,
    title: item.querySelector('h3')?.textContent || '',
    description: item.querySelector('.excerpt')?.textContent || '',
    category: item.dataset.category || ''
  }));

  // Fuse.js initialisieren
  const fuse = new Fuse(searchData, {
    keys: ['title', 'description', 'category'],
    threshold: 0.3,
    includeScore: true
  });

  let currentFilter = 'all';

  // Kategoriefilterung
  filterBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();

      // Aktiven Button aktualisieren
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      // Aktuellen Filter speichern
      currentFilter = this.dataset.filter;

      // Filter anwenden
      applyFilters();
    });
  });

  // Suchfunktion
  searchInput.addEventListener('input', function() {
    const query = this.value.trim();

    if (query.length > 0) {
      clearBtn.style.display = 'block';
    } else {
      clearBtn.style.display = 'none';
    }

    applyFilters();
  });

  // Suche zurücksetzen
  clearBtn.addEventListener('click', function() {
    searchInput.value = '';
    clearBtn.style.display = 'none';
    applyFilters();
  });

  function applyFilters() {
    const query = searchInput.value.trim();

    if (query.length === 0) {
      // Keine Suche - nur Kategoriefilter anwenden
      portfolioItems.forEach(item => {
        if (currentFilter === 'all' || item.dataset.category === currentFilter) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    } else {
      // Suche + Kategoriefilter
      const results = fuse.search(query);
      const matchedElements = new Set(results.map(r => r.item.element));

      portfolioItems.forEach(item => {
        const matchesSearch = matchedElements.has(item);
        const matchesCategory = currentFilter === 'all' || item.dataset.category === currentFilter;

        if (matchesSearch && matchesCategory) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    }
  }
});
</script>