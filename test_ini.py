import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                      'CompressionLevel': '9'}
config['bitbucket.org'] = {}
config['bitbucket.org']['User'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Port'] = '50022'     # mutates the parser
topsecret['ForwardX11'] = 'no'  # same here
config['DEFAULT']['ForwardX11'] = 'yes'
with open('example.ini', 'w') as configfile:
    config.write(configfile)

config = configparser.ConfigParser()
config.sections()
config.read('example.ini')
config.sections()
'bitbucket.org' in config
'bytebong.com' in config
config['bitbucket.org']['User']
config['DEFAULT']['Compression']
topsecret['ForwardX11']
topsecret['Port']
for key in config['bitbucket.org']:
    print(key)
config['bitbucket.org']['ForwardX11']

config =configparser.ConfigParser()
config.sections()
print('-----------------')
config.read('FILE.INI')
print(config['DEFAULT']['w_path'])