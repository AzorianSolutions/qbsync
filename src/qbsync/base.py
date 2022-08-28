class Base:

    def __repr__(self):
        values = []
        for key in self.__dict__.keys():
            values.append(key + ': ' + str(getattr(self, key)))
        return '<' + self.__class__.__name__ + ' {' + ', '.join(values) + '!r}>'
