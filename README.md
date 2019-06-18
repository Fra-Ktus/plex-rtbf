plex-rtbf
===============

Plex plugin for video's from RTBF http://www.rtbf.be/auvio/

Because the PLEX plug in SDK does not support very well https and the RTBF made it mandatory to use it made the fix complicated.

The plug-in now needs a proxy to query the website.

This explains how to setup a proxy:
https://forums.plex.tv/t/https-broken/216635/16

The plex_proxy.js is the minimal file to create a proxy on your Plex server.

This is how the plug-in is browsing the RTBF website:
http://localhost:8006/auvio/categorie/info?id=1

