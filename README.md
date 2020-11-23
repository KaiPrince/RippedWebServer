# RippedWebServer

A web server written in Flask + Elm

## Install

Requirements:

- Python
- Yarn

Compile Elm

```
yarn build
```

Install pip requirements

```
cd server
pip install -r requirements.txt
```

## Running

Optional: Set development mode (_powershell_)

```
$env:FLASK_ENV="development"
```

Run Flask

```
cd server
flask run
```

## TODO

- [ ] Accessibility pass
- [x] Styling with <s>Tailwind</s> Bootstrap
- [ ] Theming
- [ ] File previews
- [ ] Authentication & link tokens (expirable)
- [x] Full Elm integration
- [x] Upload progress bar
- [x] Large file uploads
- [ ] Public links
- [x] File Storage microservice
- [ ] Service registry
- [ ] Users microservice
- [ ] File Storage auto-deploy?
- [x] Split docker-compose across microservices
- [ ] Convert files app to Eve
- [ ] Add exception handling and remove file from db if creation fails
- [ ] Register logging service
- [ ] Handle filename overlap by altering filename (filename_2)
- [ ] Fix CI
- [ ] Move repo urls to config and get from env.
