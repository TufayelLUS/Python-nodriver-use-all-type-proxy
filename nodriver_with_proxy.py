import zipfile
import os
from time import sleep
import nodriver as uc
from nodriver import Config
from bs4 import BeautifulSoup as bs

# pip install nodriver bs4


# only these two format is allowed, the proxy protocol can be set accordingly too
proxy = "http://username:password:host:port"
proxy_2 = "http://host:port"


def createProxyPlugin(PROTOCOL, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "%s",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROTOCOL, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)


def getConfigWithNewProxy(proxy):
    config = Config()
    picked_proxy = proxy
    print("Proxy selected for the session: {}".format(picked_proxy))
    proxy_protocol = picked_proxy.split("://")[0]
    other_parts = picked_proxy.split("://")[1].split(':')
    if len(other_parts) == 4:
        proxy_user = other_parts[0]
        proxy_pass = other_parts[1]
        proxy_host = other_parts[2]
        proxy_port = other_parts[3]
        createProxyPlugin(proxy_protocol, proxy_host,
                          proxy_port, proxy_user, proxy_pass)
        config.add_extension(os.path.join(
            os.getcwd(), "proxy_auth_plugin.zip"))
    else:
        config.add_argument("--proxy-server={}".format(picked_proxy))
    # config.add_argument("--blink-settings=imagesEnabled=false")
    return config


async def getPageData():
    driver = await uc.start(config=getConfigWithNewProxy(proxy))
    sleep(1)
    page = await driver.get("http://www.google.com")
    page_html = await page.get_content()
    soup = bs(page_html, 'html.parser')
    # now get any element using soup
    await driver.stop()

    # start another instance with a difference proxy
    driver = await uc.start(config=getConfigWithNewProxy(proxy_2))
    sleep(1)
    page = await driver.get("http://www.google.com")
    page_html = await page.get_content()
    soup = bs(page_html, 'html.parser')
    # now get any element using soup
    await driver.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(getPageData())
