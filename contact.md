---
layout: default
title: Contact | TechVizions LLC
description: Contact TechVizions LLC for cloud security architecture, compliance, and DevSecOps consulting.
permalink: /contact/
---

<section id="contact">
  <div class="container">
    <div class="row">
      <div class="col-lg-12 text-center">
        <h1 class="section-heading text-uppercase">{{ site.data.home.contact.heading }}</h1>
        <h3 class="section-subheading text-muted">Tell us about your security and compliance priorities.</h3>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12">
        <form id="contactForm" action="https://formspree.io/f/xnnpnzbv" method="POST">
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <input class="form-control" id="name" type="text" name="name" placeholder="{{ site.data.home.contact.name }}" required>
              </div>
              <div class="form-group">
                <input class="form-control" id="email" type="email" name="email" placeholder="{{ site.data.home.contact.email }}" required>
              </div>
              <div class="form-group">
                <input class="form-control" id="phone" type="tel" name="phone" placeholder="{{ site.data.home.contact.phone }}" required>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <textarea class="form-control" id="message" name="message" placeholder="{{ site.data.home.contact.message }}" required></textarea>
              </div>
            </div>
            <div class="col-lg-12 text-center">
              <button id="sendMessageButton" class="btn btn-primary btn-xl text-uppercase" type="submit">
                {{ site.data.home.contact.btn }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>
