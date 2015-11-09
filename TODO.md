### TODO

* NLP pipelined: POS (1-v encoding?)
    * `text = word_tokenize("And now for something completely different")`
    * Use `pos_tag_sents()` for efficient tagging of more than one sentence.
* ensure valid train / test split
* have a look into the alignment tool: http://www1.icsi.berkeley.edu/Speech/docs/sctk-1.2/sclite.htm

### Questions

* Do you know any open source ASR software we can use?
* The xml-files in the data folders `dev2012-w` and `tst2014-w` are missing.
* How were the transcript files generated? The different data folders have different transcripts:
   * `dev2010-w, dev2012-w`: cleaned and uncleand, txt and ctm version; one file for each talk
   * `tst2010-w`: ctm and txt file; one file for all talks; no mapping to the talk id
   * `tst2011, tst2013-w, tst2014`: no transcript at all
   * `tst2012-w`: xml, ctm, txt file; one file for all talks; only xml file has some kind of mapping
