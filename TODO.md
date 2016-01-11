### TODO

1. Improve model for lexical features!
2. Build a model for audio.
3. Implementation of post-processing the output of the model.

### TEST SERIES
* balanced classes
* with/without question mark
* pos tagging
* only line parser input
* with/without wikipedia

### Questions

### Ideas

* Consider features like: There was a question word in the last k statements
* Try LSTM: https://github.com/Russell91/nlpcaffe
* Data aggregation: rotation, some bit fiddling
* How to find commas after first word, e.g. "However COMMA I think that"?
* POS tagging:
  * Which windowing strategy to get the best possible tags?
  * Just add the pos tags 1-of-V-encoded after the word vector. Use rather broad pos tags (maybe put a few similar pos tags in the same group)
  * Use second data channel .. might be good for convolution. However, how to encode the POS tags then? Is it possible to use the word2vec approach somehow for pos tags?
  * Use a fusion approach as Joseph proposed .. e.g. first transform the word vectors to the same size as the pos tags

### Answered Questions
* Do you know any open source ASR software we can use? No.
* The xml-files in the data folders `dev2012-w` and `tst2014-w` are missing. -> Xiaoyin provided us a new training file (`/home/fb10dl01/workspace/ms-2015-t3/Data/Dataset/train200k`), but we should also take other text for the training of the lexical features.
* How were the transcript files generated? The different data folders have different transcripts:
   * `dev2010-w, dev2012-w`: cleaned and uncleand, txt and ctm version; one file for each talk
   * `tst2010-w`: ctm and txt file; one file for all talks; no mapping to the talk id
   * `tst2011, tst2013-w, tst2014`: no transcript at all
   * `tst2012-w`: xml, ctm, txt file; one file for all talks; only xml file has some kind of mapping
   * Answer: Xiaoyin is looking into that and tries to get the missing data.
   
