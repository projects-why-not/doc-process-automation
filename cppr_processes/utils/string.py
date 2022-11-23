

class StringUtils:
    @classmethod
    def capitalize_words(cls, string, ignore_exceptions=True):
        exceptions = ['a', 'an', 'the', 'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around',
                      'at', 'before', 'behind', 'between', 'beyond', 'but', 'by', 'concerning', 'despite', 'down',
                      'during', 'except', 'following', 'for', 'from', 'in', 'including', 'into', 'like', 'near',
                      'of', 'off', 'on', 'onto', 'out', 'over', 'past', 'plus', 'since', 'throughout', 'to', 'towards',
                      'under', 'until', 'up', 'upon', 'with', 'within', 'without']
        return " ".join([w
                         if w in exceptions and ignore_exceptions
                         else w[0].upper() + w[1:]
                         for w in string.split()])

    @classmethod
    def slice(cls, string, st=0, end=-1, step=1):
        if end == -1:
            end = len(string)
        return string[st:end:step]
