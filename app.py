from PyInquirer import style_from_dict, prompt, Token
from PyInquirer import ValidationError, Validator
from termcolor import colored, cprint
from pyfiglet import figlet_format, Figlet
import re
import os
import click
import smtplib

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def pyfiglet(string, color, font=True):
    if font:
        f = Figlet(font='standard')
        print(colored(f.renderText(string), color=color))
    else:
        text = colored(string, color, attrs=['reverse', 'blink'])
        print(text)


class email_validator(Validator):
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

    def validate(self, email):
        if len(email.text):
            if re.match(self.pattern, email.text):
                return True
            else:
                raise ValidationError(
                    message='Invalid email',
                    cursor_position=len(email.text))
        else:
            raise ValidationError(
                message='Invalid email',
                cursor_position=len(email.text))


class empty_validator(Validator):
    def validate(self, document):
        if len(document.text):
            return True
        else:
            raise ValidationError(
                message="you can't leave this blank",
                cursor_position=len(document.text))


def send_mail(emails):
    from_email = emails.get('from_email')
    from_pass = emails.get('password_from_email')
    to_email = emails.get('to_email')
    subject = emails.get('subject')
    content = emails.get("text_html")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    message = 'Subject: {}\n\n{}'.format(subject, content)
    server.starttls()
    server.login(from_email, from_pass)
    server.sendmail(from_email, to_email, message)


class path_validator(Validator):
    def validate(self, value):
        if len(value.text):
            if os.path.isfile(value.text):
                return True
            else:
                raise ValidationError(
                    message="File not found",
                    cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


def email_details():
    details = [
        {
            'type': 'input',
            'name': 'from_email',
            'message': 'enter from email :',
            'validate': email_validator
        },
        {
            'type': 'input',
            'name': 'password_from_email',
            'message': 'enter password of from email :',
            'validate': empty_validator
        },
        {
            'type': 'input',
            'name': 'to_email',
            'message': 'enter To email :',
            'validate': email_validator
        },
        {
            'type': 'input',
            'name': 'subject',
            'message': 'enter subject :',
            'validate': empty_validator
        },
        {
            'type': 'list',
            'name': 'content_type',
            'message': 'content type :',
            'choices': ['HTML', 'Text'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'input',
            'name': 'text_html',
            'message': 'enter text :',
            'validate': empty_validator,
            'when': lambda answers: answers['content_type'] == 'text'
        },
        {
            'type': 'confirm',
            'name': 'html_content',
            'message': 'do you want to send html file :',
            'validate': empty_validator,
            'when': lambda answers: answers['content_type'] == 'html'
        },
        {
            'type': 'input',
            'name': 'text_html',
            'message': 'enter HTML :',
            'when': lambda answers: not answers.get("html_content", True),
            'validate': empty_validator
        },
        {
            'type': 'input',
            'name': 'text_html',
            'message': 'enter HTML path :',
            'validate': path_validator,
            'filter': lambda val: open(val).read(),
            'when': lambda answers: answers.get("html_content", False)
        },
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'do you want to send',

        },

    ]
    answer = prompt(details, style=style)
    return answer


@click.command()
def main():
    pyfiglet("Email  CLI", 'red')
    pyfiglet('Welcome to Email CLI', "blue", font=False)
    emails = email_details()
    if emails.get("confirm", True):
        try:
            send_mail(emails)
            pyfiglet("email send successfully", "green", font=False)
        except:
            pyfiglet("something went wrong,check information which you provided", "red", font=False)
    else:
        pyfiglet("Thank you", "green ", font=False)


if __name__ == '__main__':
    main()
