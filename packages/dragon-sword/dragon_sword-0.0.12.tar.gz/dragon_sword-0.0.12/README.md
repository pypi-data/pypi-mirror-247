common tool

```shell
python setup.py sdist build
pip install twine
twine upload dist/*
```

有外部依赖的，不要在包的__init__里初始化

禁止使用相对import，一脚本，而难调