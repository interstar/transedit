# TransEdit

Small Python "text editor" which works by applying a pipeline of transformations (written as a Python function) to the text.

## Why?

Sometimes you have a text file. You want to run a script to process it, but see the result interactively.

Perhaps you want to filter it for only the lines containing certain keywords. Perhaps do a regex based text replacement on each line.

These are the things that tools like awk and sed are great for. The classic small Unix tools.

But there's a problem with the Unix pipeline. The results appear on your terminal and are lost.

Or you pipe those results into a new file. But then you can't see the result until you then open that file in a separate editor.

And if you made a mistake in your script, you have to go back and do the whole thing again.

Alternatively, you can open in a normal text editor and use the search and replace tools, doing the changes step by step, manually. But if you make a mistake, or just want to try a different transformation, rewinding is laborious.


In other words, we often want to do bulk processing on files, interactively, and have the option of tweaking the transformation as we look over the results.

So what you want is the benefits of both a pipeline of simple transformations AND the interactivity of a text editor.

That's where transedit comes in.

It's simple. Two panels. One for the script that processes the input file. One for the result of the processing.

Want to keep tweaking and fiddling with the script? You can. The processing is non-destructive.

Want to hand edit and save the final results when you are satisfied? Yes, you can.

## Quick start.

Make sure you have the dependencies. 

**Additional Setup for Ubuntu**

On Ubuntu, Tkinter is not included by default. Please install it using:

    sudo apt-get install python3-tk 


The application also needs BeautifulSoup
    
    pip install beautifulsoup4
    

Then go into the transedit directory and run transedit on a file like this:

    cd transedit
    python ./transedit.py [PATH/TO/FILE]
    
If you run it without the file to work on, you will be able to load it within the GUI.

When the program runs, you'll see two panes. 

On the left is the script editor. In this you will write a Python function called `transform` which will do the transformations on your file.

The simplest script does nothing to the file. 

     def transform(text) : 
         return text
     
To run it, just click the `Process Script` button to apply the current processing pipeline to the currently loaded file, and show the results in the output (right-hand) panel.

## The Pipeline / Processing Object

You can write any Python function that can process the text file. But to simplify building a pipeline of simple filters and transformations, there's a pipeline or process object, simply called P

Here's how to use it

```
def transform(text):
    p = P(text).grep("foo").grep_v("bar").replace("old", "new")
    return p.run()
```

P(text) creates a P object containing the text. We can then chain up as many transformations in the form of 

* `grep` - a filter for only those lines that match a pattern.
* `grep_v` - a filter for only those lines that DON'T match a pattern.
* `replace` - a string replacement applied to each line.

`run()` runs the text lines through the pipeline and returns the final transformed text, which will get displayed in the right panel.

### Using Regexes

P also regex-based filter and replace functions.
* `re_search(r'PATTERN')` - filter which allows through only those lines that contain text matching the regex PATTERN. 
* `re_search_fails(r'PATTERN')` - a negated version of the re_search. Ie returns only those lines that DON'T contain text matching the regex PATTERN.
* `re_sub(r'PATTERN',r'NEWPAT')` - regex based search and replace. Uses re.sub so can do everything Python's re can do.

For example

```
def transform(text):
    p = P(text).re_search_fail('youtube').re_sub(r'(.+?),(.+)',r'\2,\1')
    return p.run()
```

Will find all the lines that DON'T contain the word 'youtube', and will then split those lines at the first comma, and return those two items in the reversed order. (Ie. item 2, item 1)

Here's a useful way to split a text file into a part that matches a pattern, followed by a part that doesn't.

```
def transform(text) :
    pat="PATTERN"
    p=P(text).re_search(pat).run()
    q=P(text).re_search_fails(pat).run()

    return """%s
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%s"""% (p,q) 
```

## Beautiful Soup

We also include BeautifulSoup, so we can process HTML etc files.

```
def transform(text) :
  soup = BeautifulSoup(text)
  return soup.get_text()
```

