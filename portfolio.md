---
layout: default
title: Portfolio | TechVizions LLC
description: Selected federal and commercial cloud security and compliance engagements delivered by TechVizions LLC.
permalink: /portfolio/
---

<section class="bg-light" id="portfolio">
  <div class="container">
    <div class="row">
      <div class="col-lg-12 text-center">
        <h1 class="section-heading text-uppercase">{{ site.data.home.portfolio.heading }}</h1>
        <h3 class="section-subheading text-muted">Selected engagements across federal and regulated industries.</h3>
      </div>
    </div>
    <div class="row">
      {%- for project in site.projects -%}
      <div class="col-lg-12 mb-5">
        <h4>{{ project.client }}</h4>
        <p class="text-muted mb-2">{{ project.category }}</p>
        <p><strong>Date:</strong> {{ project.date }}</p>
        <div>{{ project.content }}</div>
      </div>
      {%- endfor -%}
    </div>
  </div>
</section>
