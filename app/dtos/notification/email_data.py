class EmailData(object):
    def __init__(self,
        subject,
        html_template_path,
        txt_template_path,
        context_data):
        self.subject = subject
        self.html_template_path = html_template_path
        self.txt_template_path = txt_template_path
        self.context_data = context_data
