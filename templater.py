#!/usr/bin/env python3

import os, sys, time, yaml

with open("site.yaml", "r") as stream:
  config = yaml.safe_load(stream)

f = open(config['source'], 'r')
main_template = f.read()
f.close()
for key in config['keys'].keys():
  if not f'<%=@@@{key}@@@=%>' in main_template:
    print(f'For key: {key}, can\'t find anchor: <%=@@@{key}@@@=%> in file: {config["source"]}')
    sys.exit(1)
  total_content = ''
  for content in config['keys'][key]:
    f = open(content['file'], 'r')
    file_content = f.read()
    file_content_duplicate = file_content
    f.close()

    description = ''
    description_params = ['object_number', 'object_name', 'date', 'telescope', 'mount', 'camera', 'filters', 'expositions', 'sky', 'extra_description']
    for par in description_params:
      if 'parameters' in content.keys() and par in content['parameters'].keys() and content['parameters'][par] != '':
        if description == '':
          description = f"{content['parameters'][par]}"
        else:
          description = f"{description}  ||  {content['parameters'][par]}"
    file_content_duplicate = file_content_duplicate.replace('<%=@@@description@@@=%>',  description)
    file_content = file_content.replace('<%=@@@description@@@=%>',  description)

    if 'parameters' in content.keys():
      for paramkey in content['parameters'].keys():
        if paramkey in list(set(description_params) - set(['object_number', 'object_name', 'date'])):
          continue
        paramval = content['parameters'][paramkey]
        if not f'<%=@@@{paramkey}@@@=%>' in file_content:
          print(f'For key: {paramkey}, can\'t find anchor: <%=@@@{paramkey}@@@=%> in file: {content["file"]}')
          sys.exit(1)
        file_content = file_content.replace(f'<%=@@@{paramkey}@@@=%>',  paramval)
        if 'duplicate' in content.keys():
          if paramkey in content['duplicate'].keys():
            file_content_duplicate = file_content_duplicate.replace(f'<%=@@@{paramkey}@@@=%>',  content['duplicate'][paramkey])
          else:
            file_content_duplicate = file_content_duplicate.replace(f'<%=@@@{paramkey}@@@=%>',  paramval)
      total_content += '\n' + file_content + '\n'
      if 'duplicate' in content.keys():
        total_content += '\n' + file_content_duplicate + '\n'
    else:
      total_content += '\n' + file_content + '\n'
  main_template = main_template.replace(f'<%=@@@{key}@@@=%>',  total_content)

f = open(config['target'], 'w')
f.write(main_template)
f.close()
