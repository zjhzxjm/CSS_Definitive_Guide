from django import template
import datetime
import re

register = template.Library()


class CurrentTimeNode(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = str(format_string)
        self.var_name = var_name

    def render(self, context):
        now = datetime.datetime.now()
        context[self.var_name] = now.strftime(self.format_string)
        return ''


# class CommentNode(template.Node):
#     def render(self, context):
#         return ''
class UpperNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()


@register.tag
def do_current_time(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)

    m = re.search(r'(.*?) as (\w+)', arg)
    if m:
        fmt, var_name = m.groups()
    else:
        msg = '%r tag had invalid arguments' % tag_name
        raise template.TemplateSyntaxError(msg)

    if not(fmt[0] == fmt[-1] and fmt[0] in ('"', "'")):
        msg = "%r tag's argument should be in quotes" % tag_name
        raise template.TemplateSyntaxError(msg)

    return CurrentTimeNode(fmt[1:-1], var_name)


# def do_comment(parser, token):
#     nodelist = parser.parse(('endcomment',))
#     # 传递标签元组，返回django.template.NodeList实例
#     print(nodelist)
#     return CommentNode()
@register.tag(name="upper")
def do_upper(parser, token):
    nodelist = parser.parse(('endupper',))
    # 传递标签元组，返回django.template.NodeList实例,即{% upper %}和{% endupper %}间所有节点的列表
    print(nodelist)
    parser.delete_first_token()
    # 销毁该标签
    return UpperNode(nodelist)


@register.simple_tag
def current_time(format_string):
    try:
        return datetime.datetime.now().strftime(str(format_string))
    except UnicodeDecodeError:
        return ''
