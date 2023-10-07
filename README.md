# How to use
- Clone this repository
- Navigate into the cloned repository
- Create a file `config.json` and add the following:
  ```
  {
      "edition_url": "https://shadew.net/assets/nfcdata.json",
    
      "info_json_url": "https://shadew.net/nfc/info.json",
      "banner_image_url": "https://shadew.net/nfc/banner_800.png",

      "telegram_token": "<insert telegram bot token>",
      "telegram_channel": "@<insert telegram channel name>"
  }
  ```

# Running using docker compose
- This is very straightforward:
  ```
  docker compose up -d
  ```


# Running manually
- Install required modules
  ```
  pip3 install -r requirements.txt
  ```

## Start the server
- The repository contains a file `server.sh`, run this script using `bash`.
  The script will pipe the program output into a local log file.
  ```bash
  bash server.sh
  ```

  Alternatively, run the Python command itself, to get the program output
  into the console.
  ```bash
  python3 server.py
  ```

## Start the posting service
- The repository contains a file `post_service.sh`, run this script using `bash`.
  The script will pipe the program output into a local log file.
  ```bash
  bash server.sh
  ```

  Alternatively, run the Python command itself, to get the program output
  into the console.
  ```bash
  python3 post_service.py
  ```

The `server.sh` and `post_service.sh` files can be configured to run as a UNIX service.