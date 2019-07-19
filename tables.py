from flask_table import Table, Col

class Results(Table):
    events = Col('Events')
    severity = Col('Severity')
    urgency = Col('urgency')
    warning_source = Col('Warning Source')
    headlines = Col('headlines')