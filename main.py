#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re




def page_builder(user_error, pass_error, verify_error, email_error):
    username_label = '<label>Username</label>'
    password_label = '<label>Password</label>'
    verpass_label  = '<label>Verify Password</label>'
    email_label    = '<label>Email (Optional)</label>'

    username_input = '<input type = "text" name = "username">'
    password_input = '<input type = "password" name = "password">'
    verpass_input = '<input type = "password" name = "verify">'
    email_input = '<input type = "text" name = "email">'

    submit = '<input type="submit" />'

    header = '<h1>Sign-up Information:</h1>'

    form = ('<form method="post">' + username_label + username_input + user_error + '<br>'
    + password_label + password_input + pass_error + '<br>'
    + verpass_label + verpass_input + verify_error + '<br>'
    + email_label + email_input + email_error + '<br>'
    + submit + '</form>')

    return header + form



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
Password_RE = re.compile(r"^.{3,20}$")
Email_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_pass(passw):
    return Password_RE.match(passw)

def valid_email(email):
    return Email_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = page_builder("","","","")
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if not valid_username(username):
            content = page_builder('Invalid Username.',"","", "")

        elif not valid_pass(password):
            content = page_builder("",'Invalid password.',"", "")

        elif password != verify:
            content = page_builder("","","Passwords do not match.", "")

        elif email != "" and not valid_email(email):
            content = page_builder("","","","Invalid email.")

        else:
            content = "Wecome " + username

        self.response.write(content)






app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
