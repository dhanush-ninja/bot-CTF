# Discord Bot for CTF

## Description

This bot creates channels for CTF (Capture The Flag) competitions. It is designed to help manage and organize CTF challenges and resources within a Discord server, allowing for seamless collaboration and competition among participants.

## Getting Started

### Installing

- Clone this repository to your local machine.
- Ensure that you have Python installed on your system.

### Setting up `.env`

Create a `.env` file in the root directory of your project and add the following lines:

```env
DISCORD_TOKEN=your_discord_token_here
SECRET_KEY=your_secret_key_here
```

Replace `your_discord_token_here` and `your_secret_key_here` with your actual Discord token and secret key.

### Executing program

- Install the required dependencies:

```bash
pip install -r requirements.txt
```

- Run the bot by executing:

```bash
python app.py
```

## Help

Any advise for common problems or issues.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details


In my updated code 
Run this server by navigating into the folder Discord_bot   and run the below command.

uvicorn app.main:app --reload