from wtforms import Form, Field, StringField, validators, TextField
from wtforms.widgets import TextInput
from flask.ext.babel import lazy_gettext as _

class TagsInputField(Field):
    widget = TextInput()
    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            if not isinstance(valuelist, list):
                self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

class ArticleForm(Form):
    title = StringField(
        _(u'Title'), 
        [
            validators.Length(min=6, max=256, message=_(u'%(attribute)s must be between %(min)d and %(max)d characters', min=6, max=256, attribute=_(u'Title')))
        ]
    )
    content = TextField(
        _(u'Content'), 
        [
            validators.Length(min=128, message=_(u'%(attribute)s is too short', attribute=_(u'Content')))
        ]
    )
    tags = TagsInputField(
        _(u'Tags'), 
        [
            validators.Length(min=1, max=5, message=_(u'Must have at least %(min)d tag and maximum %(max)d tags', attribute=_(u'Content'), min=1, max=5))
        ]
    )

class CommentForm(Form):
    content = TextField(
        _(u'Content'), 
        [
            validators.Length(min=10, message=_(u'%(attribute)s is too short', attribute=_(u'Content')))
        ] 
    )

class QuestionForm(Form):
    title = StringField(
        _(u'Title'), 
        [
            validators.Length(min=6, max=256, message=_(u'%(attribute)s must be between %(min)d and %(max)d characters', min=6, max=256, attribute=_(u'Title')))
        ]
    )
    content = TextField(
        _(u'Content'), 
        [
            validators.Length(min=64, message=_(u'%(attribute)s must be from %(min)d characters', attribute=_(u'Content'), min=64))
        ]
    )
    tags = TagsInputField(
        _(u'Tags'), 
        [
            validators.Length(min=1, max=5, message=_(u'Must have at least %(min)d tag and maximum %(max)d tags', attribute=_(u'Content'), min=1, max=5))
        ]
    )

class AnswerForm(Form):
    content = TextField(
        _(u'Content'), 
        [
            validators.Length(min=20, message=_(u'%(attribute)s is too short', attribute=_(u'Answer')))
        ] 
    )

class TopicForm(Form):
    title = StringField(
        _(u'Title'), 
        [
            validators.Length(min=6, max=256, message=_(u'%(attribute)s must be between %(min)d and %(max)d characters', min=6, max=256, attribute=_(u'Title')))
        ]
    )
    content = TextField(
        _(u'Content'), 
        [
            validators.Length(min=64, message=_(u'%(attribute)s must be from %(min)d characters', attribute=_(u'Content'), min=64))
        ]
    )
    tags = TagsInputField(
        _(u'Tags'), 
        [
            validators.Length(min=1, max=5, message=_(u'Must have at least %(min)d tag and maximum %(max)d tags', attribute=_(u'Content'), min=1, max=5))
        ]
    )