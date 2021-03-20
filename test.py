import requests as r
import json
data = {
    "adminUser": "admin",
    "adminPass": "DrklOyEHNzxxQMZU",
    "domainName": "test.gitdev.in"
}
x = r.post('https://panel.gitdev.in:8090/api/deleteWebsite',
           data=json.dumps(data))

print(x.json())
