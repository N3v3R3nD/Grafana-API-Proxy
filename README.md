Grafana Proxy

Grafana Proxy is a Flask application that allows you to proxy requests to a Grafana instance with an access token.
It also supports converting the 'from' and 'to' timestamps to a different timezone and applying a time shift.

Getting Started
To use Grafana Proxy, you'll need to have Python 3.x installed on your system.
You can download it from the official website: https://www.python.org/downloads/

You'll also need to install the required packages by running the following command:

Copy code
pip install -r requirements.txt
Configuration
Before you can start using Grafana Proxy, you'll need to configure it with your Grafana credentials. Open the proxy.py file in your preferred text editor and modify the following variables:

makefile
Copy code
token_url = "IP:8080/api/1/login/"
target_api_base_url = "IP:8080/api/1/"
username = "your_user"
password = "your_password"
You can also configure the logging behavior of the application by modifying the following variables:

makefile
Copy code
log_to_file = True
log_directory = "/var/log/grafana_proxy/"
If log_to_file is set to True, logs will be written to a file in the specified log_directory. Otherwise, logs will be printed to the console.

Running the Application
To start the Grafana Proxy, run the following command:

Copy code
python proxy.py
By default, the application will run on http://localhost:8081/. You can change the host and port by modifying the app.run() call in the if __name__ == '__main__': block.

Using the Proxy
Once the application is running, you can use it to proxy requests to your Grafana instance. To do this, simply replace the Grafana URL with the URL of your proxy server. For example, if your Grafana URL is http://localhost:3000/, you would use http://localhost:8081/ as the URL when configuring your data source in Grafana.

When using the proxy, you can also apply a timezone conversion and a time shift to the 'from' and 'to' timestamps. To do this, add the from and to query parameters to your request and specify the timestamps in the UTC timezone. The proxy will automatically convert the timestamps to the desired timezone and apply the time shift.

License
This project is licensed under the MIT License - see the LICENSE file for details.

I hope this helps! Let me know if you have any further questions or need any more assistance.
