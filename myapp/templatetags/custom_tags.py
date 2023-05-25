from django import template
register = template.Library()

@register.filter
def extract_word(value):
    words = value.split(", ")
    if len(words) > 1:
        return words[1]
    return ""
@register.filter
def extract_words(value):
    words = value.split(",")
    if len(words) > 1:
        return words[0]
    return ""
