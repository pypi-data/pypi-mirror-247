import http, time, json
from typing import Dict, Callable, Any, AsyncIterator, Tuple, overload
from email.utils import formatdate

from CheeseAPI.file import File

contentTypes = {
    'tif': 'image/tiff',
    '001': 'application/x-001',
    '301': 'application/x-301',
    '323': 'text/h323',
    '906': 'application/x-906',
    '907': 'drawing/907',
    'a11': 'application/x-a11',
    'acp': 'audio/x-mei-aac',
    'ai': 'application/postscript',
    'aif': 'audio/aiff',
    'aifc': 'audio/aiff',
    'aiff': 'audio/aiff',
    'anv': 'application/x-anv',
    'asa': 'text/asa',
    'asf': 'video/x-ms-asf',
    'asp': 'text/asp',
    'asx': 'video/x-ms-asf',
    'au': 'audio/basic',
    'avi': 'video/avi',
    'awf': 'application/vnd.adobe.workflow',
    'biz': 'text/xml',
    'bmp': 'application/x-bmp',
    'bot': 'application/x-bot',
    'c4t': 'application/x-c4t',
    'c90': 'application/x-c90',
    'cal': 'application/x-cals',
    'cat': 'application/vnd.ms-pki.seccat',
    'cdf': 'application/x-netcdf',
    'cdr': 'application/x-cdr',
    'cel': 'application/x-cel',
    'cer': 'application/x-x509-ca-cert',
    'cg4': 'application/x-g4',
    'cgm': 'application/x-cgm',
    'cit': 'application/x-cit',
    'class': 'java/*',
    'cml': 'text/xml',
    'cmp': 'application/x-cmp',
    'cmx': 'application/x-cmx',
    'cot': 'application/x-cot',
    'crl': 'application/pkix-crl',
    'crt': 'application/x-x509-ca-cert',
    'csi': 'application/x-csi',
    'css': 'text/css',
    'cut': 'application/x-cut',
    'dbf': 'application/x-dbf',
    'dbm': 'application/x-dbm',
    'dbx': 'application/x-dbx',
    'dcd': 'text/xml',
    'dcx': 'application/x-dcx',
    'der': 'application/x-x509-ca-cert',
    'dgn': 'application/x-dgn',
    'dib': 'application/x-dib',
    'dll': 'application/x-msdownload',
    'doc': 'application/msword',
    'dot': 'application/msword',
    'drw': 'application/x-drw',
    'dtd': 'text/xml',
    'dwf': 'Model/vnd.dwf',
    'dwf': 'application/x-dwf',
    'dwg': 'application/x-dwg',
    'dxb': 'application/x-dxb',
    'dxf': 'application/x-dxf',
    'edn': 'application/vnd.adobe.edn',
    'emf': 'application/x-emf',
    'eml': 'message/rfc822',
    'ent': 'text/xml',
    'epi': 'application/x-epi',
    'eps': 'application/x-ps',
    'etd': 'application/x-ebx',
    'exe': 'application/x-msdownload',
    'fax': 'image/fax',
    'fdf': 'application/vnd.fdf',
    'fif': 'application/fractals',
    'fo': 'text/xml',
    'frm': 'application/x-frm',
    'g4': 'application/x-g4',
    'gbr': 'application/x-gbr',
    '': 'application/x-',
    'gif': 'image/gif',
    'gl2': 'application/x-gl2',
    'gp4': 'application/x-gp4',
    'hgl': 'application/x-hgl',
    'hmr': 'application/x-hmr',
    'hpg': 'application/x-hpgl',
    'hpl': 'application/x-hpl',
    'hqx': 'application/mac-binhex40',
    'hrf': 'application/x-hrf',
    'hta': 'application/hta',
    'htc': 'text/x-component',
    'htm': 'text/html',
    'html': 'text/html',
    'htt': 'text/webviewhtml',
    'htx': 'text/html',
    'icb': 'application/x-icb',
    'ico': 'image/x-icon',
    'iff': 'application/x-iff',
    'ig4': 'application/x-g4',
    'igs': 'application/x-igs',
    'iii': 'application/x-iphone',
    'img': 'application/x-img',
    'ins': 'application/x-internet-signup',
    'isp': 'application/x-internet-signup',
    'IVF': 'video/x-ivf',
    'java': 'java/*',
    'jfif': 'image/jpeg',
    'jpe': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'js': 'application/x-javascript',
    'jsp': 'text/html',
    'la1': 'audio/x-liquid-file',
    'lar': 'application/x-laplayer-reg',
    'latex': 'application/x-latex',
    'lavs': 'audio/x-liquid-secure',
    'lbm': 'application/x-lbm',
    'lmsff': 'audio/x-la-lms',
    'ls': 'application/x-javascript',
    'ltr': 'application/x-ltr',
    'm1v': 'video/x-mpeg',
    'm2v': 'video/x-mpeg',
    'm3u': 'audio/mpegurl',
    'm4e': 'video/mpeg4',
    'mac': 'application/x-mac',
    'man': 'application/x-troff-man',
    'math': 'text/xml',
    'mdb': 'application/msaccess',
    'mfp': 'application/x-shockwave-flash',
    'mht': 'message/rfc822',
    'mhtml': 'message/rfc822',
    'mi': 'application/x-mi',
    'mid': 'audio/mid',
    'midi': 'audio/mid',
    'mil': 'application/x-mil',
    'mml': 'text/xml',
    'mnd': 'audio/x-musicnet-download',
    'mns': 'audio/x-musicnet-stream',
    'mocha': 'application/x-javascript',
    'movie': 'video/x-sgi-movie',
    'mp1': 'audio/mp1',
    'mp2': 'audio/mp2',
    'mp2v': 'video/mpeg',
    'mp3': 'audio/mp3',
    'mp4': 'video/mpeg4',
    'mpa': 'video/x-mpg',
    'mpd': 'application/vnd.ms-project',
    'mpe': 'video/x-mpeg',
    'mpeg': 'video/mpg',
    'mpg': 'video/mpg',
    'mpga': 'audio/rn-mpeg',
    'mpp': 'application/vnd.ms-project',
    'mps': 'video/x-mpeg',
    'mpt': 'application/vnd.ms-project',
    'mpv': 'video/mpg',
    'mpv2': 'video/mpeg',
    'mpw': 'application/vnd.ms-project',
    'mpx': 'application/vnd.ms-project',
    'mtx': 'text/xml',
    'mxp': 'application/x-mmxp',
    'net': 'image/pnetvue',
    'nrf': 'application/x-nrf',
    'nws': 'message/rfc822',
    'odc': 'text/x-ms-odc',
    'out': 'application/x-out',
    'p10': 'application/pkcs10',
    'p12': 'application/x-pkcs12',
    'p7b': 'application/x-pkcs7-certificates',
    'p7c': 'application/pkcs7-mime',
    'p7m': 'application/pkcs7-mime',
    'p7r': 'application/x-pkcs7-certreqresp',
    'p7s': 'application/pkcs7-signature',
    'pc5': 'application/x-pc5',
    'pci': 'application/x-pci',
    'pcl': 'application/x-pcl',
    'pcx': 'application/x-pcx',
    'pdf': 'application/pdf',
    'pdx': 'application/vnd.adobe.pdx',
    'pfx': 'application/x-pkcs12',
    'pgl': 'application/x-pgl',
    'pic': 'application/x-pic',
    'pko': 'application/vnd.ms-pki.pko',
    'pl': 'application/x-perl',
    'plg': 'text/html',
    'pls': 'audio/scpls',
    'plt': 'application/x-plt',
    'png': 'image/png',
    'pot': 'application/vnd.ms-powerpoint',
    'ppa': 'application/vnd.ms-powerpoint',
    'ppm': 'application/x-ppm',
    'pps': 'application/vnd.ms-powerpoint',
    'ppt': 'application/vnd.ms-powerpoint',
    'pr': 'application/x-pr',
    'prf': 'application/pics-rules',
    'prn': 'application/x-prn',
    'prt': 'application/x-prt',
    'ps': 'application/postscript',
    'ptn': 'application/x-ptn',
    'pwz': 'application/vnd.ms-powerpoint',
    'r3t': 'text/vnd.rn-realtext3d',
    'ra': 'audio/vnd.rn-realaudio',
    'ram': 'audio/x-pn-realaudio',
    'ras': 'application/x-ras',
    'rat': 'application/rat-file',
    'rdf': 'text/xml',
    'rec': 'application/vnd.rn-recording',
    'red': 'application/x-red',
    'rgb': 'application/x-rgb',
    'rjs': 'application/vnd.rn-realsystem-rjs',
    'rjt': 'application/vnd.rn-realsystem-rjt',
    'rlc': 'application/x-rlc',
    'rle': 'application/x-rle',
    'rm': 'application/vnd.rn-realmedia',
    'rmf': 'application/vnd.adobe.rmf',
    'rmi': 'audio/mid',
    'rmj': 'application/vnd.rn-realsystem-rmj',
    'rmm': 'audio/x-pn-realaudio',
    'rmp': 'application/vnd.rn-rn_music_package',
    'rms': 'application/vnd.rn-realmedia-secure',
    'rmvb': 'application/vnd.rn-realmedia-vbr',
    'rmx': 'application/vnd.rn-realsystem-rmx',
    'rnx': 'application/vnd.rn-realplayer',
    'rp': 'image/vnd.rn-realpix',
    'rpm': 'audio/x-pn-realaudio-plugin',
    'rsml': 'application/vnd.rn-rsml',
    'rt': 'text/vnd.rn-realtext',
    'rtf': 'application/msword',
    'rv': 'video/vnd.rn-realvideo',
    'sam': 'application/x-sam',
    'sat': 'application/x-sat',
    'sdp': 'application/sdp',
    'sdw': 'application/x-sdw',
    'sit': 'application/x-stuffit',
    'slb': 'application/x-slb',
    'sld': 'application/x-sld',
    'slk': 'drawing/x-slk',
    'smi': 'application/smil',
    'smil': 'application/smil',
    'smk': 'application/x-smk',
    'snd': 'audio/basic',
    'sol': 'text/plain',
    'sor': 'text/plain',
    'spc': 'application/x-pkcs7-certificates',
    'spl': 'application/futuresplash',
    'spp': 'text/xml',
    'ssm': 'application/streamingmedia',
    'sst': 'application/vnd.ms-pki.certstore',
    'stl': 'application/vnd.ms-pki.stl',
    'stm': 'text/html',
    'sty': 'application/x-sty',
    'svg': 'text/xml',
    'swf': 'application/x-shockwave-flash',
    'tdf': 'application/x-tdf',
    'tg4': 'application/x-tg4',
    'tga': 'application/x-tga',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'tld': 'text/xml',
    'top': 'drawing/x-top',
    'torrent': 'application/x-bittorrent',
    'tsd': 'text/xml',
    'txt': 'text/plain',
    'uin': 'application/x-icq',
    'uls': 'text/iuls',
    'vcf': 'text/x-vcard',
    'vda': 'application/x-vda',
    'vdx': 'application/vnd.visio',
    'vml': 'text/xml',
    'vpg': 'application/x-vpeg005',
    'vsd': 'application/vnd.visio',
    'vss': 'application/vnd.visio',
    'vst': 'application/vnd.visio',
    'vsw': 'application/vnd.visio',
    'vsx': 'application/vnd.visio',
    'vtx': 'application/vnd.visio',
    'vxml': 'text/xml',
    'wav': 'audio/wav',
    'wax': 'audio/x-ms-wax',
    'wb1': 'application/x-wb1',
    'wb2': 'application/x-wb2',
    'wb3': 'application/x-wb3',
    'wbmp': 'image/vnd.wap.wbmp',
    'wiz': 'application/msword',
    'wk3': 'application/x-wk3',
    'wk4': 'application/x-wk4',
    'wkq': 'application/x-wkq',
    'wks': 'application/x-wks',
    'wm': 'video/x-ms-wm',
    'wma': 'audio/x-ms-wma',
    'wmd': 'application/x-ms-wmd',
    'wmf': 'application/x-wmf',
    'wml': 'text/vnd.wap.wml',
    'wmv': 'video/x-ms-wmv',
    'wmx': 'video/x-ms-wmx',
    'wmz': 'application/x-ms-wmz',
    'wp6': 'application/x-wp6',
    'wpd': 'application/x-wpd',
    'wpg': 'application/x-wpg',
    'wpl': 'application/vnd.ms-wpl',
    'wq1': 'application/x-wq1',
    'wr1': 'application/x-wr1',
    'wri': 'application/x-wri',
    'wrk': 'application/x-wrk',
    'ws': 'application/x-ws',
    'ws2': 'application/x-ws',
    'wsc': 'text/scriptlet',
    'wsdl': 'text/xml',
    'wvx': 'video/x-ms-wvx',
    'xdp': 'application/vnd.adobe.xdp',
    'xdr': 'text/xml',
    'xfd': 'application/vnd.adobe.xfd',
    'xfdf': 'application/vnd.adobe.xfdf',
    'xhtml': 'text/html',
    'xls': 'application/vnd.ms-excel',
    'xlw': 'application/x-xlw',
    'xml': 'text/xml',
    'xpl': 'audio/scpls',
    'xq': 'text/xml',
    'xql': 'text/xml',
    'xquery': 'text/xml',
    'xsd': 'text/xml',
    'xsl': 'text/xml',
    'xslt': 'text/xml',
    'xwd': 'application/x-xwd',
    'x_b': 'application/x-x_b',
    'sis': 'application/vnd.symbian.install',
    'sisx': 'application/vnd.symbian.install',
    'x_t': 'application/x-x_t',
    'ipa': 'application/vnd.iphone',
    'apk': 'application/vnd.android.package-archive',
    'xap': 'application/x-silverlight-app',
}

