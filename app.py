from flask import Flask
from payroll import get_payroll

app = Flask(__name__)

@app.route("/")
def home():
    return """<h1>Renewal Therapy Internal Tools</h1>
    <ul><li><a href="/payroll">Payroll</a></li></ul>"""

@app.route("/payroll")
def hello_world():
    allocations = get_payroll(
        start_date='2025-01-01',
        end_date='2025-01-15'
    )
    allocations2 = get_payroll(
        start_date='2025-01-16',
        end_date='2025-01-31'
    )
    output_html = """
        <h1>Renewal Therapy Payroll</h1>
        <h2>Allocations for Jan 1 through Jan 15, 2025</h2>
        {}
        <h2>Allocations for Jan 16 through Jan 31, 2025</h2>
        {}
    """.format(
        '\n'.join([f'<p>{a[0]}: ${a[1]:,.2f}</p>' for a in allocations]),
        '\n'.join([f'<p>{a[0]}: ${a[1]:,.2f}</p>' for a in allocations2]),
    )

    return output_html