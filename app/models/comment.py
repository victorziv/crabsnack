
class Comment(BaseModel):

    """
    """
    __tablename__ = 'comments'
    query = QueryComment(dba)

    # ____________________________

    def __init__(self, **attrs):
        self.__dict__.update(attrs)
    # ____________________________

    @staticmethod
