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
- [ ] Upload progress bar
- [ ] Large file uploads
- [ ] Public links
- [ ] File Storage microservice
- [ ] Service registry
- [ ] Users microservice
- [ ] File Storage auto-deploy?
- [ ] Split docker-compose across microservices
- [ ] Convert files app to Eve
