from flask import render_template
from app import class_views as cl
from app import db
from app import models   

def register_routes(app):
    @app.route("/")#The landing page
    def index():
        return render_template("index.html")

    @app.route("/aboutUs/")#The about us page
    def aboutUs():
        return render_template("aboutUs.html")

    @app.route("/meetTheTeam/")#The meet the team page
    def meetTheTeam():
        return render_template("meetTheTeam.html")

    @app.route("/products/")#The products page 
    def products():
        return render_template("products.html")
    
    @app.route("/contactUs/")#The contact us
    def  contactUs():
        return render_template("contactUs.html")

    app.add_url_rule("/careers/",view_func=cl.Careers.as_view('career_base'))
    app.add_url_rule("/careers/<string:link_type>",view_func=cl.Careers.as_view('career_type'))#The dynamic link system for careers section
    app.add_url_rule("/resources/",view_func=cl.Resources.as_view('resources_base'))
    app.add_url_rule("/resources/<string:link_type>",view_func=cl.Resources.as_view('resources_links'))#The dynmic link system for the resources section
