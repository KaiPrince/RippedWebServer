# RippedWebServer

A microservice-based web server written in Flask + Elm.

## Install

Requirements:

- Python
- Yarn
- Docker

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

### Production

Optional: Add `--build` to rebuild after changes.

```
docker-compose up
```

### Development

Optional: Set development mode (_powershell_)

```
$env:FLASK_ENV="development"
```

Run server

```
cd server
flask run
```

Run files service

```
cd files
flask run
```

Run disk storage service

```
cd disk_storage
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
- [x] Register logging service
- [ ] Handle filename overlap by altering filename (filename_2)
- [ ] Fix CI
- [ ] Move repo urls to config and get from env.
- [ ] Add file size
- [ ] only refresh auth token on protected routes
- [ ] only display refresh message on recently stale token
- [ ] create clipboard microservice
- [ ] one-time password for protected files "HKDTA"
- [ ] hash file path in sharing token and compare to request url
- [ ] Fix confusion of file_name and filename in server create view
- [ ] Prevent overwrite of duplicated file
- [ ] Add share token for viewing file details
- [ ] Show "you are being granted temporary access" message when using share token
