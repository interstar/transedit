# Transedit

Small Python "text editor" which works on a pipeline of transformation you write in Python code.


Sometimes you have a text file and you just want to do some processing on it but see the result interactively.

Perhaps filter it for the lines containing certain keywords. Perhaps do some basic text replacement.

These are the things that tools like awk and sed are great for. The classic small Unix tools.

But there's a problem with the Unix pipeline. The results appear on your terminal and are lost.

Or you pipe it into a file. But you can't see the result until you then open that file.

If you made a mistake, you have to go back and do the whole thing again.

Sometimes you might want to tweak the processing pipeline. Or hand edit the results.

What you want is the benefits of both a pipeline of simple transformations AND the interactivity of a text editor.

That's where transedit comes in.

It's simple. Two panels. One for the script that processes the input file. One for the result of the processing.

Want to tweak and fiddle with the script? You can. The processing is non-destructive.

Want to hand edit and save the final results? Yes, you can.

## Quick start.

Make sure you have the dependencies. Basically tkinter

    sudo apt-get install python3-tk 
    
in Ubuntu.

Then run transedit on a file like this.

    python ./transedit.py [PATH/TO/FILE]
    
You'll see two panes. 

Type your script (a Python function) into the left pane. The simplest script that does nothing is just 

     def transform(text) : return text
     
Then click the `Process Script` button to apply the current processing pipeline to the original file and show the results in the output panel.

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

### Beautiful Soup

We also include BeautifulSoup, so we can process HTML etc files.

```
def transform(text) :
  soup = BeautifulSoup(text)
  return soup.get_text()
``

