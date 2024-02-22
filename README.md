# Platform-GPT Middleware

The Platform-GPT Middleware is a Python application that serves as a bridge between Slack, the OpenAI API, and user interactions. It allows you to receive requests from Slack, process them, send data in the right format to the OpenAI API, and return the response to the user within the same Slack thread. Additionally, it manages a conversation buffer and can call custom functions to fulfill user requests.

## Mission

The mission of platform-gpt is to streamline and automate routine requests directed to platform engineering, devops, or site reliability engineering teams. These requests may include tasks such as:

- User provisioning
- Kubernetes cluster health checks
- CPU/memory usage alerts
- Disk space alerts

It has been observed that a significant portion, approximately 60%, of the requests received by these teams are straightforward and can be efficiently addressed by an intelligent bot like platform-gpt.

Please note that platform-gpt is currently in the development phase and is not yet ready for production use. Our goal is to enhance its capabilities to provide a valuable and efficient resource for handling common inquiries and tasks.

## Features

- Seamless integration between Slack and the OpenAI API.
- Real-time response to user queries within Slack.
- Conversation history management.
- Custom function support for handling specific user requests.

## Prerequisites

Before running the middleware, make sure you have the following:

1. An OpenAI API account with an API key.
2. A Slack account and a Slack token.
3. A Sentry account (optional but recommended for error tracking).

## How to Run

Follow these steps to set up and run the Platform-GPT Middleware:

1. Clone the Repository:

   ```shell
   git clone https://github.com/nitesh8860/platform-gpt
   cd platform-gpt
   ```

2. Create a Configuration File:

   Copy the `.env.example` file to `.env` and update the values:

3. Set Up a Virtual Environment:

   Create and activate a Python virtual environment:

   ```shell
   python -m venv venv
   source venv/bin/activate
   ```

4. Install Dependencies:

   Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

5. Run the Middleware:

   Start the middleware application using Uvicorn:

   ```shell
   uvicorn app.main:app --reload
   ```

## Custom Functions

You can extend the middleware by defining custom functions to handle specific user requests. Explore the `app` directory to add your custom logic in `custom_functions.py`.

## Architecture

![Screenshot 1](screenshots/3.png)

## Chat Screenshots

Explore the application with these screenshots:

![Screenshot 1](screenshots/1.png)

![Screenshot 2](screenshots/2.png)

## Error Tracking (Sentry)

For improved error tracking and monitoring, consider setting up Sentry with your middleware. This is optional but highly recommended for a production environment.

## Contributing

Contributions to this middleware are welcome! Feel free to enhance its functionality or fix any issues. Please create a pull request for your changes.

## License

This project is available under the [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).

Enjoy seamless interactions between Slack and the OpenAI API with Platform-GPT Middleware!

## NOTE

Database is not in use and yet to be implemented.
