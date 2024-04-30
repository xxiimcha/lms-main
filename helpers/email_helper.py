from django.core.mail import send_mail, EmailMessage



class EmailHelper(object):

    def __init__(self, subject:str, body:str, recipients:list) -> None:
        self.subject = subject
        self.body = body
        self.recipients = recipients
        pass

    def send_email(self,use_html=False):

        email = EmailMessage(
            subject = self.subject, 
            body = self.body,
            # from_email = EMAIL_HOST_USER,
            to=[self.recipients])
        
        if use_html:
            email.content_subtype = "html"


        status =  email.send()

        return status