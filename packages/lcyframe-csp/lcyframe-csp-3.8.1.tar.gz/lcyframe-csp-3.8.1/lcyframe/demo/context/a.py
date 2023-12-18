from envyaml import EnvYAML
from lcyframe.libs import yaml2py

"""
localhost.yml
env_name: $PYTHONUNBUFFERED
env_name: ${PYTHONUNBUFFERED}
"""
# read file env.yml and parse config
# 支持yml里读取环境变量key: $env
# 读取方式：env["wsgi"]["host"] or env["wsgi.host"]
env = EnvYAML('localhost.yml')
print(env['env_name'])

env2 = yaml2py.load_confog('localhost.yml')
print(env2['env_name'])     # 不支持读取环境变量

