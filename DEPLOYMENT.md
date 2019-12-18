### Initial Setup

See [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04) for initial server setup.

Create the directories:

```
sudo mkdir -p /var/app/decidel
sudo chown -R $USER:$USER /var/app/decidel
sudo mkdir -p /var/log/decidel
sudo chown -R $USER:$USER /var/log/decidel
```

Create `/etc/systemd/system/decidel.service` to run the app under supervision:

```
[Unit]
Description=uWSGI instance to serve decidel
After=network.target

[Service]
User=<non-root-user>
Group=www-data
WorkingDirectory=/var/app/decidel
Environment="PATH=/var/app/decidel/venv/bin"
ExecStart=/var/app/decidel/venv/bin/uwsgi --ini decidel.ini

[Install]
WantedBy=multi-user.target
```

Start the service and set it to run on boot:

```
sudo systemctl start decidel
sudo systemctl enable decidel
```

Setup nginx directive:

```
# /etc/nginx/sites-available/api.decidel.ca

server {

		# ssl directives
		...


    server_name api.decidel.ca;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/app/decidel/decidel.sock;
    }
}
```

```
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

Install redis:

* https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04
* https://www.digitalocean.com/community/tutorials/how-to-back-up-and-restore-your-redis-data-on-ubuntu-14-04

Make sure `REDIS_URL` is set correctly in /var/app/decidel/instance/config.py

### Deploying updates

Actual deployment is handled by the [Deploy Action](.github/workflows/deploy.yml).
