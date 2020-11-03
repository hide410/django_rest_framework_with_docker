# postgresが入ったイメージをプルする
FROM postgres

# OSが扱う文字コードをUTF-8に、通貨の単位や年月日の表記の順番を日本仕様に設定する
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
ENV LANG ja_JP.UTF-8