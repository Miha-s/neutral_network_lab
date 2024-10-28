class ImageLink:
    def __init__(self, link, type):
        self.link = link
        self.type = type

    def __repr__(self):
        return f"ImageLink('{self.link}', '{self.type}')"