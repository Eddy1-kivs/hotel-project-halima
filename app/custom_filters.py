from django import template

register = template.Library()

@register.filter
def limit_words(value, arg):
    """
    Truncates a string after a certain number of words.
    Argument: number of words to preserve.
    """
    words = value.split()
    return ' '.join(words[:arg])
