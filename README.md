# ETL Exercise

prompt: [https://github.com/PlutoFlume/cr_eng_challenge_python](http://en.wikipedia.org/wiki/Markdown)

## Considerations:

- the input is a single json document which makes it difficult to chunk and parallelise the IO bound load task. With line oriented json that could have been an option. It would also be possible to use a C backed json parser like `ijson` but I decided to keep it python only.
- the mapping step between recipients and words could have benefited from a multiprocessing based map reduce approach since it's C
PU bound, but I didn't get that far.
- the flushing to the database phase is an IO bound operation so I've parallelised it with threads which is possible since the tables don't have relationships.
- the implementation is idempotent apart from word counts, which are incremented. email ids are hashes of the payloads and writes to the database ignore conflicts, or deal with them in the case of the 'Words' table.
- this is a quick script and is missing error handling, logging, packaging, etc.
- there are also no tests so it's very possible that there are bugs.
- it uses postgres as the database.


```
# grab data
curl https://raw.githubusercontent.com/PlutoFlume/cr_eng_challenge_python/dev/uploads.json > uploads.json

# install dependencies
pipenv install
# or
pip install click psycopg2

# usage
python main.py --help
Usage: main.py [OPTIONS]

Options:
  -f, --input-file TEXT
  -h, --db-host TEXT
  -u, --db-user TEXT
  -p, --db-password TEXT
  -d, --db-name TEXT
  --help                  Show this message and exit.
```

```
python main.py
Finished decoding json: 1.789s
Finished parsing input: 9.062s
Total time: 31.659s
```
