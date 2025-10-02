# Backend Integration Test

This repository contains a **Python** script that processes a BIND Server Log file and sends it to Lumu Custom Collector API.

## Execution

To execute the script, run:
```bash
python script.py <your_query_file_name>
```

## Requirements

- Define your environment variables:

On linux:

```bash
export COLLECTOR_ID="your_collector_id"
export LUMU_CLIENT_KEY="your_client_key"
```
On Windows:

```powershell
setx COLLECTOR_ID "your_collector_id"
setx LUMU_CLIENT_KEY "your_client_key"
```

- Install 'requests' package:

```bash
pip install requests
```

## Expected Output
A summary of parsed data as follows:
![Expected Output](https://res.cloudinary.com/donrhclb6/image/upload/v1759446106/ParsedDATA_jychji.png)