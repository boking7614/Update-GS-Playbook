import glob
import yaml

new_cert = ['00-godaddy-root.cer', 'demo.net.crt', 'demo.net-dec.key']

ssl_path = glob.glob('C:\server\*\*\gs_release\ssl')
dict_file = {'cert': new_cert, 'path': ssl_path}

with open(r'sslpath_info.yml', 'w') as file:
    documents = yaml.dump(dict_file, file)
