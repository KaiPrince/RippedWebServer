# RippedWebServer
A web server written in Flask + Elm

## Install
Requirements:
* Python
* Yarn

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

Optional: Set development mode
_powershell_
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
- [ ] File previews
- [ ] Authentication & link tokens (expirable)
- [x] Full Elm integration
- [ ] Upload progress bar
