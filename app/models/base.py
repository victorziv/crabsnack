from flask import abort
# =========================================


class Permission:
    FOLLOW = 0x01               # 0b00000001
    COMMENT = 0x02              # 0b00000010
    WRITE_ARTICLES = 0x04       # 0b00000100
    MODERATE_COMMENTS = 0x08    # 0b00001000
    ADMINISTER = 0x80           # 0b10000000
# =========================================


class BaseModel:

    @classmethod
    def fetch_all(cls):
        model_list = cls.query.read()
        return [cls(attrs=m) for m in model_list]
    # __________________________________

    @classmethod
    def get_by_field(cls, name, value):
        kwargs = {name: value}
        modeld = cls.query.read_one_by_field(**kwargs)
        if modeld is None:
            return

        model_instance = cls(attrs=dict(modeld))
        return model_instance
    # __________________________________

    @classmethod
    def get_by_field_or_404(cls, name, value):
        kwargs = {name: value}
        modeld = cls.query.read_one_by_field(**kwargs)
        if modeld is None:
            abort(404)

        model_instance = cls(attrs=dict(modeld))
        return model_instance
    # __________________________________

    @classmethod
    def clear_table(cls):
        cls.query.remove_all_records()
# ===========================
