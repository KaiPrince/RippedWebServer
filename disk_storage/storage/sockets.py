"""
 * Project Name: RippedWebServer
 * File Name: sockets.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 29, 2020
 * Description: This file contains the socketio module.
"""

from flask import Flask
from flask_socketio import SocketIO

socket_io = SocketIO()


def init_app(app: Flask):
    socket_io.init_app(app)
