- FastAPI 실행

```shell
uvicorn main:app --reload --port 8000
```

- thrift(HBASE) 서버 실행
```shell
$HBASE_HOME/bin/hbase-daemon.sh start thrift
```

- hbase shell
disable 'messages'
drop 'messages'
create 'messages', 'info'
exit


