Guaranteed to work with [starterkit-python](https://github.com/icfpcontest2020/starterkit-python).
Base image `icfpcontest2020/python:latest` built automatically from `Dockerfile.base`.

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
|app/check_result_error.txt|計算に成功した行の計算結果と与式|
|app/check_result_success.txt|計算に失敗した行のエラー内容と与式|
|variables_loop.txt|変数の循環参照を出力したもの|