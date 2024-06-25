# Python ChatBot Project

This project is a Python-based chatbot that utilizes various libraries to provide functionalities like responding to user queries, checking server status, and more. It's structured to be modular, with separate components for different tasks.

## TODO

- Adding a system so that people don't spam queries (and getting that so that the system can adjust to meet spending limits)

- Building an informed query section, that can search up good context.

- Creating a proompter section, which asks a question based on some news -> probably add some schedulability.

## Features

- **[ChatBot Prompts](cogs/ChatBotPrompts.py)**: Handles dynamic conversation flows.
- **[Ping](cogs/Ping.py)**: Checks and reports server status.
- **[Status](cogs/Status.py)**: Provides the current status of the chatbot.

## Dependencies

The project relies on several third-party libraries, including:

- `urllib3` for HTTP requests.
- `websockets` for WebSocket communication.
- `aiohttp` for asynchronous HTTP requests.
- `distro` for Linux distribution information.
- `sniffio` for detecting the async library in use.
- `openai` for accessing OpenAI's APIs.

For a full list of dependencies, refer to the [requirements.txt](requirements.txt) file.

## Installation

1. Clone the [repository](https://github.com/Elias2660/Proompter):

   ```shell
   git clone git@github.com:Elias2660/Proompter.git
   ```

2. Create a virtual environment:

   ```shell
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```powershell
     .\venv\Scripts\activate
     ```

   - On Unix or MacOS:

     ```sh
     source venv/bin/activate
     ```

4. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the chatbot:

```sh
python main.py
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to discuss potential improvements or features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
