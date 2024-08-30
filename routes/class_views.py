from flask.views import MethodView
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import abort
from models import data_handler as dl


career_templates =  {
            None:"./main_pages/careers_pages/careers.html",
            **{t: f"main_pages/careers_pages/{t}.html" for t in ["internship", "remote", "hybrid", "onsite", "others","thank_you"]}
        }

resources_templates = {
            None:"./main_pages/resources_pages/resources.html",
            **{t: f"main_pages/resources_pages/{t}.html" for t in ["blog", "documentations", "new_updates", "events", "community","academy","partners"]}
        }

class Careers(MethodView):

    def get(self,link_type=None):
        templates =career_templates
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        template = templates.get(link_type)
        return render_template(template) if template else abort(404)
    
    def post(self,link_type):
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        form_data = request.form.to_dict()
        fullname = form_data.get('fullname')
        role = form_data.get('role')

        handlers = {
            "internship":self.handleIntership,
            "remote":self.handleRemote,
            "hybrid":self.handleHybrid,
            "onsite":self.handleOnsite,
            "others":self.handleOthers,
            }
        
        handler = handlers.get(link_type, lambda *args: abort(404))
        return handler(fullname , role)
    
    def handleIntership(self,fullname,role):
        applicants = dl.Applicants()
        applicants.add_applicant(fullname=fullname,role="internship")
        return redirect(url_for("career_type",link_type="thank_you"))
    
    def handleRemote(self,fullname,role):
        applicants = dl.Applicants()
        applicants.add_applicant(fullname=fullname,role="remote")
        return redirect(url_for("career_type",link_type="thank_you"))

    def handleHybrid(self,fullname,role):
        applicants = dl.Applicants()
        applicants.add_applicant(fullname=fullname,role="hybrid")
        return redirect(url_for("career_type",link_type="thank_you"))

    def handleOnsite(self,fullname,role):
        applicants = dl.Applicants()
        applicants.add_applicant(fullname=fullname,role="onsite")
        return redirect(url_for("career_type",link_type="thank_you"))

    def handleOthers(self,fullname,role):
        applicants = dl.Applicants()
        applicants.add_applicant(fullname=fullname,role="others")
        return redirect(url_for("career_type",link_type="thank_you"))
        
    
class Resources(MethodView):

    def get(self,link_type=None):
        
        templates = resources_templates
        link_type = link_type.strip().lower().rstrip("/")if link_type else None
        template = templates.get(link_type)
        return render_template(template)if template else abort(404)

if __name__ == "__main__":
    pass