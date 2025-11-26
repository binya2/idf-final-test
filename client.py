import requests

url = "http://localhost:8000/assignWithCsv"
files = {"file": ("hayal_300_no_status.csv", open("hayal_300_no_status.csv", "rb"), "text/csv")}
response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
