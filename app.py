from flask import Flask, render_template
from payroll import get_payroll, format_pay_periods

app = Flask(__name__)

@app.route("/")
def home():
    return """<h1>Renewal Therapy Internal Tools</h1>
    <ul><li><a href="/payroll">Payroll</a></li></ul>"""

@app.route("/payroll")
def display_allocations():
    # allocations = get_payroll(
    #     start_date='2025-01-01',
    #     end_date='2025-01-15'
    # )
    # allocations2 = get_payroll(
    #     start_date='2025-01-16',
    #     end_date='2025-01-31'
    # )
    # allocations3 = get_payroll(
    #     start_date='2025-02-01',
    #     end_date='2025-02-15'
    # )
    # <a href="/payroll/run/2025-01-01/2025-01-15/confirm">Run Payroll</a>
    # output_html = """
    #     <h1>Renewal Therapy Payroll</h1>
    #     <h2>Allocations for Jan 1 through Jan 15, 2025</h2>
    #     {}
    #     <h2>Allocations for Jan 16 through Jan 31, 2025</h2>
    #     {}
    #     <h2>Allocations for Feb 1 through Feb 15, 2025</h2>
    #     {}
    # """.format(
    #     '\n'.join([f'<p>{a[0]}: ${a[1]:,.2f}</p>' for a in allocations]),
    #     '\n'.join([f'<p>{a[0]}: ${a[1]:,.2f}</p>' for a in allocations2]),
    #     '\n'.join([f'<p>{a[0]}: ${a[1]:,.2f}</p>' for a in allocations3]),
    # )

    # context = {
    #     # 'pay_periods': [allocations, allocations2],
    #     'pay_periods': [{
    #         'start_date': 'Jan 1',
    #         'end_date': 'Jan 15, 2025',
    #         'allocations': allocations
    #     }, {
    #         'start_date': 'Jan 16',
    #         'end_date': 'Jan 31, 2025',
    #         'allocations': allocations2
    #     }],
    # }

    context = {
        'pay_periods': format_pay_periods(n_pay_periods=4)
    }

    return render_template('payroll_show.html', **context)

    # return output_html

@app.route('/payroll/run/<start_date>/<end_date>/<mode>')
def run_payroll(start_date, end_date, mode):
    return """
    <p>start_date: {}</p><p>end_date: {}</p><p>confirm: {}</p>
    """.format(start_date, end_date, 'Ran it' if mode == 'run' else 'Ask please')