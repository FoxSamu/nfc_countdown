# How to use
- Clone this repository
- Navigate into the cloned repository
- Create a file `config.json` and add the following:
  ```
  {
      "edition_url": "https://shadew.net/assets/nfcdata.json"
  }
  ```
- Install required modules
  ```
  pip3 install -r requirements.txt
  ```
- The repository contains a file `server.sh`, run this script using `bash`
  ```bash
  bash server.sh
  ```

  Alternatively, run the Python command itself (not recommended)
  ```bash
  python3 server.py
  ```

The `server.sh` file can be configured to run as a UNIX service.