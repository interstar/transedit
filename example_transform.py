def transform(text):
    p = P(text).grep("foo").grep_v("bar").replace("old", "new")
    return p.run()
