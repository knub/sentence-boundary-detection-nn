### Concrete TODO for next meeting, Nov 19th

* Pipeline Breakthrough --> Given an unpunctuated and lowercase text, let our model run and output the predictions
* Implement proper POS tagging the NLP pipeline? Which tagger to use?
* Use POS tagging as features, there are three approaches (implement in order):
  * Just add the pos tags 1-of-V-encoded after the word vector. Use rather broad pos tags (maybe put a few similar pos tags in the same group)
  * Use second data channel .. might be good for convolution. However, how to encode the POS tags then? Is it possible to use the word2vec approach somehow for pos tags?
  * Use a fusion approach as Joseph proposed .. e.g. first transform the word vectors to the same size as the pos tags
* Prepare HDF5 output for Xiaoyin
* Precision/Recall per class - already implemented by Tanja and Stefan

### Ideas

* Consider features like: There was a question word in the last k statements
* Try LSTM (ask Christian Bartz for better Caffe LSTM implementation)


### TODO

* NLP pipelined: POS (1-v encoding?)
    * `text = word_tokenize("And now for something completely different")`
    * Use `pos_tag_sents()` for efficient tagging of more than one sentence.
* ensure valid train / test split
* have a look into the alignment tool: http://www1.icsi.berkeley.edu/Speech/docs/sctk-1.2/sclite.htm
* Tokenizer: Use tokenizer which maximizes hit rate in word vector
* Performance optimization for pos tagging
* Idea: Replace some tokens, e.g. 10, 11, 12 --> <NUMBER>
* Determine precision/recall for specific numbers

### Questions

* The xml-files in the data folders `dev2012-w` and `tst2014-w` are missing.
* How were the transcript files generated? The different data folders have different transcripts:
   * `dev2010-w, dev2012-w`: cleaned and uncleand, txt and ctm version; one file for each talk
   * `tst2010-w`: ctm and txt file; one file for all talks; no mapping to the talk id
   * `tst2011, tst2013-w, tst2014`: no transcript at all
   * `tst2012-w`: xml, ctm, txt file; one file for all talks; only xml file has some kind of mapping

### Answered Questions
* Do you know any open source ASR software we can use? No.
