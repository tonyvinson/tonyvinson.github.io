---
layout: default
title: Services | TechVizions LLC
description: Cloud security architecture, compliance and authorization, and DevSecOps automation for federal and commercial organizations.
permalink: /services/
---

<section id="services">
  <div class="container">
    <div class="row">
      <div class="col-lg-12 text-center">
        <h1 class="section-heading text-uppercase">{{ site.data.home.services.heading }}</h1>
        <h3 class="section-subheading text-muted">{{ site.data.home.services.subheading }}</h3>
      </div>
    </div>
    <div class="row text-center">
      {%- for service in site.data.home.services.service -%}
      <div class="col-md-4">
        <span class="fa-stack fa-4x">
          <i class="fas fa-circle fa-stack-2x text-primary"></i>
          <i class="{{ service.icon }} fa-stack-1x fa-inverse"></i>
        </span>
        <h4 class="service-heading">{{ service.heading }}</h4>
        <p class="text-muted">{{ service.text }}</p>
      </div>
      {%- endfor -%}
    </div>
  </div>
</section>
