---
description: Ikropka – pracownia projektowania zieleni i krajobrazu. Tworzymy ogrody,
  parki i przestrzenie publiczne z dbałością o naturę i estetykę.
header:
  caption: Twój partner w zielonych inwestycjach
  overlay_filter: '0.5'
  overlay_image: /assets/images/layout_slider_do-500KB_www1.jpg
layout: splash
permalink: /
title: IKROPKA — Pracownia Architektury Krajobrazu

feature_row:
  - image_path: /assets/images/services-dendrology.jpg
    alt: "Usługi dendrologiczne"
    title: "Usługi Dendrologiczne"
    excerpt: "Inwentaryzacje, operaty, ekspertyzy, przeglądy drzew i pogotowie dendrologiczne."
    url: "/oferta/#dendrology"
    btn_label: "Dowiedz się więcej"
    btn_class: "btn--primary"
  - image_path: /assets/images/services-design.jpg
    alt: "Usługi projektowe"
    title: "Usługi Projektowe"
    excerpt: "Projekty zagospodarowania terenu, projekty zieleni, ogrody prywatne, parki."
    url: "/oferta/#design"
    btn_label: "Dowiedz się więcej"
    btn_class: "btn--primary"
  - image_path: /assets/images/services-supervision.jpg
    alt: "Nadzory"
    title: "Nadzory i Obsługa Inwestycji"
    excerpt: "Inspektor nadzoru dendrologicznego i nadzór terenów zieleni w procesie inwestycyjnym."
    url: "/oferta/#supervision"
    btn_label: "Dowiedz się więcej"
    btn_class: "btn--primary"
---

Powstała w 2007 roku Pracownia Architektury Krajobrazu IKROPKA na przestrzeni lat zyskała renomę profesjonalnego, rzetelnego i terminowego wykonawcy. Swoją ofertę kieruje zarówno do osób prywatnych, jak i architektów, inwestorów, samorządów. Klient może liczyć na profesjonalną obsługę i fachowe doradztwo. Każdy projekt wykonany zostanie z szacunkiem do środowiska naturalnego.

{% include feature_row %}

## Trzy filary działalności

### Projektowanie

IKROPKA tworzy projekty dopasowane do potrzeb Klientów. Może pochwalić się również bogatym doświadczeniem w pracy w przestrzeniach objętych ochroną konserwatorską.

### Dendrologia

Zespół zajmujący się opracowaniami dendrologicznymi opracowuje inwentaryzacje zieleni, operaty dendrologiczne, a w przypadkach większej szczegółowości opinie i ekspertyzy dendrologiczne poprzedzone badaniami drzew.

### Nadzór

IKROPKA od lat świadczy usługi nadzoru dendrologicznego – Inspektor Nadzoru Terenów Zieleni oraz Inspektor Nadzoru Dendrologicznego w Procesie Inwestycyjnym.

## Holistyczne podejście

Pracownia Architektury Krajobrazu IKROPKA pomaga swoim Klientom w czynnościach formalnoprawnych związanych z uzyskaniem niezbędnych pozwoleń w tym na wycinkę drzew. W oparciu o obowiązujące podstawy prawne, w przypadku Wrocławia Zarządzenie Nr 1217/19 Prezydenta Wrocławia z dnia 28 czerwca 2019 r. w sprawie ochrony drzew i rozwoju terenów zieleni Wrocławia opracowujemy dane dotyczące drzew celem wprowadzenia do Systemu Informacji Przestrzennej Wrocławia (SIP). Dużą wagę przykładamy do ochrony drzew w procesie inwestycyjnym przygotowując opracowania takie jak projekt ochrony drzew na placu budowy. Wspieramy zarządców nieruchomości oraz jednostki samorządowe, gminy ( w tym placówki oświatowe) wykonując przeglądy drzewostanu pod kątem bezpieczeństwa dla ludzi i mienia. Prowadzimy także szkolenia poświęcone zagadnieniom dendrologicznym na każdym etapie realizowania inwestycji. Zapraszamy do współpracy!


## Nasze atuty

- **PODEJMUJEMY KAŻDE WYZWANIE** - Żaden projekt nie jest dla nas zbyt trudny. Specjalizujemy się w złożonych inwestycjach, obiektach zabytkowych i wymagających terenach.
- **PROJEKTY FUNKCJONALNE I OPARTE NA PRZYRODZIE (NBS)** - Tworzymy rozwiązania oparte na naturze (Nature-Based Solutions), które łączą funkcjonalność z dbałością o środowisko.
- **TERMINOWOŚĆ PRZEDE WSZYSTKIM** - Dotrzymujemy terminów. Twoja inwestycja nie będzie opóźniona z naszej winy.
- **WIELOLETNIE DOŚWIADCZENIE OD 2003 ROKU** - Ponad 20 lat praktyki w architekturze krajobrazu i dendrologii. Setki zrealizowanych projektów.
- **ZESPÓŁ PROFESJONALISTÓW** - Dendrolodzy, architekci krajobrazu, inspektorzy nadzoru - wykwalifikowani specjaliści z uprawnieniami.
- **DBAMY O TWOJĄ INWESTYCJĘ** - Pełna obsługa od projektu, przez nadzór, aż po odbiór. Jesteśmy z Tobą na każdym etapie. 

## Wybrane projekty

Zapoznaj się z naszymi najnowszymi realizacjami:

<div class="featured-portfolio">
{% assign featured = site.portfolio | sort: 'date' | reverse | limit: 6 %}
{% for project in featured %}
  <div class="featured-item">
    <a href="{{ project.url | relative_url }}">
      {% if project.featured_image %}
        <img src="{{ site.baseurl }}{{ project.featured_image }}" alt="{{ project.title | xml_escape }}" loading="lazy">
      {% endif %}
      <h4>{{ project.title }}</h4>
    </a>
  </div>
{% endfor %}
</div>

<div style="text-align: center; margin: 2rem 0;">
  <a href="/ikropka-migration/portfolio/" class="button">Zobacz wszystkie projekty (72) →</a>
</div>

<style>
.featured-portfolio {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.featured-item {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.featured-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.featured-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.featured-item h4 {
  padding: 1rem;
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.featured-item a {
  text-decoration: none;
  color: inherit;
}
</style>

## Co mówią o nas klienci?

> "Polecamy Pracownię Architektury Krajobrazu IKROPKA jako solidnego partnera do współpracy w ramach zadań związanych z dendrologią i obiektami zabytkowymi."
>
> — **Wejherowski Zarząd Nieruchomości Komunalnych**, 2019

> "Pani Dominika Krop-Andrzejczuk wraz z Jej zespołem jest fachowym i doświadczonym wykonawcą projektów zieleni miejskiej i dachów zielonych."
>
> — **JSK Architekci**, 2019

> "PAK IKROPKA jest fachowym i doświadczonym projektantem zagospodarowania terenów zieleni. Polecamy współpracę."
>
> — **ARCHICOM**, 2018

> "Zespół kierowany przez Dominikę Krop wykazuje się znajomością szerokiej wiedzy z dendrologii, fauny, flory i ich znaczenia dla środowiska."
>
> — **Urząd Miasta i Gminy w Strzelinie**, 2017



[Zobacz wszystkie referencje (60+)](/ikropka-migration/referencje/){: .btn .btn--info}
{: .text-center}
