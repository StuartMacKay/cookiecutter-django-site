import os

broker_url = os.environ["BROKER_URL"]

task_always_eager = broker_url == ""

accept_content = ["json"]

worker_hijack_root_logger = False
