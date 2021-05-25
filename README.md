### Wikiparser
Parses Wikipedia dumps into [TeXoo](https://github.com/sebastianarnold/TeXoo).

#### How to run it
Default:
```console
make kb
```
If you want to parse references in Wikipedia articles as annotations:
```console
make kb_annotated
```

If you require a specific dump, download it from from [Wikipedia](https://dumps.wikimedia.org/enwiki/latest/). This parser is only compatible with `pages-articles` dumps. Make sure that only one dump is in the project folder when running.
