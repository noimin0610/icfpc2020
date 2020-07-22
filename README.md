# ICFPC2020 Team Fortius

Team Fortius's repogitory for [ICFP Programming Contest 2020](https://icfpcontest2020.github.io/#/)

Guaranteed to work with [starterkit-python](https://github.com/icfpcontest2020/starterkit-python).
Base image `icfpcontest2020/python:latest` built automatically from `Dockerfile.base`.

## Members

- @noimin0610
- @prd-xxx
- @matsu7874

## Programming Language

We used Python.

## Usage

- `app` ディレクトリを変更したら以下のコマンドで変更後のプログラムを実行できる
```bash
docker build -t [container-name] .
docker run [container-name] [args for main.py]
```
 
### Attention

- build 時間は 10 分以内になるようにする
- プログラムはHTTPを介してオーガナイザーのサーバーと通信する必要があるが，インターネットにアクセスすることはできない
- Dockerfile の変更は不可

## Resources

|name|description|
|--|--|
|app/galaxy.txt|課題となる関数のリスト|
|check_result_error.txt|計算に成功した行の計算結果と与式|
|check_result_success.txt|計算に失敗した行のエラー内容と与式|
|variables_loop.txt|変数の循環参照を出力したもの|