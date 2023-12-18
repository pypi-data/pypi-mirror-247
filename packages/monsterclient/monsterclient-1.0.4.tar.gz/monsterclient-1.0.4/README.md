#### how to build?

1. create venv

`python3 -m venv <venv>`

2. build

```
source <venv>/bin/activate

python -m build

pip install dist/monsterclient-1.0.3-py3-none-any.whl

```

#### how to use?

set this variables in .bashrc:

for AUTH version 1

```
export ST_AUTH=http://127.0.0.1:8080/auth/v1.0
export ST_USER=test:tester
export ST_KEY=testing
export ST_URL=http://127.0.0.1:8080/v1/AUTH_test

```
for AUTH version 3
```
export OS_MONSTER_URL=http://127.0.0.1:8080  
export OS_USERNAME=tester
export OS_PASSWORD=testing
export OS_AUTH_URL="http://127.0.0.1:5000"
export OS_PROJECT_NAME="test"
export OS_USER_DOMAIN="default"
export OS_PROJ_DOMAIN="default"
```

`pip install monsterclient`

enjoy :)


##### commands

1. put

```
monster put <container>
monster put <container> <object>
```

2. delete

```
monster delete <container>
monster delete <container> <object>
```

3. get

```
monster get
monster get <container>
monster get <container> <object>
```

4. head

```
monster head
monster head <container>
monster head <container> <object>
```

5. post

```
monster post --meta key:value
monster post <container> --meta key:value
monster post <container> <object> --meta key:value
```

6. info

```
monster info
```

* to see curl command use `-c` or `--curl` option. for example:

```
monster put <container> --curl
```