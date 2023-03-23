from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, AnyOf

class Upload(FlaskForm):
    pcap = FileField('pcap', validators=[DataRequired()])

class ProtoFilter(FlaskForm):
    value = FileField('value')
    filter_type = FileField('filter_type', validators=[DataRequired(), AnyOf([u'all', u'proto', u'ipsrc', u'ipdst'])])
