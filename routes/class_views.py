from flask.views import MethodView
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import abort
from models import data_handler as dl
from app import session
from models.data_handler import bcrypt


career_templates =  {
            None:"./main_pages/careers_pages/careers.html",
            **{t: f"main_pages/careers_pages/{t}.html" for t in ["internship", "remote", "hybrid", "onsite", "others","thank_you"]}
        }

resources_templates = {
            None:"./main_pages/resources_pages/resources.html",
            **{t: f"main_pages/resources_pages/{t}.html" for t in ["blog", "documentations", "new_updates", "events", "community","academy","partners"]}
        }

admin_templates = {
            None:"./admin/index.html",
            **{t: f"./admin/{t}.html" for t in ["login","signupadmin","logout"]}
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


class Admin(MethodView):

    def get(self, link_type=None):
        # Debugging output
        print(f"Session username: {session.get('username')}")
        print(f"Received link_type: '{link_type}'")



        # Redirect to login if user is not signed in and link_type is "index"
        if session.get("username") is None and link_type == None:
            print("Redirecting to login")
            return redirect(url_for("admin_links", link_type="login"))

        # Process link_type and render the appropriate template
        templates = admin_templates
        link_type = link_type.strip().lower().rstrip("/") if link_type else None
        template = templates.get(link_type)
        return render_template(template) if template else abort(404)

    def post(self, link_type=None):
        # Debugging output
        print(f"Received link_type: {link_type}")
        self.form_data = request.form.to_dict()
        print(self.form_data)

        handlers = {
            "signupadmin":self.signupadmin,
            "login":self.login,
            "logout":self.logout,
            }
        handler = handlers.get(link_type)
        return handler()

    def signupadmin(self):
        dl.User().create_user(**self.form_data)
        return redirect(url_for("admin_links", link_type="login"))

    def login(self):
        users = dl.User().get_all_users()
        usernames = []

        for user in users:
            usernames.append(user.username)

        print(usernames)
        print(user)

        if self.form_data['username'] in usernames:
            user = dl.User().get_specfic_user(self.form_data['username'])
            password = self.form_data["password"].encode('utf-8')
            verify = bcrypt.checkpw(password, user.password)
            if verify == True:
                # Set the session for the logged-in user
                session['username'] = user.username
                print(f"Logged in as: {user.username}")
                return redirect(url_for("admin_links",link_type="/"))
            else:
                print("Password incorrect.")
                return redirect(url_for("admin_links", link_type="login"))
        else:
            print("Username not found")
            return redirect(url_for("admin_links",link_type= "login"))

    def logout(self):
        session.pop()
        return render_template("admin/logout.html")



if __name__ == "__main__":
    pass
