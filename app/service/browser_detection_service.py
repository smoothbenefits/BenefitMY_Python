import httpagentparser

def IsBrowserSupported(user_agent):

    parsed = httpagentparser.detect(user_agent)

    # For now, we only care about major version number
    version = int(parsed['browser']['version'].split('.')[0])
    browser = parsed['browser']['name']

    if (browser == 'Chrome' and version >= 40):
        return True

    if (browser == 'Firefox' and version > 18):
        return True

    if (browser == 'Microsoft Internet Explorer' and version > 9):
        return True

    if (browser == 'Safari' and version > 4):
        return True

    return False