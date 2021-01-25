const express = require('express');
// NOTE: For some reason, heroku throws a "module not found" error
// const ServiceRegistry = require('./lib/ServiceRegistry');


const semver = require('semver');

class ServiceRegistry {
  constructor(log) {
    this.log = log;
    this.services = {};
    this.timeout = 30;
  }

  get(name, version) {
    this.cleanup();
    const candidates = Object.values(this.services).filter(
      (service) =>
        service.name === name && semver.satisfies(service.version, version)
    );

    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  register(name, version, ip, port) {
    this.cleanup();
    const key = name + version + ip + port;

    if (!this.services[key]) {
      this.services[key] = {};
      this.services[key].timestamp = Math.floor(new Date() / 1000);
      this.services[key].ip = ip;
      this.services[key].port = port;
      this.services[key].name = name;
      this.services[key].version = version;
      this.log.debug(
        `Added services ${name}, version ${version} at ${ip}:${port}`
      );
      return key;
    }
    this.services[key].timestamp = Math.floor(new Date() / 1000);
    this.log.debug(
      `Updated services ${name}, version ${version} at ${ip}:${port}`
    );
    return key;
  }

  unregister(name, version, ip, port) {
    const key = name + version + ip + port;
    delete this.services[key];
    this.log.debug(
      `Unregistered services ${name}, version ${version} at ${ip}:${port}`
    );
    return key;
  }

  cleanup() {
    const now = Math.floor(new Date() / 1000);
    Object.keys(this.services).forEach((key) => {
      if (this.services[key].timestamp + this.timeout < now) {
        delete this.services[key];
        this.log.debug(`Removed service ${key}`);
      }
    });
  }
}

const service = express();

module.exports = (config) => {
  const log = config.log();
  const serviceRegistry = new ServiceRegistry(log);
  // Add a request logging middleware in development mode
  if (service.get('env') === 'development') {
    service.use((req, res, next) => {
      log.debug(`${req.method}: ${req.url}`);
      return next();
    });
  }

  service.put('/register/:servicename/:serviceversion/:serviceport', (req, res) => {
    const { servicename, serviceversion, serviceport } = req.params;

    const serviceip = req.connection.remoteAddress.includes('::') ? `[${req.connection.remoteAddress}]` : req.connection.remoteAddress;

    const serviceKey = serviceRegistry
      .register(servicename, serviceversion, serviceip, serviceport);
    return res.json({ result: serviceKey });
  });

  service.delete('/register/:servicename/:serviceversion/:serviceport', (req, res) => {
    const { servicename, serviceversion, serviceport } = req.params;

    const serviceip = req.connection.remoteAddress.includes('::') ? `[${req.connection.remoteAddress}]` : req.connection.remoteAddress;

    const serviceKey = serviceRegistry
      .unregister(servicename, serviceversion, serviceip, serviceport);
    return res.json({ result: serviceKey });
  });

  service.get('/find/:servicename/:serviceversion', (req, res) => {
    const { servicename, serviceversion } = req.params;
    const svc = serviceRegistry.get(servicename, serviceversion);
    if (!svc) return res.status(404).json({ result: 'Service not found' });
    return res.json(svc);
  });

  // eslint-disable-next-line no-unused-vars
  service.use((error, req, res, next) => {
    res.status(error.status || 500);
    // Log out the error to the console
    log.error(error);
    return res.json({
      error: {
        message: error.message,
      },
    });
  });
  return service;
};
