class URLInfo:
    def __init__(self, domain, subject, article_id):
        self.domain = domain
        self.subject = subject
        self.article_id = article_id

    def __str__(self):
        result = ""
        result += f"domain: {self.domain}\n"
        result += f"subject: {self.subject}\n"
        result += f"article_id: {str(self.article_id)}\n"

        return result
