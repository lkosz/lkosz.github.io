#!/usr/bin/env python3

import os, sys, time, yaml

with open("site.yaml", "r") as stream:
  config = yaml.safe_load(stream)

f = open(config['source'], 'r')
main_template = f.read()
f.close()
for key in config['keys'].keys():
  if not '<%=@@@' + key + '@@@=%>' in main_template:
    print('For key: ' + key + ', can\'t find anchor: ' + '<%=@@@' + key + '@@@=%> in file: ' + config['source'])
    sys.exit(1)
  total_content = ''
  for content in config['keys'][key]:
    f = open(content['file'], 'r')
    file_content = f.read()
    file_content_duplicate = file_content
    f.close()
    if 'parameters' in content.keys():
      for paramkey in content['parameters'].keys():
        paramval = content['parameters'][paramkey]
        if not '<%=@@@' + paramkey + '@@@=%>' in file_content:
          print('For key: ' + paramkey + ', can\'t find anchor: ' + '<%=@@@' + paramkey + '@@@=%> in file: ' + content['file'])
          sys.exit(1)
        file_content = file_content.replace('<%=@@@' + paramkey + '@@@=%>',  paramval)
        if 'duplicate' in content.keys():
          if paramkey in content['duplicate'].keys():
            file_content_duplicate = file_content_duplicate.replace('<%=@@@' + paramkey + '@@@=%>',  content['duplicate'][paramkey])
          else:
            file_content_duplicate = file_content_duplicate.replace('<%=@@@' + paramkey + '@@@=%>',  paramval)
      total_content += '\n' + file_content + '\n'
      if 'duplicate' in content.keys():
        total_content += '\n' + file_content_duplicate + '\n'
    else:
      total_content += '\n' + file_content + '\n'
  main_template = main_template.replace('<%=@@@' + key + '@@@=%>',  total_content)

f = open(config['target'], 'w')
f.write(main_template)
f.close()
