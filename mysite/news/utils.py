class MyMixin(object):

    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.capitalize()

    def get_upper(self, s):
        if isinstance(s, str):
            return s.capitalize()
        else:
            return s.title.capitalize()

