# MiloTextGen
 
MiloTextGen is a Python-based text generation library similar to [Tracery](https://tracery.io/). The grammar is generated from a CSV, TSV, or XLSX file provided by the user. Grammars are CFG-based. Each column header represents a rule, and each column entry is a single possible choice. Rules are enclosed by \[brackets]. Anything in brackets will be replaced by a randomly-chosen entry in the column with a name matching the string between the brackets.

Choices can also be weighted by inserting a 'weight' column directly to the right of a rule. I haven't made a tutorial yet (if people contact me asking for one I'll probably do it quicker though), so for now look at the example grammars to see how they're structured, and look at the example code for how to use the library to generate text!

You can also declare variables! Typing \[a=noun] will take an entry from the 'noun' column and set it equal to a. From that point on, any \[a] within the grammar will evaluate to whatever noun was generated the first time.

The library also offers several modifiers to make grammatical agreement easier to implement. Most of these come from the [Pattern](https://github.com/clips/pattern) and [NLTK](https://www.nltk.org/) libraries. The modifiers are:

\[rule.a] puts a or an before a noun at the beginning of a produced string 
\[rule.cap] capitalizes the first letter of produced string. All other capitalization is left the same.
\[rule.ed] produces past tense of a verb at the end of a produced string.
\[rule.s] produces plural of noun at the end of a produced string 
\[rule.ing] produces gerund of verb at the end of a produced string
\[rule.er] produces comparative of the last word (e.g. big->bigger, good->better)
\[rule.est] produces superlative of the last word (e.g. big->biggest, bad->worst)
\[rule.1p] produces 1st person version of a verb at the end of a produced string
\[rule.2p] produces 2nd person version of a verb at the end of a produced string
\[rule.3p] produces 3rd person version of a verb at the end of a produced string

These commands can be chained (e.g. \[rule.a.cap] is perfectly valid). For real English words, the Pattern library is used for most items (except for the 'a' command, which has worked better for me with NLTK). For non-real words, the program uses a rules-based approach that works with reasonable believability. The 1p, 2p, and 3p commands do not modify non-real words, however.