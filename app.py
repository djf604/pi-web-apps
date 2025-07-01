from datetime import datetime
from flask import Flask, render_template
from payroll import get_payroll, format_pay_periods, make_payroll_transfer

app = Flask(__name__)

@app.route("/")
def home():
    return """<h1>Renewal Therapy Internal Tools</h1>
    <ul><li><a href="/payroll">Payroll</a></li></ul>"""

@app.route("/payroll")
def display_allocations():

    context = {
        'pay_periods': format_pay_periods(n_pay_periods=4)
    }

    return render_template('payroll_show.html', **context)

    # return output_html

@app.route('/payroll/run/<start_date>/<end_date>/<mode>')
def run_payroll(start_date, end_date, mode):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    ret = make_payroll_transfer(start_date, end_date, dry_run=False)
    print(ret)
    return '<br/>'.join(ret)