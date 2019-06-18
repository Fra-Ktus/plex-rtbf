var httpProxy = require('http-proxy');
httpProxy.createServer({changeOrigin: true, target: 'https://www.rtbf.be'}).listen(8006);
