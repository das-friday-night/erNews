import yaml

f = open('config.yaml')
dataMap = yaml.load(f)
print dataMap
f.close()