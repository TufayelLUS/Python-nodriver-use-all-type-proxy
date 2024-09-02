# Python nodriver - How to Use All Types of Proxy
Nodriver library is an official successor of the undetected chromedriver library that is widely used to prevent bot detection while automating any websites. There are many websites that undetected chromedriver files to bypass the bot verification system and nodriver have done a wonderful job in bypassing those exceptions. Nodriver implementation also removes the maintenance of matching webdriver software too. This repository is a demonstration of how to use a proxy in nodriver library of Python. It shows how to use an authentication based proxy in nodriver and also how to use a normal proxy in the nodriver library.

# Installation command
<pre>pip install nodriver</pre>

# Documentation Page Link for nodriver Library
<a href="https://ultrafunkamsterdam.github.io/nodriver/">Click here</a>

# Supported format of proxy
<pre>protocol://host:port<br>protocol://username:password:host:port</pre>

# How does it work?
As we know the Chrome argument variable doesn't support auth-based proxies to be used as an argument parameter, it creates a custom Chrome plugin with the proxy information and loads it when the Chrome browser starts. This allows all types of proxies to be used with no problems. This approach has been tested as working, thanks to the original developer of this Chrome plugin source code.

# Loved it?
Please share your appreciation by giving this repository a ⭐ and share it with your friends who might need it.