class BaseResponse:
    def __init__(self, body: str | bytes | Callable | None = None, status: http.HTTPStatus | int = http.HTTPStatus.OK, headers: Dict[str, str] = {}):
        self.status: http.HTTPStatus = http.HTTPStatus(status)
        self.headers: Dict[str, str] = {
            'Server': 'CheeseAPI',
            'Transfer-Encoding': 'chunked'
        }
        self.headers.update(headers)
        self.body: str | bytes | Callable = body
        if self.body is None:
            self.body = self.status.description

        self.transfering: bool = False

    async def __call__(self) -> Tuple[bytes, bool]:
        if not self.transfering:
            content = [ b''.join([ b'HTTP/1.1 ', str(self.status).encode(), b' ', http.HTTPStatus(self.status).phrase.encode(), b'\r\n' ]) ]

            if isinstance(content, AsyncIterator):
                self.headers['Transfer-Encoding'] = 'chunked'
            self.headers['Date'] = formatdate(time.time(), usegmt = True)
            for key, value in self.headers.items():
                content.extend([ key.encode(), b': ', value.encode(), b'\r\n' ])

            content.append(b'\r\n')
            self.transfering = True
            return b''.join(content)
        else:
            self.transfering = False

            content = self.body
            if isinstance(content, Callable):
                content = content()
            elif isinstance(content, AsyncIterator):
                try:
                    content = await anext(content)
                    self.transfering = True
                except StopAsyncIteration:
                    return b'0\r\n\r\n', False

            if not isinstance(content, bytes):
                content = str(content).encode()

            if self.headers.get('Transfer-Encoding') == 'chunked':
                content = [ b'%x\r\n' % len(content), content, b'\r\n' ]
                if not self.transfering:
                    content.append(b'0\r\n\r\n')

            return b''.join(content), self.transfering

