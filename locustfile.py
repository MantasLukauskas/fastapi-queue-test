from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 5)  # Simulated users will wait 1-5 seconds between tasks

    @task
    def get_status(self):
        self.client.get("/status/")
