import urllib3
import json


class TeamsWebhookException(Exception):
    """custom exception for failed webhook call"""
    pass


class ConnectorCard:
    def __init__(self, hookurl, http_timeout=60):
        self.http = urllib3.PoolManager()
        self.payload = {}
        self.hookurl = hookurl
        self.http_timeout = http_timeout

    def text(self, bread = '', fillings = '', cheese = ''):
        self.payload["text"] = (
            f"- ***Bread***: {bread} \r- ***Cheese***: {cheese} \r- ***Filling***:{fillings}")
        return self
        # - Item 1\r- Item 2\r- Item 3

    def title(self, mtitle='Test'):
        self.payload["title"] = mtitle
        return self

    def send(self):
        headers = {"Content-Type":"application/json"}
        r = self.http.request(
                'POST',
                f'{self.hookurl}',
                body=json.dumps(self.payload).encode('utf-8'),
                headers=headers, timeout=self.http_timeout)
        if r.status == 200: 
            return True
        else:
            raise TeamsWebhookException(r.reason)


if __name__ == "__main__":
    myTeamsMessage = ConnectorCard('')

    myTeamsMessage.text(bread = 'White', fillings = '', cheese = 'Cheddar')
    myTeamsMessage.title("Test ")#Name
    # myTeamsMessage.facts()#Name
    myTeamsMessage.send()


        #     "facts": [{
        #     "name": "Assigned to",
        #     "value": "Unassigned"
        # }, {
        #     "name": "Due date",
        #     "value": "Mon May 01 2017 17:07:18 GMT-0700 (Pacific Daylight Time)"
        # }, {
        #     "name": "Status",
        #     "value": "Not started"
        # }]