class Response(BaseResponse):
    def __init__(self, body: str | bytes | Callable | None = None, status: http.HTTPStatus | int = http.HTTPStatus.OK, headers: Dict[str, str] = {}):
        _headers = {
            'content-type': 'text/plain; charset=utf-8'
        }
        _headers.update(headers)
        super().__init__(body, status, _headers)

class JsonResponse(BaseResponse):
    def __init__(self, body: Dict[str, Any] = {}, status: http.HTTPStatus | int = http.HTTPStatus.OK, headers: Dict[str, str] = {}):
        _headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        _headers.update(headers)
        super().__init__(json.dumps(body), status, _headers)

class FileResponse(BaseResponse):
    @overload
    def __init__(self, filePath: str, downloaded: bool = False, headers: Dict[str, str] = {}):
        ...

    @overload
    def __init__(self, fileData: File, downloaded: bool = False, headers: Dict[str, str] = {}):
        ...

    def __init__(self, data: str | File, downloaded: bool = False, headers: Dict[str, str] = {}):
        if isinstance(data, str):
            from CheeseAPI.app import app

            if data[0] == '.':
                filePath = app.workspace.base + '/' + data

            try:
                with open(filePath, 'rb') as f:
                    data = f.read()
            except:
                raise FileNotFoundError('The file was not found')

            fileSuffix = filePath.split('.')[-1]

        elif isinstance(data, File):
            fileSuffix = data.name
            data = data.data

        if downloaded or fileSuffix not in contentTypes:
            _headers = { 'content-type': 'application/octet-stream' }
        else:
            _headers = { 'content-type': contentTypes[fileSuffix] }
        _headers.update(headers)
        super().__init__(data, http.HTTPStatus.OK, _headers)
