import requests

url = "http://localhost:8000/assignWithCsv/upload"
files = {"file": ("hayal_300_no_status.csv", open("hayal_300_no_status.csv", "rb"), "text/csv")}
params = {"has_header": "true"}
response = requests.post(url, files=files, params=params)

print(response.status_code)
print(response.json())
