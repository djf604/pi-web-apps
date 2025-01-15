from flask import Flask
from payroll import get_payroll

app = Flask(__name__)

@app.route("/")
def hello_world():
    allocations = get_payroll(
        start_date='2025-01-01',
        end_date='2025-01-15'
    )
    output_html = """
        <h1>Renewal Therapy Payroll</h1>
        <h2>Allocations for Jan 1 through Jan 15, 2025</h2>
        {}
    """.format(
        '\n'.join([f'<p>{a[0]}: ${a[1]:,.2f}</p>' for a in allocations])
    )
    
    return output_html