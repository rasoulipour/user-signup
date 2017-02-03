

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
import cgi


def page_builder(user_error, pass_error, verify_error, email_error, u, p, v, e):
    username_label = '<label>Username</label>'
    password_label = '<label>Password</label>'
    verpass_label  = '<label>Verify Password</label>'
    email_label    = '<label>Email (Optional)</label>'

    username_input = '<input type = "text" name = "username" value='+u+'>'
    password_input = '<input type = "password" name = "password" value='+p+'>'
    verpass_input  = '<input type = "password" name = "verify" value='+v+'>'
    email_input    = '<input type = "text" name = "email" value='+e+'>'

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

def valid_email(ema):
    return Email_RE.match(ema)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        username, password, verify, email = "" , "" , "" , ""
        content = page_builder("","","","", username, password, verify, email)
        self.response.write(content)


    def post(self):
        username = self.request.get("username")
        username = cgi.escape(username)
        password = self.request.get("password")
        password = cgi.escape(password)
        verify   = self.request.get("verify")
        verify   = cgi.escape(verify)
        email    = self.request.get("email")
        email    = cgi.escape(email)

        if (valid_email(email) or email == "") and password == verify and valid_pass(password) and valid_username(username):
            content = "Welcome " + username
        else:

            error_user   = ""
            error_pass   = ""
            error_verify = ""
            error_email  = ""

            if not valid_username(username):
                error_user = "usename not valid."
                username = ""

            if not valid_pass(password):
                error_pass = "password not valid"
                password = ""

            if password != verify:
                error_verify = "passwords do not match"
                verify = ""

            if not valid_email(email):
                error_email = "email is not valid"
                email = ""

            content = page_builder(error_user,error_pass,error_verify,error_email,username, password, verify, email)


        self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
