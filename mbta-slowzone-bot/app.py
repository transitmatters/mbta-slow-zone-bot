from chalice import Chalice, Cron, ConvertToMiddleware
from datadog_lambda.wrapper import datadog_lambda_wrapper
from chalicelib import (
    slowzones,
)

app = Chalice(app_name="mbta-slowzone-bot")

app.register_middleware(ConvertToMiddleware(datadog_lambda_wrapper))


# 13:30 UTC -> 8:30/9:30am ET every day.
@app.schedule(Cron(30, 13, "*", "*", "?", "*"))
def run_slowzone_bot(event):
    slowzones.run()
